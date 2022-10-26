from sys import path_importer_cache
from classifier_app import logger
import os
import yaml
import json
import joblib
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from box import ConfigBox
from classifier_app import logger

@ensure_annotations
def read_yaml(path_to_yaml: Path)-> ConfigBox:
    """
    The read_yaml function reads a yaml file and returns a ConfigBox object.

    Args:
        path_to_yaml:Path: Pass the path to the yaml file

    Returns:
        A configbox object

    """
  
    try:
        with open(path_to_yaml,"r") as yaml_file:
            yaml_file_content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(yaml_file_content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    The create_directories function creates directories at the specified paths.
    The function accepts a list of strings, where each string is a path to a directory that should be created.
    If the directory already exists, it will not be overwritten.


    Args:
        path_to_directories:list: Pass a list of paths to the function
        verbose=True: Print the message to the console

    Returns:
        None
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created the directory at : {path}")


@ensure_annotations
def save_json(path_to_save: Path, data:dict):
    """
    The save_json function saves a dictionary as a json file.
    The function takes two arguments: path_to_save and data. 
    path_to_save is the location where the json file will be saved, 
    while data is the dictionary that will be converted to json format.

    Args:
        path_to_save:Path: Specify the path where you want to save your json file
        data:dict: Pass the data that we want to save in json format

    Returns:
        A dict
    """

    with open(path_to_save,"w") as f:
        json.dump(data,f, indent=4)

    logger.info(f"json file saved at : {path_to_save}")


@ensure_annotations
def load_json(json_file_path: Path)-> ConfigBox:
    """
    The load_json function loads a json file from the specified path and returns it as a ConfigBox.


    Args:
        json_file_path:Path: Specify the path to the json file

    Returns:
        A configbox object
    """


    with open(json_file_path,"r") as f:
        json_file_content = json.load(f)

    logger.info(f"json file loaded successfully from : {json_file_path}")
    return ConfigBox(json_file_content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    The save_bin function saves a binary file to the specified path.
    It accepts two arguments: data and path.
    data is the object that will be saved in binary format, and path is the location where it will be saved.

    Args:
        data:Any: Store the data that needs to be saved
        path:Path: Specify the path where the binary file is to be saved

    Returns:
        The path where the binary file is saved
    """

    joblib.dump(value = data,filename=path)
    logger.info(f"binary file saved at : {path}")


@ensure_annotations
def laod_bin(path: Path)-> Any:
    """
    The laod_bin function loads a binary file from the specified path.
    

    Args:
        path:Path: Specify the location of the binary file

    Returns:
        The data that was stored in the binary file
    """


    data = joblib.load(filename=path)
    logger.info(f"binary file loaded from : {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """
    The get_size function returns the size of a file in KB.
    Args:
        path (Path): path of the file
    Returns:
        str: size in KB
    
    Args:
        path:Path: Pass the path of the file to be checked
    
    Returns:
        The size of the file in kb
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"