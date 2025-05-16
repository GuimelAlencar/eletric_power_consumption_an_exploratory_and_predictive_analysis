import pandas as pd

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def is_constant_time_interval(df: pd.DataFrame, datetime_col: str) -> bool:
    time_diffs = df[datetime_col].diff().dropna()
    return len(time_diffs.unique()) == 1


def validate_dataframe_by_time_range(
    df: pd.DataFrame, datetime_col: str, max_interval: pd.Timedelta
) -> bool:
    if datetime_col not in df.columns:
        logging.error(f"Column {datetime_col} not found in dataframe")
        # raise ValueError(f"Column {datetime_col} not found in dataframe")

    if not pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
        logging.error(f"Column {datetime_col} must be datetime type")
        # raise ValueError(f"Column {datetime_col} must be datetime type")

    if not is_constant_time_interval(df, datetime_col):
        logging.error("Time intervals between records must be constant")
        # raise ValueError("Time intervals between records must be constant")

    time_diff = df[datetime_col].diff().dropna().iloc[0]
    if time_diff > max_interval:
        logging.error(f"Time interval ({time_diff}) exceeds maximum allowed ({max_interval})")
        # raise ValueError(
        #     f"Time interval ({time_diff}) exceeds maximum allowed ({max_interval})"
        # )

    return True

# TODO: Esse script precisa ser atualizado com mais ferramentas, de forma a conter formas avançadas de validação dos dados expostos.