import tensorflow as tf
import time
from classifier_app.entity import PrepareCallbacksconfig,TrainingConfig
import os
from pathlib import Path


class PrepareCallback:

    def __init__(self, config: PrepareCallbacksconfig):
        self.config = config

    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(
                                        self.config.tensorboard_root_log_dir,
                                        f"tb_logs_at_{timestamp}"
        )
        print(tb_running_log_dir)                                
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)

    @property
    def _create_ckpt_callbacks(self):
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=self.config.checkpoint_model_filepath,
            save_best_only= True
        )

    @property
    def _create_earlyStopping_callbacks(self):
        return tf.keras.callbacks.EarlyStopping(
            monitor= "val_loss",
            min_delta= 0.001,
            patience=8,
            verbose = 0,
            mode = "auto",
            restore_best_weights=True            
        )


    def get_tb_ckpt_estopping_callbacks(self):
        return [
            self._create_tb_callbacks,
            self._create_ckpt_callbacks,
            self._create_earlyStopping_callbacks
        ]


from statistics import mode
import tensorflow as tf
import time

class Training:

    def __init__(self, config: TrainingConfig):
        self.config = config

    
    def get_base_model(self):
        self.model = tf.keras.models.load_model(filepath= self.config.updated_base_model_path)
        

    def train_Valid_generator(self):
        
        datagenerator_kargs = dict(
                                rescale = 1/255.0,
                                validation_split=0.20

                                )

        dataflow_kwargs = dict(
                            target_size = self.config.params_image_size[:-1],
                            batch_size = self.config.params_batch_size,
                            interpolation = "bilinear"
                            )

        valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kargs)

        if self.config.params_is_augmentation:
            train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                                    rotation_range= 20,
                                    zoom_range= 0.20,
                                    width_shift_range= 0.20,
                                    height_shift_range= 0.20,
                                    shear_range= 0.20,
                                    horizontal_flip= True,
                                    vertical_flip= True,
                                    **datagenerator_kargs
            )
        else:
            train_datagen = valid_datagen

        self.train_generator = train_datagen.flow_from_directory(
                            directory= self.config.training_data,
                            subset= "training",
                            shuffle= True,
                            **dataflow_kwargs            
                            )

        self.valid_generator = valid_datagen.flow_from_directory(
                                directory= self.config.training_data,
                                shuffle= False,
                                subset = "validation",
                                **dataflow_kwargs
                                )
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(filepath= path)

    def train(self, callbackList: list):
        self.steps_per_epoch = self.train_generator.samples//self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples// self.valid_generator.batch_size

        self.model.fit(
                    self.train_generator,
                    validation_data = self.valid_generator,
                    steps_per_epoch = self.steps_per_epoch,
                    validation_steps = self.validation_steps,
                    epochs= self.config.params_epochs,
                    callbacks = callbackList

        )

        self.save_model(path = self.config.trained_model_path, model = self.model)   

    

