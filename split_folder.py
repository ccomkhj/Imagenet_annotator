import os
import random
import shutil
from pathlib import Path
from typing import List, Tuple

import typer
from loguru import logger
from typing_extensions import Annotated

from tools.helpers import getImages


def split_train_val(path: str, ratio: float = 0.8) -> Tuple[List, List]:
    objs = getImages(path)

    random.shuffle(objs)
    split_idx = int(len(objs) * ratio)

    logger.info(f"train files: {split_idx} and val files: {len(objs)-split_idx}")

    train = objs[:split_idx]
    val = objs[split_idx:]

    return train, val


def split(img_path: str, ratio: float):
    train_path = Path(img_path) / "train"
    val_path = Path(img_path) / "val"

    # get obj class from folder names
    folders = [
        os.path.join(img_path, f)
        for f in os.listdir(img_path)
        if f not in ["train", "val"]
    ]



    for folder in folders:

        objType = Path(folder).parts[-1]

        # Create directories
        if not os.path.exists(train_path / objType):
            logger.info(f"{train_path / objType} doesn't exist, so create new one.")
            os.makedirs(train_path / objType, exist_ok=True)
            
        if not os.path.exists(val_path / objType):
            logger.info(f"{val_path / objType} doesn't exist, so create new one.")
            os.makedirs(val_path / objType, exist_ok=True)

        train, val = split_train_val(folder, ratio)
        logger.info(f"works with {objType} with train: {len(train)}, val: {len(val)}")

        # Move files
        for train_obj in train:
            dst = train_path / objType / Path(train_obj).name
            shutil.move(train_obj, dst)

        for val_obj in val:
            dst = val_path / objType / Path(val_obj).name
            shutil.move(val_obj, dst)


def main(
    img_path: str = typer.Option(..., "--img_path", "-i", help="Path to images"),
    ratio: Annotated[
        float,
        typer.Option(..., "--ratio", "-r", help="split ratio between train and val"),
    ] = 0.8,
):
    split(img_path, ratio)


if __name__ == "__main__":
    typer.run(main)
