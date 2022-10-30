from classifier_app.constants import *
from classifier_app.utils import read_yaml,create_directories
from classifier_app.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, PrepareCallbacksconfig,TrainingConfig
import os


class ConfigurationManager:


    def __init__(self, 
                    config_file_path = CONFIG_FILE_PATH,
                    params_filepath = PARAMS_FILE_PATH):
                    
                    self.config = read_yaml(config_file_path)
                    self.params = read_yaml(params_filepath)
                    
                    create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self)-> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
                                root_dir=Path(config.root_dir),
                                soruce_url=Path(config.source_url),
                                local_data_file = Path(config.local_data_file),
                                unzip_dir=Path(config.unzip_dir),
                                train_dir_name= Path(config.train_dir_name),
                                test_dir_name= Path(config.test_dir_name),
                                split_data= Path(config.split_data),
                                params_train_ratio= self.params.TRAIN_RATIO,
                                params_test_ratio = self.params.TEST_RATIO
                              )
        return data_ingestion_config

    def PrepareBaseModelConfig(self)-> PrepareBaseModelConfig:
        config = self.config.prepare_Base_Model
        params = self.params

        create_directories([config.root_dir])

        prepareBaseModelConfig = PrepareBaseModelConfig(
                                root_dir=Path(config.root_dir),
                                base_model_path = Path(config.base_model_path),
                                updated_base_model_path= Path(config.updated_base_model_path),
                                params_CLASSES = params.CLASSES,
                                params_WEIGHTS = params.WEIGHTS,
                                params_LEARNING_RATE = params.LEARNING_RATE,
                                params_INCLUDE_TOP= params.INCLUDE_TOP,
                                params_IMAGE_SIZE=params.IMAGE_SIZE
                                )
        return prepareBaseModelConfig

    def get_prepareCallbackConfig(self)-> PrepareCallbacksconfig:
        config = self.config.prepare_callbacks
        params = self.params


        # checkpoint_model_dir, _  =  os.path.split(config.checkpoint_model_filepath)
        checkpoint_model_dir = os.path.dirname(config.checkpoint_model_filepath)
        early_stopping_checkpoint_dir = os.path.dirname(config.early_stopping_checkpoint_filepath)

        
        create_directories([Path(config.root_dir), Path(config.tensorboard_root_log_dir),
                            Path(checkpoint_model_dir),
                            Path(early_stopping_checkpoint_dir)])
        

        prepareCallbacksconfig = PrepareCallbacksconfig(
                                root_dir=Path(config.root_dir),
                                tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
                                checkpoint_model_filepath=Path(config.checkpoint_model_filepath),
                                early_stopping_checkpoint_filepath= Path(config.early_stopping_checkpoint_filepath)
                                
                                )
                                
        return prepareCallbacksconfig    
    

    def get_training_config(self)-> TrainingConfig:
        config_training = self.config.training
        config_model = self.config.prepare_Base_Model
        training_data_path =os.path.join(Path(self.config.data_ingestion.split_data),Path(self.config.data_ingestion.train_dir_name))
        testing_data_path =os.path.join(Path(self.config.data_ingestion.split_data),Path(self.config.data_ingestion.test_dir_name))

        params = self.params        
        create_directories([Path(config_training.root_dir)])

        trainingConfig = TrainingConfig(
                            root_dir=Path(config_training.root_dir),
                            trained_model_path=Path(config_training.trained_model_path),
                            updated_base_model_path = Path(config_model.updated_base_model_path),
                            training_data = training_data_path,
                            testing_data = testing_data_path,
                            params_epochs = self.params.EPOCHS,
                            params_batch_size= self.params.BATCH_SIZE,
                            params_is_augmentation= self.params.AUGMENTATION,
                            params_image_size= self.params.IMAGE_SIZE
                                )
                                
        return trainingConfig