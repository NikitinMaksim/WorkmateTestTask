import pytest
from unittest.mock import patch, mock_open
from main import parse_args, main

# Тестовые данные
TEST_CSV_DATA = """id,name,department,hours_worked,rate
1,John Doe,Engineering,160,50
2,Jane Smith,Marketing,150,40"""

@pytest.fixture
def mock_csv_file(tmp_path):
    """Фикстура с тестовым CSV файлом"""
    file = tmp_path / "test.csv"
    file.write_text(TEST_CSV_DATA)
    return str(file)

def test_parse_args():
    """Тест парсинга аргументов"""
    args = parse_args(['file1.csv', 'file2.csv', '--report', 'payout'])
    assert args.files == ['file1.csv', 'file2.csv']
    assert args.report == 'payout'
    assert args.format == 'text'

def test_main_with_valid_file(mock_csv_file, capsys):
    """Тест основной функции с валидным файлом"""
    with patch('sys.argv', ['main.py', mock_csv_file, '--report', 'payout']):
        main()
    
    captured = capsys.readouterr()
    assert "John Doe" in captured.out
    assert "Jane Smith" in captured.out

def test_main_with_missing_file(capsys):
    """Тест обработки отсутствующего файла"""
    with patch('sys.argv', ['main.py', 'nonexistent.csv', '--report', 'payout']):
        with pytest.raises(SystemExit):
            main()
    
    captured = capsys.readouterr()
    assert "Warning: File not found" in captured.err

def test_main_json_output(mock_csv_file, capsys):
    """Тест JSON вывода"""
    with patch('sys.argv', ['main.py', mock_csv_file, '--report', 'payout', '--format', 'json']):
        main()
    
    captured = capsys.readouterr()
    assert '"name": "John Doe"' in captured.out
    assert '"Engineering"' in captured.out

def test_main_with_empty_file(tmp_path, capsys):
    """Тест с пустым файлом"""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("id,name\n")
    
    with patch('sys.argv', ['main.py', str(empty_file), '--report', 'payout']):
        with pytest.raises(SystemExit):
            main()
    
    captured = capsys.readouterr()
    assert "Error: No employee data found" in captured.err