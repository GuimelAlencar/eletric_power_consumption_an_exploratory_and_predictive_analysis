# tests/test_importer.py
import pytest
from unittest import mock
import os
import pandas as pd
from src.data_pipeline.importer import download_dataset
import logging

# Configuração de logging para testes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def setup_teardown():
    # Setup
    test_dir = "data/tests"
    yield test_dir
    # Teardown
    if os.path.exists(test_dir):
        for f in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, f))
        os.rmdir(test_dir)

@mock.patch('importer.KaggleApi')
def test_download_dataset_success(mock_kaggle, setup_teardown, caplog):
    """Testa download bem-sucedido com conversão para Parquet"""
    # Configurar mocks
    mock_api = mock.MagicMock()
    mock_kaggle.return_value = mock_api
    
    # Executar
    download_dataset(
        dataset_name="user/dataset",
        csv_file_name="data.csv",
        target_dir=setup_teardown
    )

    # Verificar
    expected_files = [
        os.path.join(setup_teardown, "data.parquet")
    ]
    
    # Verifica criação de arquivos
    for f in expected_files:
        assert os.path.exists(f), f"Arquivo {f} não foi criado"
    
    # Verifica limpeza
    assert not os.path.exists(os.path.join(setup_teardown, "data.csv"))
    assert not os.path.exists(os.path.join(setup_teardown, "data.csv.zip"))
    
    # Verifica logs
    assert "salvo com sucesso" in caplog.text

@mock.patch('importer.KaggleApi')
def test_download_dataset_invalid_credentials(mock_kaggle, setup_teardown, caplog):
    """Testa tratamento de credenciais inválidas"""
    # Configurar mock para levantar exceção
    mock_api = mock.MagicMock()
    mock_api.authenticate.side_effect = Exception("Invalid credentials")
    mock_kaggle.return_value = mock_api

    # Executar e verificar exceção
    with pytest.raises(Exception, match="Invalid credentials"):
        download_dataset(
            dataset_name="user/dataset",
            csv_file_name="data.csv",
            target_dir=setup_teardown
        )
    
    # Verificar logs
    assert "Falha na autenticação" in caplog.text
    assert "Invalid credentials" in caplog.text

@mock.patch('importer.KaggleApi')
def test_download_dataset_missing_file(mock_kaggle, setup_teardown, caplog):
    """Testa tratamento de arquivo CSV ausente"""
    # Configurar mock
    mock_api = mock.MagicMock()
    mock_kaggle.return_value = mock_api
    
    # Forçar erro no download
    mock_api.dataset_download_file.side_effect = Exception("File not found")

    # Executar e verificar exceção
    with pytest.raises(Exception, match="File not found"):
        download_dataset(
            dataset_name="user/dataset",
            csv_file_name="invalid.csv",
            target_dir=setup_teardown
        )
    
    # Verificar logs
    assert "Falha no download do dataset" in caplog.text

@mock.patch('src.data_pipeline.importer.KaggleApi')  # Caminho absoluto do módulo
def test_parquet_conversion_integrity(mock_kaggle, setup_teardown):
    """Testa integridade do arquivo Parquet gerado"""
    # Configurar mock para evitar chamadas reais à API
    mock_api = mock.MagicMock()
    mock_kaggle.return_value = mock_api
    
    # Criar arquivo CSV de teste
    test_csv = os.path.join(setup_teardown, "test.csv")
    pd.DataFrame({'col1': [1,2], 'col2': ['a','b']}).to_csv(test_csv, index=False)
    
    # Executar conversão
    download_dataset(
        dataset_name="user/dataset",
        csv_file_name="test.csv",
        target_dir=setup_teardown,
        parquet_file_name="test.parquet"
    )
    
    # Verificar integridade do Parquet
    parquet_path = os.path.join(setup_teardown, "test.parquet")
    df = pd.read_parquet(parquet_path)
    
    assert not df.empty, "DataFrame Parquet está vazio"
    assert list(df.columns) == ['col1', 'col2'], "Colunas incorretas"