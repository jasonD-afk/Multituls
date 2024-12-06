import datetime
import json
import csv
import os

class Notes:
    def __init__(self, title, content, note_id, date=None):
        self.title = title
        self.content = content
        self.note_id = note_id
        self.date = date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __repr__(self):
        return f"Note(id={self.note_id}, title={self.title}, content={self.content}, timestamp={self.date})"

class NoteManager:
    def __init__(self, filename='notes\\notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def add_note(self, title, content):
        note_id = len(self.notes) + 1 
        new_note = Notes(title, content, note_id)
        self.notes.append(new_note)
        self.save_notes()
    
    def create_new_note(self):
        title = input("Введите название заметки: ")
        content = input("Введите описание заметки: ")
        self.add_note(title, content)
    
    def save_notes(self):
        with open(self.filename, 'w') as f:
            json.dump([{'title': n.title, 'content': n.content, 'date': n.date} for n in self.notes], f)

    def load_notes(self):
        try:
            with open(self.filename, 'r') as f:
                return [Notes(**n) for n in json.load(f)]
        except FileNotFoundError:
            return []
    
    def view_note(self):
        for note in self.notes:
            print(f"{note.note_id}: {note.title} (Дата: {note.date})")
    
    def view_note_details(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                print(f"Заголовок: {note.title}\nСодержимое: {note.content}\nДата: {note.date}")
                return
        print("Заметка не найдена.")
        
    def edit_note(self, note_id, new_title=None, new_content=None):
        for note in self.notes:
            if note.note_id == note_id:
                if new_title is not None:
                    note.title = new_title
                if new_content is not None:
                    note.content = new_content
                note.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                return
        print("Такой заметки нет")

    def delete(self, note_id):
        note_found = False
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note) 
                note_found = True  
                break 
        if note_found:
            self.save_notes()
            print(f"Заметка с ID {note_id} была успешно удалена.")
        else:
            print(f"Заметка с ID {note_id} не найдена.")
    
    def export_csv(self, csv_filename='notes\\notes.csv'):
        with open(csv_filename,"w", newline='') as f:
            write = csv.writer(f)
            write.writerow(['ID', 'Title', 'Content', 'Date'])
            for note in self.notes:
                write.writerow([note.note_id, note.title, note.content, note.date])

    def import_csv(self,csv_filename='notes\\notes.csv'):
        with open(csv_filename, 'r') as f:
            read = csv.DictReader(f)
            for row in read:
                self.add_note(row['Title'], row['Content'])

    def main(self):
        while True:
            print("\nВыберите опцию:")
            print("1. Создать новую заметку")
            print("2. Просмотреть все заметки")
            print("3. Просмотреть детали заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Экспортировать заметки в CSV")
            print("7. Импортировать заметки из CSV")
            print("8. Выход")

            choice = input("Введите номер опции: ")

            if choice == '1':
                self.create_new_note()
            elif choice == '2':
                self.view_note()
            elif choice == '3':
                note_id = int(input("Введите ID заметки для просмотра: "))
                self.view_note_details(note_id)
            elif choice == '4':
                note_id = int(input("Введите ID заметки для редактирования: "))
                new_title = input("Введите новый заголовок (или оставьте пустым): ")
                new_content = input("Введите новое содержимое (или оставьте пустым): ")
                self.edit_note(note_id, new_title or None, new_content or None)
            elif choice == '5':
                note_id = int(input("Введите ID заметки для удаления: "))
                self.delete(note_id)
            elif choice == '6':
                self.export_csv()
                print("Заметки экспортированы в notes.csv.")
            elif choice == '7':
                self.import_csv()
                print("Заметки импортированы из notes.csv.")
            elif choice == '8':
                break
            else:
                print("Некорректный ввод.")

if __name__ == '__main__':
    manager = NoteManager()
    manager.main()