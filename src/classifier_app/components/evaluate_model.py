from classifier_app.entity import EvaluateConfig
import tensorflow as tf
from pathlib import Path
from classifier_app.utils import save_json



class Evaluate_Model:

    def __init__(self, config: EvaluateConfig):
        self.config = config
        print(self.config)
    
    def _load_model(self):
        self.model  = tf.keras.models.load_model(self.config.trained_model_path)

    def _test_generator(self):

        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                            rescale= 1/255.0
        )

        test_generator = test_datagen.flow_from_directory(
                                directory= self.config.test_data_path,
                                target_size= self.config.params_target_size,
                                interpolation= self.config.params_interpolation,
                                batch_size= self.config.params_batch_size
        )
        return test_generator

    def evaluateModel(self):
        self._load_model()
        test_generator = self._test_generator()
        self.score  = self.model.evaluate(test_generator)
        self._save_score()

    def _save_score(self):
        score = dict({
                    "loss":self.score[0],
                    "accuracy": self.score[1]
        })
        score_path = Path("scores.json")
        save_json(path_to_save=Path(score_path), data= score)
    
            
        