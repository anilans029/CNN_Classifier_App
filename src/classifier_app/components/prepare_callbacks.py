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
