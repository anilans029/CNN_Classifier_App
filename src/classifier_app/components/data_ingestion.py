import shutil
from webbrowser import get
from classifier_app.entity.config_entity import DataIngestionConfig
import urllib.request as request
from zipfile import ZipFile
import os
from classifier_app import logger
from classifier_app.utils import get_size
from tqdm import tqdm
from pathlib import Path
from classifier_app.utils import create_directories
import numpy as np
from tqdm import tqdm



class DataIngestion:

    def __init__(self, config: DataIngestionConfig):

        self.config = config

    
    def download_file(self):
        
        try:
            logger.info(f"Trying to download file....")
            if not os.path.exists(self.config.local_data_file):
                
                logger.info(f" Download Started .....")
                filename, headers = request.urlretrieve(self.config.soruce_url,
                                    filename=self.config.local_data_file)
                
                logger.info(f"{filename} Succefully downloaded the file at: {[self.config.local_data_file]} with following info: /n {headers}")
            
            else:
                file_size = get_size(Path(self.config.local_data_file))
                logger.info(f"File already exists of size : {file_size} ")
        
        except Exception as e:
            raise e


    def _get_updated_list_of_file(self,list_of_files):
            return [f for f in list_of_files if f.endswith(".jpg") and ("Dog" in f or "Cat" in f) ]

    
    def _preprocess(self, zf: ZipFile, f: str, working_dir: str):
        target_filepath = os.path.join(working_dir, f)
        
        ## checking for the file is present in the working directory or not
        if not os.path.exists(target_filepath):
            zf.extract(f, working_dir)

        ## checking whether the file is of size 0 KB
        if os.path.getsize(target_filepath)==0:
            target_file_size = get_size(Path(target_filepath))
            logger.info(f"Removing file: {target_filepath} of size : {target_file_size}")
            os.remove(target_filepath)

    
    def unzip_and_clean(self, ):
        logger.info(f"unzipping file and removing unwanted files.....")
        with ZipFile(file = self.config.local_data_file,mode = "r") as zf:
                list_of_files = zf.namelist()   
                updated_list_of_files = self._get_updated_list_of_file(list_of_files)

                ## preprocessing
                for f in tqdm(updated_list_of_files):
                    self._preprocess(zf, f,self.config.unzip_dir)

    def train_test_split(self):
        train_dir = os.path.join(self.config.split_data, self.config.train_dir_name)
        test_dir =  os.path.join(self.config.split_data, self.config.test_dir_name)
        ## creating the target directories
        dirs = [train_dir, test_dir]
        create_directories(dirs)

        train_ratio = self.config.params_train_ratio
        test_ratio = self.config.params_test_ratio

        base_dir  = os.listdir(self.config.unzip_dir)[0]
        classes = os.listdir(os.path.join(self.config.unzip_dir, base_dir))

        for cls in classes:
            cur_dir = os.path.join(self.config.unzip_dir,base_dir, cls)
            files = os.listdir(cur_dir)
            np.random.shuffle(files)

            for dir in dirs:
                target_dir = os.path.join(dir, cls)
                create_directories([target_dir])
                if dir == train_dir:
                    train_files = files[: int(len(files)*train_ratio)]
                    print(f"copying the train_data_files of {cls} class to {target_dir}")
                    for train_file in tqdm(train_files):
                        src_file_path = os.path.join(cur_dir,train_file)
                        shutil.copy(src_file_path, target_dir)
                
                elif dir== test_dir:
                    test_files = files[int(len(files)*train_ratio):]
                    print(f"copying the test_data_files of {cls} class to {target_dir}")
                    for test_file in tqdm(test_files):
                        src_file_path = os.path.join(cur_dir, test_file)
                        shutil.copy(src_file_path, target_dir)



        







