import pandas as pd
from pathlib import Path
import pandera as pa  # Para validação de schemas
from typing import Dict

DATA_RAW_PATH = Path("data/raw")
DATA_EXTERNAL_PATH = Path("data/external")

# Esquema de Validação (exemplo)
schema = pa.DataFrameSchema({
    "datetime": pa.Column(pa.DateTime),
    "consumption": pa.Column(float, checks=pa.Check.ge(0)),
    "zone": pa.Column(str, checks=pa.Check.isin(["north", "south"]))
})

def validate_data(input_file: Path, schema: pa.DataFrameSchema, external_checks: Dict) -> bool:
    """
    Valida dados brutos contra schema e dados externos.
    Args:
        external_checks: Dicionário com métricas externas (ex: {"max_consumption": 1000}).
    """
    df = pd.read_parquet(input_file)
    
    # Validação de Schema
    try:
        schema.validate(df)
    except pa.errors.SchemaError as e:
        logging.error(f"Erro de schema: {str(e)}")
        return False
    
    # Validação de Regras de Negócio (ex: consumo máximo)
    if (df["consumption"] > external_checks["max_consumption"]).any():
        logging.error("Consumo excede valor máximo externo.")
        return False
    
    return True


{
    """
    1. Shape_validation: 
    Valida se a forma do dataframe corresponde com o esperado, a função deve implementar expressões lógicas complexas, como por exemplo, para 'shape': (x, y):
    condicao_x = lambda x: x > 1000 or x < 200 or (500 < x < 800)
    condicao_y = lambda y: y > 1000 or y < 200 or (500 < y < 800)
    }
    """

    'shape': (1000, 15),

    """
    2. Column_types_validation: Valida se os tipos de dados das colunas correspondem com o esperado
    A função vai validar o dicionário de colunas:tipos de forma simples:
    Para cada coluna do dataframe, a função vai verificar se o tipo de dado é o esperado
    A função deve retornar um erro caso uma das condições acima seja descumprida.
    Caso ocorra um erro de validação, a função vai retornar a coluna, o tipo esperado ou não esperado e o tipo encontrado em formatode erro.
    """

    'dtypes': {'age': 'int64', 'income': 'float64', ...},

    """
    3. Samples_validation:
    A função vai validar o conteúdo de "samples" observando condições como:
    Coluna x deve começar com y valor ou não pode alcançar valor y
    Colunas x e y não devem ter valores iguais
    Coluna x não pode ser menor do quê coluna y
    """
    'samples': {
        'head': [{'age': 25, 'income': 45000.0}, ...],
        'middle': [{'age': 25, 'income': 45000.0}, ...],
        'tail': [{'age': 58, 'income': 82000.0}, ...]
    },

    """
    3. Description_validatin:
    A função deve validar o conteúdo de "describe" observando as condições:
    """

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
