import cv2
import yaml
import os
import glob
import typer
from loguru import logger
from typing import List, Dict
import time
import io

def getImages(path:str) ->List[str] :
    """get images inside directory

    Args:
        path (str): path of the directory

    Returns:
        List[str]: list of file pathes
    """    
    # use glob to find all files with the specified extensions
    png_files = glob.glob(path + '/*.png')
    jpg_files = glob.glob(path + '/*.jpg')
    jpeg_files = glob.glob(path + '/*.jpeg')

    # combine all lists into one
    return png_files + jpg_files + jpeg_files

def loadConfig():
    try:
        with open('config/class.yaml', 'r') as file:
            class2idx = yaml.safe_load(file)
    except:
        logger.warning("No config found in config/class.yaml")
    return class2idx

def cmdGen(key: int, ann: io.TextIOWrapper, filename:str, cls2idx: Dict[str, int]):
    breakpoint()
    for cls, idx in cls2idx.items():
        if key == ord(str(idx)):
            logger.info(f"{filename} has class: {cls}, index: {idx}")
            ann.write(f"{filename} {idx}\n")
            cv2.destroyAllWindows()

def main(in_path: str = typer.Option(..., "--path", "-i", help="Path to input images")):

    directory = "result"
    if not os.path.exists(directory):
        logger.info(f"{directory} doesn't exist, so create new one.")
        os.makedirs(directory)

    unixTime = int(time.time())
    logger.add(os.path.join(directory, f"log_{unixTime}.txt"), rotation="100 MB")
    ann = open(os.path.join(directory, f'ann_{unixTime}.txt'), 'a')
    
    # Configure logger to save logs to a file
    
    cls2idx = loadConfig()
    logger.info("Config file below.")
    logger.opt(raw=True).info(yaml.dump(cls2idx))
    
    image_files = getImages(in_path)
    logger.info(f"Total {len(image_files)} images are loaded.")

    # Loop through images
    for filename in image_files:
        # Read image
        img = cv2.imread(filename)

        # Display image
        cv2.imshow('Image', img)

        # Wait for keyboard input
        key = cv2.waitKey(0)

        # Check if user pressed 'q' key to quit
        if key == ord('q'):
            logger.info(f"Leave annotation process at {filename}")
            ann.close() 
            break

        cmdGen(key, ann, os.path.basename(filename), cls2idx)
        if key == ord("x"):
            logger.info(f"Made mistake at {old_filename}")
        old_filename = filename


    # Close all windows
    ann.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    typer.run(main)