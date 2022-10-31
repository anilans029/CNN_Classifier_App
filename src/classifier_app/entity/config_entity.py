from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path

DataIngestionConfig = namedtuple("DataIngestionConfig",[
                            "root_dir",
                            "soruce_url",
                            "local_data_file",
                            "unzip_dir",
                            "train_dir_name",
                            "test_dir_name",
                            "split_data",
                            "params_train_ratio",
                            "params_test_ratio"
                                ])


@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path

    params_CLASSES: int
    params_WEIGHTS: str
    params_LEARNING_RATE: float
    params_INCLUDE_TOP: bool
    params_IMAGE_SIZE: list

@dataclass(frozen=True)
class PrepareCallbacksconfig:
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path
    early_stopping_checkpoint_filepath: Path

@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    testing_data: Path
    params_epochs: int
    params_batch_size:int
    params_is_augmentation: bool
    params_image_size: list

@dataclass
class EvaluateConfig:
    trained_model_path: Path
    root_dir: Path
    test_data_path: Path
    params_target_size: list
    params_batch_size: int
    params_interpolation : str



