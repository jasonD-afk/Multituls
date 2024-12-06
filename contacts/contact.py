import json
import csv
import os

class Contact:
    def __init__(self, contact_id, name, phone=None, email=None):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Contact(id={self.contact_id}, name={self.name}, phone={self.phone}, email={self.email})"

class ContactManager:
    def __init__(self, filename='contacts\\contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return [Contact(**data) for data in json.load(f)]
        return []

    def save_contacts(self):
        with open(self.filename, 'w') as f:
            json.dump([{
                'contact_id': contact.contact_id,
                'name': contact.name,
                'phone': contact.phone,
                'email': contact.email
            } for contact in self.contacts], f)

    def add_contact(self, name, phone=None, email=None):
        contact_id = len(self.contacts) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()

    def search_contact(self, query):
        results = [contact for contact in self.contacts if query.lower() in contact.name.lower() or (contact.phone and query in contact.phone)]
        return results

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                if name is not None:
                    contact.name = name
                if phone is not None:
                    contact.phone = phone
                if email is not None:
                    contact.email = email
                self.save_contacts()
                return True
        return False

    def delete_contact(self, contact_id):
        self.contacts = [contact for contact in self.contacts if contact.contact_id != contact_id]
        self.save_contacts()

    def export_to_csv(self, csv_filename='contacts\\contacts.csv'):
        with open(csv_filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Phone', 'Email'])
            for contact in self.contacts:
                writer.writerow([contact.contact_id, contact.name, contact.phone, contact.email])

    def import_from_csv(self, csv_filename='contacts\\contacts.csv'):
        with open(csv_filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_contact(row['Name'], row['Phone'], row['Email'])

    def main(self):
        while True:
            print("\nВыберите опцию:")
            print("1. Добавить новый контакт")
            print("2. Найти контакт")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Экспортировать контакты в CSV")
            print("6. Импортировать контакты из CSV")
            print("7. Выход")

            choice = input("Введите номер опции: ")

            if choice == '1':
                name = input("Введите имя контакта: ")
                phone = input("Введите номер телефона (или оставьте пустым): ")
                email = input("Введите адрес электронной почты (или оставьте пустым): ")
                self.add_contact(name, phone or None, email or None)
                print("Контакт добавлен.")
            
            elif choice == '2':
                query = input("Введите имя или номер телефона для поиска: ")
                results = self.search_contact(query)
                if results:
                    for c in results:
                        print(c)
                else:
                    print("Контакты не найдены.")
            
            elif choice == '3':
                contact_id = int(input("Введите ID контакта для редактирования: "))
                name = input("Введите новое имя (или оставьте пустым): ")
                phone = input("Введите новый номер телефона (или оставьте пустым): ")
                email = input("Введите новый адрес электронной почты (или оставьте пустым): ")
                if self.edit_contact(contact_id, name or None, phone or None, email or None):
                    print("Контакт обновлен.")
                else:
                    print("Контакт не найден.")
            
            elif choice == '4':
                contact_id = int(input("Введите ID контакта для удаления: "))
                self.delete_contact(contact_id)
                print(f"Контакт с ID {contact_id} был удален.")
            
            elif choice == '5':
                self.export_to_csv()
                print("Контакты экспортированы в contacts.csv.")
            
            elif choice == '6':
                self.import_from_csv()
                print("Контакты импортированы из contacts.csv.")
            
            elif choice == '7':
                break
            
            else:
                print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 7.")

if __name__ == '__main__':
    manager = ContactManager()
    manager.main()