import json
import csv
import os
from datetime import datetime

class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.record_id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __repr__(self):
        return f"FinanceRecord(id={self.record_id}, amount={self.amount}, category='{self.category}', date='{self.date}', description='{self.description}')"

class FinanceManager:
    def __init__(self, filename='finance\\finance.json'):
        self.filename = os.path.join(os.getcwd(), filename)
        self.records = self.load_records()

    def load_records(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return [FinanceRecord(**data) for data in json.load(f)]
        return []

    def save_records(self):
        with open(self.filename, 'w') as f:
            json.dump([{
                'record_id': record.record_id,
                'amount': record.amount,
                'category': record.category,
                'date': record.date,
                'description': record.description
            } for record in self.records], f)

    def add_record(self, amount, category, date, description):
        record_id = len(self.records) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(new_record)
        self.save_records()

    def view_records(self, category=None, date=None):
        filtered_records = self.records
        if category:
            filtered_records = [record for record in filtered_records if record.category.lower() == category.lower()]
        if date:
            filtered_records = [record for record in filtered_records if record.date == date]
        
        for record in filtered_records:
            print(record)

    def generate_report(self, start_date=None, end_date=None):
        report_records = []
        
        for record in self.records:
            record_date = datetime.strptime(record.date, "%d-%m-%Y")
            if (start_date and record_date < start_date) or (end_date and record_date > end_date):
                continue
            report_records.append(record)

        total_income = sum(r.amount for r in report_records if r.amount > 0)
        total_expense = sum(r.amount for r in report_records if r.amount < 0)
        
        print(f"Общий доход: {total_income:.2f}")
        print(f"Общие расходы: {total_expense:.2f}")
    
    def export_to_csv(self, csv_filename='finance\\finance.csv'):
        with open(csv_filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description'])
            for record in self.records:
                writer.writerow([record.record_id, record.amount, record.category, record.date, record.description])

    def import_from_csv(self, csv_filename='finance\\finance.csv'):
        with open(csv_filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                amount = float(row['Amount'])
                category = row['Category']
                date = row['Date']
                description = row['Description']
                self.add_record(amount, category, date, description)

    def calculate_balance(self):
        return sum(record.amount for record in self.records)

    def main(self):
        while True:
            print("\nВыберите опцию:")
            print("1. Добавить новую финансовую запись")
            print("2. Просмотреть все записи")
            print("3. Генерировать отчет")
            print("4. Экспортировать записи в CSV")
            print("5. Импортировать записи из CSV")
            print("6. Посчитать общий баланс")
            print("7. Выход")

            choice = input("Введите номер опции: ")

            if choice == '1':
                amount = float(input("Введите сумму операции (положительное для дохода и отрицательное для расхода): "))
                category = input("Введите категорию операции: ")
                date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
                description = input("Введите описание операции: ")
                self.add_record(amount, category, date, description)
                print("Финансовая запись добавлена.")
            
            elif choice == '2':
                category_filter = input("Введите категорию для фильтрации (или оставьте пустым): ")
                date_filter = input("Введите дату для фильтрации (ДД-ММ-ГГГГ или оставьте пустым): ")
                self.view_records(category_filter or None, date_filter or None)
            
            elif choice == '3':
                start_date_str = input("Введите начальную дату (ДД-ММ-ГГГГ или оставьте пустым): ")
                end_date_str = input("Введите конечную дату (ДД-ММ-ГГГГ или оставьте пустым): ")
                
                start_date = datetime.strptime(start_date_str, "%d-%m-%Y") if start_date_str else None
                end_date = datetime.strptime(end_date_str, "%d-%m-%Y") if end_date_str else None
                
                self.generate_report(start_date=start_date, end_date=end_date)
            
            elif choice == '4':
                self.export_to_csv()
                print("Финансовые записи экспортированы в finance.csv.")
            
            elif choice == '5':
                self.import_from_csv()
                print("Финансовые записи импортированы из finance.csv.")
            
            elif choice == '6':
                balance = self.calculate_balance()
                print(f"Общий баланс: {balance:.2f}")
            
            elif choice == '7':
                print("Выход из программы.")
                break
            
            else:
                print("Некорректный ввод. Пожалуйста, выберите номер опции от 1 до 7.")

if __name__ == '__main__':
    manager = FinanceManager()
    manager.main()