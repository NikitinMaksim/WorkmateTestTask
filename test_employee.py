import pytest
from employee import Employee, CSVReader

def test_employee_creation():
    emp = Employee({'name': 'Test', 'hours_worked': '160', 'rate': '50'})
    assert emp.payout == 8000

def test_csv_reader(tmp_path):
    csv_data = "name,hours,rate\nTest,160,50"
    file = tmp_path / "test.csv"
    file.write_text(csv_data)
    
    data = CSVReader.read_file(str(file))
    assert len(data) == 1
    assert data[0]['name'] == 'Test'