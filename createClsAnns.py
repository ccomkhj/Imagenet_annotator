import io
import os
import shutil
import time
from pathlib import Path
from typing import Dict, List

import cv2
import typer
import yaml
from loguru import logger
from typing_extensions import Annotated

from tools.helpers import getImages


def loadConfig():
    try:
        with open("config/class.yaml", "r") as file:
            class2idx = yaml.safe_load(file)
    except:
        logger.warning("No config found in config/class.yaml")
    return class2idx


def cmdGen(key: int, ann: io.TextIOWrapper, filename: str, cls2idx: Dict[str, int]):
    for cls, idx in cls2idx.items():
        if key == ord(str(idx)):
            logger.info(f"{filename} has class: {cls}, index: {idx}")
            ann.write(f"{filename} {idx}\n")
            cv2.destroyAllWindows()

            return cls
    return False


def main(
    in_path: str = typer.Option(..., "--in_path", "-i", help="Path to input images"),
    begin_index: Annotated[
        int,
        typer.Option(
            ...,
            "--begin",
            "-b",
            help="Begin with specific index (ignore files before index)",
        ),
    ] = 0,
    save: Annotated[
        bool,
        typer.Option(
            ..., "--save", "-s", help="Path to save successfully classified images"
        ),
    ] = False,
    folder: Annotated[
        bool,
        typer.Option(..., "--folder", "-f", help="Image saved into each class folder"),
    ] = False,
):
    directory = Path("result")
    if not os.path.exists(directory):
        logger.info(f"{directory} doesn't exist, so create new one.")
        os.makedirs(directory, exist_ok=True)

    # Configure logger to save logs to a file

    cls2idx = loadConfig()
    logger.info("Config file below.")
    logger.opt(raw=True).info(yaml.dump(cls2idx))

    unixTime = int(time.time())

    if save:
        save_path = Path(directory) / "success" / str(unixTime)
        os.makedirs(save_path, exist_ok=True)
    
        if folder:
            for obj in cls2idx.keys():
                save_path_obj = Path(directory) / "success" / str(unixTime) / obj
                os.makedirs(save_path_obj, exist_ok=True)


    logger.add(os.path.join(directory, f"log_{unixTime}.txt"), rotation="100 MB")
    ann = open(os.path.join(directory, f"ann_{unixTime}.txt"), "a")


    image_files = getImages(in_path)
    logger.info(f"Total {len(image_files)} images are loaded.")

    if begin_index != 0:
        logger.info(f"Begin annotation from index: {begin_index}")

    # Loop through images
    for idx, filename in enumerate(image_files[begin_index:]):
        # Read image
        img = cv2.imread(filename)

        # Display image
        cv2.imshow("Image", img)

        # Wait for keyboard input
        key = cv2.waitKey(0)

        # Check if user pressed 'q' key to quit
        if key == ord("q"):
            logger.info(f"Leave annotation process at {filename}. (idx: {idx}")
            ann.close()
            break
        if key == ord("x"):
            logger.info(f"Made mistake at {prev_filename} [Right before image]")
            # Don't save the previous things
            continue
        if key == ord("s"):
            logger.info(f"Skip {filename}, this image is not relevant.")
            # Don't save the previous things
            continue

        success = cmdGen(key, ann, os.path.basename(filename), cls2idx)

        if success and save and not folder:
            dst = save_path / Path(filename).name
            shutil.copy(filename, dst)

        elif success and save and folder:
            # success is the name of class
            dst = save_path / success / Path(filename).name
            shutil.copy(filename, dst)

        prev_filename = filename

    # Close all windows
    ann.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    typer.run(main)
