from tools.helpers import getImages
import typer
from typing_extensions import Annotated
from pathlib import Path
from loguru import logger
from typing import List, Tuple
import random
import shutil
import os

def split_train_val(ann: str, ratio:float = 0.8) -> Tuple[List, List]:
    objs = []
    with open(ann, 'r') as f:
        contents = f.read().split('\n')
        for content in contents:
            objs.append(content)

    random.shuffle(objs)
    split_idx = int(len(objs)*ratio)

    logger.info(f"train files: {split_idx} and val files: {len(objs)-split_idx}")

    train = objs[:split_idx]
    val = objs[split_idx:]

    return train, val


def check_mismatching(imgs, anns):
    if len(imgs) != len(anns): 
        logger.info(f"the number of annotation and file are different. # images: {len(imgs)}, # anns: {len(anns)}")

    img_only_names = [Path(img).name for img in imgs]
    flag = False

    checkedAnns = []

    # check: anns -> imgs 
    for ann in anns:
        file_name = ann.split()[0]
        if file_name not in img_only_names:
            logger.warning(f"Anns > Images, {ann} is not in training set.")
            flag = True
        else:
            checkedAnns.append(file_name)

    # check: imgs -> anns
    for file_name in img_only_names:
        if file_name not in checkedAnns:
            logger.warning(f"Images > Anns, {file_name} is not in training set.")
            flag = True

    if flag:
        raise ValueError("Not proceeding further. Check between ann and images.")

def split(img_path: str, ann: str, ratio: float):

    imgs = getImages(img_path)
    train, val = split_train_val(ann, ratio)

    check_mismatching(imgs, train+val)

    train_path = Path(img_path) / "train"
    val_path = Path(img_path) / "val"

    # Create directories
    if not os.path.exists(train_path):
        logger.info(f"{train_path} doesn't exist, so create new one.")
        os.makedirs(train_path, exist_ok = True)
    if not os.path.exists(val_path):
        logger.info(f"{val_path} doesn't exist, so create new one.")
        os.makedirs(val_path, exist_ok = True)

    # Move files
    for train_obj in train:
        filename = train_obj.split()[0] 
        dst = train_path / filename
        shutil.move(Path(img_path) / filename, dst)

    for val_obj in val:
        filename = val_obj.split()[0] 
        dst = val_path / filename
        shutil.move(Path(img_path) / filename, dst)

    # Write annotation text files
    with open (Path(img_path) / 'train.txt', 'w') as file:
        for t_line in train:
            file.write(t_line + '\n')

    with open (Path(img_path) / 'val.txt', 'w') as file:
        for v_line in val:
            file.write(v_line + '\n')


def main(img_path:str = typer.Option(..., "--img_path", "-i", help="Path to images"),
         ann: str = typer.Option(..., "--ann", "-a", help="Path to annotation file"), 
         ratio: Annotated[float, typer.Option(..., "--ratio", "-r", help= "split ratio between train and val")] = 0.8):
    split(img_path, ann, ratio)

if __name__ == "__main__":
    typer.run(main)