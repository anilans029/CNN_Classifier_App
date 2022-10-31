from classifier_app.config import ConfigurationManager
from classifier_app.components import Evaluate_Model



try:
    config = ConfigurationManager()
    evaluate_config = config.get_evaluation_config()
    evaluation = Evaluate_Model(config=evaluate_config)
    evaluation.evaluateModel()
    

except Exception as e:
    raise e