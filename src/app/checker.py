import pandas as pd


def check_dataset(df: pd.DataFrame, sample_size: int = 3) -> dict:
    report = {}

    report["shape"] = df.shape
    report["dtypes"] = df.dtypes.astype(str).to_dict()

    if isinstance(sample_size, int):
        sample_size = [sample_size] * 3

    if len(sample_size) != 3:
        raise ValueError(
            "sample_size must be either an integer or a list of 3 integers"
        )

    report["samples"] = {
        "head": df.head(sample_size[0]).to_dict(orient="records"),
        "body": df.iloc[
            len(df) // 2 - sample_size[1] // 2 : len(df) // 2 + sample_size[1] // 2
        ].to_dict(orient="records"),
        "tail": df.tail(sample_size[2]).to_dict(orient="records"),
    }

    report["describe"] = df.describe(include="all").to_dict()

    missing_values = df.isna().sum()
    report["missing_values"] = {
        "total": missing_values.sum(),
        "by_column": missing_values[missing_values > 0].to_dict(),
    }

    report["duplicates"] = {
        "total": df.duplicated().sum(),
        "examples": df[df.duplicated(keep=False)]
        .sample(min(2, df.duplicated().sum()))
        .to_dict(orient="records")
        if df.duplicated().sum() > 0
        else None,
    }

    numeric_cols = df.select_dtypes(include=["number"]).columns
    outliers = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()

        if outliers_count > 0:
            outliers[col] = {
                "outliers": outliers_count,
                "percent": f"{(outliers_count / len(df)) * 100:.2f}%",
                "limits": [float(lower_bound), float(upper_bound)],
            }

    report["outliers"] = (
        outliers if outliers else "Nenhum outlier significativo detectado"
    )

    return report

    """ Example:
    from checker import check_dataset

    report = check_dataset(df)

    print_report(report)
    """

    """
    {
        'shape': (1000, 15),
        'dtypes': {'age': 'int64', 'income': 'float64', ...},
        'samples': {
            'head': [{'age': 25, 'income': 45000.0}, ...],
            'middle': [{'age': 25, 'income': 45000.0}, ...],
            'tail': [{'age': 58, 'income': 82000.0}, ...]
        },
        'describe': {
            'age': {'count': 1000.0, 'mean': 42.5, ...},
            'income': {'count': 950.0, 'mean': 65000.0, ...}
        },
        'missing_values': {
            'total': 50,
            'by_column': {'income': 50}
        },
        'duplicates': {
            'total': 12,
            'examples': [{'age': 35, 'income': null}, ...]
        },
        'outliers': {
            'income': {
                'outliers': 15,
                'percent': '1.50%',
                'limits': [12000.0, 98000.0]
            }
        }
    }   
    """


def print_report(report: dict) -> None:
    from pprint import pprint

    pprint(report, depth=2, compact=True)


# TODO: Uma função main() pode ser criada para gerenciar as outras funções de forma a automatizar a geração de relatórios sobre os datasets informados.
