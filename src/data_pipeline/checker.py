# checker.py
import pandas as pd

def check_dataset(df: pd.DataFrame, sample_size: int = 3) -> dict:
    """
    Gera um relatório de análise do dataset.

    Parâmetros:
    - df: DataFrame a ser analisado
    - sample_size: Número de amostras a exibir (head/tail)

    Retorna:
    - Dicionário com métricas, estrutura e problemas identificados
    """
    
    report = {}

    # 1. Metadados básicos
    report["shape"] = df.shape
    report["dtypes"] = df.dtypes.astype(str).to_dict()
    
    # 2. Amostras
    report["samples"] = {
        # TODO: sample_size não deve ser um único número, mais sim um dicionário que define o tamanho de cada parte da amostra, da head, do middle e da tail

        "head": df.head(sample_size).to_dict(orient="records"),
        # "body": Take a sample of sample_size's rows from the middle of the dataframe   
        "tail": df.tail(sample_size).to_dict(orient="records")
    }
    
    # 3. Análise descritiva
    report["describe"] = df.describe(include="all").to_dict()
    
    # 4. Valores ausentes
    missing_values = df.isna().sum()
    report["missing_values"] = {
        "total": missing_values.sum(),
        "por_coluna": missing_values[missing_values > 0].to_dict()
    }
    
    # 5. Duplicatas
    report["duplicates"] = {
        "total": df.duplicated().sum(),
        "exemplos": df[df.duplicated(keep=False)].sample(min(2, df.duplicated().sum())).to_dict(orient="records") if df.duplicated().sum() > 0 else None
    }
    
    # 6. Outliers (método IQR)
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
                "percentual": f"{(outliers_count/len(df))*100:.2f}%",
                "limites": [float(lower_bound), float(upper_bound)]
            }
    
    report["outliers"] = outliers if outliers else "Nenhum outlier significativo detectado"

    return report

    """ Exemplo de uso:
    from checker import check_dataset, print_report

    # Carregar dados
    df = load_data("data/dados.parquet")

    # Gerar relatório
    report = check_dataset(df)

    # Visualizar resultados
    print_report(report)
    """

    """ Exemplo de saída:
    {
        'shape': (1000, 15),
        'dtypes': {'age': 'int64', 'income': 'float64', ...},
        'samples': {
            'head': [{'age': 25, 'income': 45000.0}, ...],
            'tail': [{'age': 58, 'income': 82000.0}, ...]
        },
        'describe': {
            'age': {'count': 1000.0, 'mean': 42.5, ...},
            'income': {'count': 950.0, 'mean': 65000.0, ...}
        },
        'missing_values': {
            'total': 50,
            'por_coluna': {'income': 50}
        },
        'duplicates': {
            'total': 12,
            'exemplos': [{'age': 35, 'income': null}, ...]
        },
        'outliers': {
            'income': {
                'outliers': 15,
                'percentual': '1.50%',
                'limites': [12000.0, 98000.0]
            }
        }
    }   
    """

# Função auxiliar para imprimir o relatório formatado
def print_report(report: dict) -> None:
    """Formata a saída do relatório para melhor legibilidade."""
    from pprint import pprint
    pprint(report, depth=2, compact=True)