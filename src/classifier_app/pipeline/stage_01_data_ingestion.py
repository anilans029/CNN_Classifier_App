from classifier_app.config import ConfigurationManager
from classifier_app.components import DataIngestion
from classifier_app import logger

STAGE_NAME = "Data Ingestion Stage"

def main():
    try:
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.unzip_and_clean()
        data_ingestion.train_test_split()

    except Exception as e:
        raise e


if __name__ == "__main__":
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")

    except Exception as e:
        logger.exception(e)
        raise e