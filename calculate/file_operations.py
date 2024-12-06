def calculator():
    print("Добро пожаловать в калькулятор!")
    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    
    while True:
        choice = input("Введите номер операции (1/2/3/4) или '0' для выхода: ")

        if choice == '0':
            print("Выход из программы.")
            break
        
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                
                if choice == '1':
                    print(f"{num1} + {num2} = {(num1 + num2)}")
                elif choice == '2':
                    print(f"{num1} - {num2} = {(num1 - num2)}")
                elif choice == '3':
                    print(f"{num1} * {num2} = {(num1 * num2)}")
                elif choice == '4':
                    if num2 == 0:
                        print("Ошибка: деление на ноль.")
                    else:
                        result = num1 / num2
                        print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
        else:
            print("Некорректный ввод. Пожалуйста, выберите номер операции от 1 до 4.")