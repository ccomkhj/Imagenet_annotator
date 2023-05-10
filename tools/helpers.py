import glob
from typing import List

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