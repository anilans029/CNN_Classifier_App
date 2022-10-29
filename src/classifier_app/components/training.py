import tensorflow as tf
import time
from classifier_app.entity import TrainingConfig
import os
from pathlib import Path

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

    

