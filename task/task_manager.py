import datetime
import json
import csv
import os

class Tasks:
    def __init__(self, task_id, task_title, description, priority, done, due_date=None):
        self.task_title = task_title
        self.description = description
        self.task_id = task_id
        self.done = done
        self.priority = priority
        self.due_date = due_date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __repr__(self):
        return f"task(id={self.task_id}, title={self.task_title}, description={self.description}, priority={self.priority}, done_task={self.done}, timestamp={self.due_date})"

class TaskManager:
    def __init__(self, filename='task\\task.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                return [Tasks(**n) for n in json.load(f)]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([{
                'task_id': n.task_id,
                'title': n.task_title,
                'description': n.description,
                'priority': n.priority,
                'done_task': n.done,
                'due_date': n.due_date
            } for n in self.tasks], f)

    def add_task(self, task_title, description, priority, done=False):
        task_id = len(self.tasks) + 1
        new_task = Tasks(task_id, task_title, description, priority, done)
        self.tasks.append(new_task)
        self.save_tasks()

    def create_task(self):
        task_title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Введите приоритет задачи («Высокий», «Средний», «Низкий»): ")
        
        while priority not in ["Высокий", "Средний", "Низкий"]:
            print('Вы неправильно ввели данные')
            priority = input("Введите приоритет задачи («Высокий», «Средний», «Низкий»): ")
        
        done = False
        due_date = input("Введите дату выполнения задачи (или оставьте пустым): ")
        
        self.add_task(task_title, description, priority, done)

    def view_tasks(self):
        for task in self.tasks:
            print(f"{task.task_id}: {task.task_title}, приоритет: {task.priority}, статус: {task.done}, (дедлайн: {task.due_date})")

    def view_task_details(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                print(f"Название задачи: {task.task_title}\nСодержимое: {task.description}\nСтатус: {task.done}")
                return
        print("Задача не найдена.")

    def edit_task(self, task_id, new_title=None, new_description=None, new_priority=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if new_title is not None:
                    task.task_title = new_title
                if new_description is not None:
                    task.description = new_description
                if new_priority is not None:
                    task.priority = new_priority
                self.save_tasks()
                return
        print("Такой задачи нет")

    def delete_task(self, task_id):
        task_found = False
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task) 
                task_found = True  
                break 
        if task_found:
            self.save_tasks()
            print(f"Задача с ID {task_id} была успешно удалена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")
    
    def export_to_csv(self, csv_filename='task\\tasks.csv'):
        with open(csv_filename,"w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Description', 'Priority', 'Status', 'Due Date'])
            for task in self.tasks:
                writer.writerow([task.task_id, task.task_title, task.description, task.priority, task.done, task.due_date])

    def import_from_csv(self,csv_filename='task\\tasks.csv'):
        with open(csv_filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_task(row['Title'], row['Description'], row['Priority'], row['Status'])

    def main(self):
        while True:
            print("\nВыберите опцию:")
            print("1. Создать новую задачу")
            print("2. Просмотр списка задач")
            print("3. Просмотреть детали задачи")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Экспортировать задачи в CSV")
            print("7. Импортировать задачи из CSV")
            print("8. Выход")

            choice = input("Введите номер опции: ")

            if choice == '1':
                self.create_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                task_id = int(input("Введите ID задачи для просмотра: "))
                self.view_task_details(task_id)
            elif choice == '4':
                task_id = int(input("Введите ID задачи для редактирования: "))
                new_title = input("Введите новый заголовок (или оставьте пустым): ")
                new_description = input("Введите новое содержимое (или оставьте пустым): ")
                new_priority = input("Введите новый приоритет (или оставьте пустым): ")
                self.edit_task(task_id, new_title or None, new_description or None, new_priority or None)
            elif choice == '5':
                task_id = int(input("Введите ID задачи для удаления: "))
                self.delete_task(task_id)
            elif choice == '6':
                self.export_to_csv()
                print("Задачи экспортированы в tasks.csv.")
            elif choice == '7':
                self.import_from_csv()
                print("Задачи импортированы из tasks.csv.")
            elif choice == '8':
                break
            else:
                print("Некорректный ввод.")

if __name__ == '__main__':
    manager = TaskManager()
    manager.main()