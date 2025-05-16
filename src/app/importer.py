import os
import kaggle
import kagglehub
from kagglehub import KaggleDatasetAdapter
import zipfile
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def download_from_kaggle(dataset_address: str, file_name: str = None) -> None:
    try:
        logger.info(f"Downloading from Kaggle: {dataset_address}")
        if file_name:
            kaggle.api.dataset_download_file(dataset_address, file_name)
        else:
            kaggle.api.dataset_download(dataset_address)
        logger.info("Download completed successfully")
    except Exception as e:
        logger.error(f"Error downloading from Kaggle: {str(e)}")
        raise


def unzip(unzip_from: str, unzip_to: str, delete: bool = True) -> None:
    try:
        logger.info(f"Unzipping {unzip_from} to {unzip_to}")
        with zipfile.ZipFile(unzip_from, "r") as zip_ref:
            zip_ref.extractall(unzip_to)
        if delete:
            os.remove(unzip_from)
            logger.info(f"Deleted zip file: {unzip_from}")
        logger.info("Unzip completed successfully")
    except Exception as e:
        logger.error(f"Error unzipping file: {str(e)}")
        raise


# TODO: move_to está fazendo o download do arquivo na raiz do projeto.
def download_dataset(
    dataset_address: str,
    file_name: str,
    move_to: str = ".",
    unzip: bool = True,
    delete: bool = True,
) -> None:
    try:
        logger.info(f"Starting dataset download process for {dataset_address}")
        download_from_kaggle(dataset_address, file_name)

        if unzip:
            base_name = file_name.rsplit(".", 1)[0]
            zip_file = f"{base_name}.zip"
            unzip(zip_file, move_to, delete)
        else:
            if move_to != ".":
                os.makedirs(move_to, exist_ok=True)
                os.rename(file_name, os.path.join(move_to, file_name))
                logger.info(f"Moved file to {move_to}")
        logger.info("Dataset download process completed")
    except Exception as e:
        logger.error(f"Error in download_dataset: {str(e)}")
        raise


# TODO: Pode futuramente inferir o tipo com base no caminho do arquivo
def load_dataset_from_file(
    file_path: str, file_type: str = "csv", **kwargs
) -> pd.DataFrame:
    try:
        logger.info(f"Loading dataset from {file_path} with type {file_type}")
        readers = {
            "csv": pd.read_csv,
            "excel": pd.read_excel,
            "json": pd.read_json,
            "parquet": pd.read_parquet,
            "pickle": pd.read_pickle,
            "sql": pd.read_sql,
        }

        assert file_type.lower() in readers, (
            f"Unsupported file type. Supported types: {', '.join(readers.keys())}"
        )

        df = readers[file_type.lower()](file_path, **kwargs)
        logger.info(f"Successfully loaded dataset with shape {df.shape}")
        return df
    except AssertionError as ae:
        logger.error(str(ae))
        raise
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise


def save_dataset_to_file(
    df: pd.DataFrame, file_path: str, file_type: str = "csv"
) -> None:
    try:
        logger.info(f"Saving dataset to {file_path} with type {file_type}")
        writers = {
            "csv": df.to_csv,
            "excel": df.to_excel,
            "json": df.to_json,
            "parquet": df.to_parquet,
            "pickle": df.to_pickle,
        }
        assert file_type.lower() in writers, (
            f"Unsupported file type. Supported types: {', '.join(writers.keys())}"
        )

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        writers[file_type.lower()](file_path, index=False)
        logger.info(f"Successfully saved dataset with shape {df.shape}")
    except AssertionError as ae:
        logger.error(str(ae))
        raise
    except Exception as e:
        logger.error(f"Error saving dataset: {str(e)}")
        raise


def load_dataset_from_kaggle(dataset_address: str, file_name: str) -> pd.DataFrame:
    try:
        logger.info(
            f"Loading dataset directly from Kaggle: {dataset_address}/{file_name}"
        )
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            dataset_address,
            file_name,
        )
        logger.info("Successfully loaded Kaggle dataset")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset from Kaggle: {str(e)}")
        raise


# TODO: Uma função main() pode ser criada para gerenciar as outras funções de forma a automatizar o download ou carregamento de um ou mais kaggle datasets.
