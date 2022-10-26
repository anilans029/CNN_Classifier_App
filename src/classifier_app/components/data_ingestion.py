from webbrowser import get
from classifier_app.entity.config_entity import DataIngestionConfig
import urllib.request as request
from zipfile import ZipFile
import os
from classifier_app import logger
from classifier_app.utils import get_size
from tqdm import tqdm
from pathlib import Path


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