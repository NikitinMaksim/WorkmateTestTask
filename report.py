from typing import List, Dict, Any, Optional, Callable, Tuple
from employee import Employee

class ReportGenerator:
    """Класс для генерации отчетов в разных форматах"""
    @staticmethod
    def generate_payout_report(employees: List[Employee], format: str = 'text') -> Any:
        """
        Генерирует отчет о выплатах в текстовом или JSON формате
        
        Args:
            employees: Список сотрудников
            format: Формат вывода ('text' или 'json')
            
        Returns:
            Отчет в выбранном формате
        """
        departments: Dict[str, Dict[str, Any]] = {}
        
        # Группируем сотрудников по отделам
        for emp in employees:
            if emp.department not in departments:
                departments[emp.department] = {
                    'employees': [],  # Список сотрудников отдела
                    'total_hours': 0,  # Суммарные часы
                    'total_payout': 0  # Суммарные выплаты
                }
            
            # Данные сотрудника для отчета
            employee_data = {
                'name': emp.name,
                'hours_worked': emp.hours_worked,
                'hourly_rate': emp.hourly_rate,
                'payout': emp.payout
            }
            
            departments[emp.department]['employees'].append(employee_data)
            departments[emp.department]['total_hours'] += emp.hours_worked
            departments[emp.department]['total_payout'] += emp.payout
        
        if format == 'json':
            # Формируем структуру для JSON
            return {
                'departments': departments,
                'total': {
                    'hours': sum(emp.hours_worked for emp in employees),
                    'payout': sum(emp.payout for emp in employees)
                }
            }
        else:
            # Текстовый формат отчета
            report_lines = []
            # Шапка таблицы
            report_lines.append(f"{'':15}{'name':<30}{'hours':<10}{'rate':<10}{'payout':<10}")
            
            # Добавляем данные по каждому отделу
            for dept in sorted(departments.keys()):
                report_lines.append(dept)  # Название отдела
                
                # Сотрудники отдела (сортировка по имени)
                for emp in sorted(departments[dept]['employees'], key=lambda x: x['name']):
                    report_lines.append(
                        "-------------  " +  # Разделитель
                        f"{emp['name']:<30}" +  # Имя
                        f"{emp['hours_worked']:<10.0f}" +  # Часы
                        f"{emp['hourly_rate']:<10.0f}" +  # Ставка
                        f"${emp['payout']:<10.0f}"  # Выплата
                    )
                
                # Итоги по отделу
                report_lines.append(
                    f"{'':45}" +  # Отступ
                    f"{departments[dept]['total_hours']:<10.0f}" +  # Часы
                    f"{'':<10}" +  # Пусто для ставки
                    f"${departments[dept]['total_payout']:<10.0f}"  # Выплата
                )
                report_lines.append("")  # Пустая строка
            
            return "\n".join(report_lines)  # Объединяем строки


class ReportFactory:
    """Фабрика для создания отчетов разных типов"""
    @staticmethod
    def get_report_generator(report_type: str) -> Optional[Callable[[List[Employee], str], Any]]:
        """Возвращает генератор отчетов по типу"""
        reports = {
            'payout': ReportGenerator.generate_payout_report  # Пока только отчет по выплатам
        }
        return reports.get(report_type)