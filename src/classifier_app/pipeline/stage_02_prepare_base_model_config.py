from classifier_app.config.configuration import ConfigurationManager
from classifier_app.components import PrepareBaseModel


try :

    config = ConfigurationManager()
    prepareBaseModel = PrepareBaseModel(config= config.PrepareBaseModelConfig())
    prepareBaseModel.get_base_model()
    prepareBaseModel.update_base_model()

except Exception as e:
    raise e