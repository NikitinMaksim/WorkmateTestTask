import argparse
import sys
from employee import Employee, CSVReader
from report import ReportFactory

def parse_args(args=None):
    """Вынесена логика парсинга аргументов для тестирования"""
    parser = argparse.ArgumentParser(description='Employee report generator')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                      help='CSV files with employee data')
    parser.add_argument('--report', type=str, required=True,
                      help='Type of report to generate')
    parser.add_argument('--format', type=str, default='text',
                      choices=['text', 'json'],
                      help='Output format (text or json)')
    return parser.parse_args(args)

def main(args=None):
    """Основная логика, принимает аргументы для тестирования"""
    args = parse_args(args)
    
    employees = []
    for file_path in args.files:
        try:
            data = CSVReader.read_file(file_path)
            employees.extend([Employee(row) for row in data])
        except FileNotFoundError:
            print(f"Warning: File not found '{file_path}', skipping", file=sys.stderr)
    
    if not employees:
        print("Error: No employee data found", file=sys.stderr)
        sys.exit(1)
    
    report = ReportFactory.get_report_generator(args.report)(employees, args.format)
    
    if args.format == 'json':
        import json
        print(json.dumps(report, indent=2))
    else:
        print(report)

if __name__ == '__main__':
    main()