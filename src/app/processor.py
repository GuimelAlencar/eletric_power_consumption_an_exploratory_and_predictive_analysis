import pandas as pd
import numpy as np

from importer import load_dataset_from_kaggle, save_dataset_to_file

from validator import validate_dataframe_by_time_range

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def aggregate_data_by_time_frequency(
    df: pd.DataFrame,
    freq: str,
    index: str = "Datetime",
    agg_schema: dict = {
        "Temperature": "mean",
        "Humidity": "mean",
        "WindSpeed": "mean",
        "GeneralDiffuseFlows": "mean",
        "DiffuseFlows": "mean",
        "PowerConsumption_Zone1": ["sum", "mean"],
        "PowerConsumption_Zone2": ["sum", "mean"],
        "PowerConsumption_Zone3": ["sum", "mean"],
    },
    naming_schema: list = [
        "Temperature",
        "Humidity",
        "WindSpeed",
        "GeneralDiffuseFlows",
        "DiffuseFlows",
        "TotalPowerConsumption_Zone1",
        "AveragePowerConsumption_Zone1",
        "TotalPowerConsumption_Zone2",
        "AveragePowerConsumption_Zone2",
        "TotalPowerConsumption_Zone3",
        "AveragePowerConsumption_Zone3",
    ],
) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy.set_index(index, inplace=True)

    df_agg = df_copy.resample(freq).agg(agg_schema)
    df_agg.columns = naming_schema
    df_agg.reset_index(inplace=True)

    return df_agg


def add_shift_column(df):
    validate_dataframe_by_time_range(df, "Datetime", pd.Timedelta(hours=6))
    hour = df["Datetime"].dt.hour
    conditions = [
        (hour >= 6) & (hour < 12),
        (hour >= 12) & (hour < 18),
        (hour >= 18) & (hour < 24),
        (hour >= 0) & (hour < 6),
    ]
    choices = [1, 2, 3, 4]
    df["turno"] = np.select(conditions, choices, default=-1)
    return df


def add_weekday_column(df):
    validate_dataframe_by_time_range(df, "Datetime", pd.Timedelta(days=1))
    df["dia_semana"] = df["Datetime"].dt.dayofweek + 1
    return df


holidays = [
    "2017-01-11",
    "2017-05-01",
    "2017-06-26",
    "2017-08-14",
    "2017-08-21",
    "2017-09-01",
    "2017-09-21",
    "2017-11-06",
    "2017-12-01",
]
holidays = pd.to_datetime(holidays).date


def add_utility_column(df):
    validate_dataframe_by_time_range(df, "Datetime", pd.Timedelta(days=1))
    if "dia_semana" not in df.columns:
        df = add_weekday_column(df)

    def classify_day(row):
        date = row["Datetime"].date()
        if date in holidays:
            return 3
        elif row["dia_semana"] >= 6:
            return 2
        else:
            return 1

    df["utilidade"] = df.apply(classify_day, axis=1)
    return df


def add_season_column(df):
    validate_dataframe_by_time_range(df, "Datetime", pd.Timedelta(days=90))

    month = df["Datetime"].dt.month

    conditions = [
        month.isin([3, 4, 5]),  # Primavera (1)
        month.isin([6, 7, 8]),  # Verão (2)
        month.isin([9, 10, 11]),  # Outono (3)
        month.isin([12, 1, 2]),  # Inverno (4)
    ]
    choices = [1, 2, 3, 4]

    df["estacao"] = np.select(conditions, choices, default=0)
    return df


def process(df):
    df = add_shift_column(df)
    df = add_weekday_column(df)
    df = add_utility_column(df)
    df = add_season_column(df)
    return df


def process_dataframe(
    df: pd.DataFrame, freq: str = "H", index: str = "Datetime"
) -> pd.DataFrame:
    try:
        logger.info("Converting Datetime column to datetime type")
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        logger.info(f'Aggregating data by "{freq}" using column "{index}" as index')
        df = aggregate_data_by_time_frequency(df, freq, index)
        logger.info("Data successfully aggregated")
        logger.info("Processing data")
        process(df)
        logger.info("Data successfully processed")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset from Kaggle: {str(e)}")
        raise


# TODO: Uma função main() pode ser criada para gerenciar as outras funções de forma a automatizar o processamento e criação de novos datasets.
