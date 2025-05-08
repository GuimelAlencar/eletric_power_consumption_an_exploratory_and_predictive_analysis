import pandas as pd
from pathlib import Path

DATA_RAW_PATH = Path("data/raw")
DATA_PROCESSED_PATH = Path("data/processed")

def process_data(input_file: Path, output_file: Path) -> None:
    """Agrega dados temporais e aplica transformações."""
    df = pd.read_parquet(input_file)
    
    # Exemplo: Agregação por hora
    df["datetime"] = pd.to_datetime(df["datetime"])
    df_processed = df.resample("h", on="datetime").mean()
    
    # Salva resultado
    df_processed.to_parquet(output_file)