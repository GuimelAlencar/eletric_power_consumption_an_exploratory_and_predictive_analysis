# importer.py
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import gc

def download_dataset(
    dataset_name: str,
    csv_file_name: str,
    target_dir: str = "data",
    parquet_file_name: str = None
) -> None:
    """
    Baixa um dataset do Kaggle, converte para Parquet e limpa arquivos/memória.

    Args:
        dataset_name (str): Nome do dataset no formato "usuario/dataset".
        csv_file_name (str): Nome do arquivo CSV a ser baixado.
        target_dir (str): Diretório de destino (padrão: "data").
        parquet_file_name (str, opcional): Nome do arquivo Parquet. Se não definido,
            usa o mesmo nome do CSV com extensão .parquet.
    """
    os.makedirs(target_dir, exist_ok=True)
    api = KaggleApi()
    api.authenticate()

    # Parquet name
    if not parquet_file_name:
        parquet_file_name = csv_file_name.replace(".csv", ".parquet")

    # Download and unzip the dataset
    api.dataset_download_file(
        dataset=dataset_name,
        file_name=csv_file_name,
        path=target_dir,
        quiet=True
    )
    zip_path = os.path.join(target_dir, f"{csv_file_name}.zip")
    if os.path.exists(zip_path):
        os.system(f"unzip -o {zip_path} -d {target_dir} && rm {zip_path}")

    # CSV to Parquet
    csv_path = os.path.join(target_dir, csv_file_name)
    parquet_path = os.path.join(target_dir, parquet_file_name)
    
    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, engine="pyarrow")
    os.remove(csv_path)

    # Limpeza de memória
    del df
    gc.collect()

    print(f"Arquivo {parquet_path} salvo com sucesso!")

    """
    # Exemplo de uso:

    def load_data(parquet_path: str) -> pd.DataFrame:
        # Carrega um arquivo Parquet para um DataFrame do Pandas.
        return pd.read_parquet(parquet_path)

    # visualizando:
    df = load_data("data/heart.parquet")
    print(df.head())
    """