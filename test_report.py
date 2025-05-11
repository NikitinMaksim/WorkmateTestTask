from report import ReportGenerator
from employee import Employee

def test_payout_report():
    employees = [
        Employee({'name': 'Test', 'department': 'Dev', 'hours_worked': '160', 'rate': '50'})
    ]
    report = ReportGenerator.generate_payout_report(employees)
    assert 'Test' in report
    assert '160' in report