from classifier_app.config.configuration import ConfigurationManager
from classifier_app.components import PrepareCallback, Training


try :

    config = ConfigurationManager()
    prepareCallbacks = PrepareCallback(config= config.get_prepareCallbackConfig())
    callbacklist = prepareCallbacks.get_tb_ckpt_estopping_callbacks()

    
    training = Training(config= config.get_training_config())
    training.get_base_model()
    training.train_Valid_generator()
    training.train(callbackList= callbacklist)
except Exception as e:
    raise e