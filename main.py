from task.task_manager import TaskManager
from notes.note import NoteManager
from contacts.contact import ContactManager
from finance.finance_manager import FinanceManager
from calculate.file_operations import calculator
def main_menu():
    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            notes_manager = NoteManager()
            notes_manager.main()

        elif choice == '2':
            task_manager = TaskManager()
            task_manager.main()

        elif choice == '3':
            contact_manager = ContactManager()
            contact_manager.main()

        elif choice == '4':
            finance_manager = FinanceManager()
            finance_manager.main()

        elif choice == '5':
            calculator()  

        elif choice == '6':
            print("Выход из программы.")
            break
        
        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 6.")

if __name__ == '__main__':
    main_menu()


