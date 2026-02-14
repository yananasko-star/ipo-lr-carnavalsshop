import json
import os

# Имя файла для хранения данных
filename = "cities.json"

# Счетчик операций
operations_count = 0

# Загрузка данных из файла
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        cities = json.load(file)
else:
    # Начальные данные (5 записей)
    cities = [
        {"id": 1, "name": "Москва", "country": "Россия", "is_big": True, "people_count": 12600000},
        {"id": 2, "name": "Минск", "country": "Беларусь", "is_big": True, "people_count": 2000000},
        {"id": 3, "name": "Брест", "country": "Беларусь", "is_big": True, "people_count": 340000},
        {"id": 4, "name": "Гродно", "country": "Беларусь", "is_big": True, "people_count": 368000},
        {"id": 5, "name": "Полоцк", "country": "Беларусь", "is_big": False, "people_count": 82000}
    ]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cities, file, ensure_ascii=False, indent=2)

# Основной цикл программы
while True:
    print("\n" + "="*50)
    print("МЕНЮ:")
    print("1. Вывести все записи")
    print("2. Вывести запись по полю")
    print("3. Добавить запись")
    print("4. Удалить запись по полю")
    print("5. Выйти из программы")
    print("="*50)
    
    choice = input("Выберите пункт меню (1-5): ")
    
    if choice == "1":
        # Вывести все записи
        print("\n" + "="*50)
        print("ВСЕ ЗАПИСИ О ГОРОДАХ:")
        print("="*50)
        for city in cities:
            big_status = "Большой город" if city["is_big"] else "Маленький город"
            print(f"ID: {city['id']}")
            print(f"Город: {city['name']}")
            print(f"Страна: {city['country']}")
            print(f"Статус: {big_status}")
            print(f"Население: {city['people_count']} чел.")
            print("-" * 30)
        operations_count += 1
    
    elif choice == "2":
        # Вывести запись по полю
        try:
            search_id = int(input("Введите ID города для поиска: "))
            found = False
            for i, city in enumerate(cities):
                if city["id"] == search_id:
                    print("\n" + "="*50)
                    print(f"НАЙДЕНА ЗАПИСЬ (позиция {i}):")
                    print("="*50)
                    big_status = "Большой город" if city["is_big"] else "Маленький город"
                    print(f"ID: {city['id']}")
                    print(f"Город: {city['name']}")
                    print(f"Страна: {city['country']}")
                    print(f"Статус: {big_status}")
                    print(f"Население: {city['people_count']} чел.")
                    found = True
                    break
            
            if not found:
                print("\n Запись с таким ID не найдена!")
            else:
                operations_count += 1
                
        except ValueError:
            print("\n Ошибка: ID должен быть числом!")
    
    elif choice == "3":
        # Добавить запись
        try:
            print("\nДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ:")
            new_id = int(input("Введите ID: "))
            
            # Проверка на уникальность ID
            for city in cities:
                if city["id"] == new_id:
                    print(" Ошибка: Город с таким ID уже существует!")
                    break
            else:
                name = input("Введите название города: ")
                country = input("Введите название страны: ")
                people_count = int(input("Введите население города: "))
                is_big = people_count > 100000
                
                new_city = {
                    "id": new_id,
                    "name": name,
                    "country": country,
                    "is_big": is_big,
                    "people_count": people_count
                }
                cities.append(new_city)
                
                # Сохранение в файл
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(cities, file, ensure_ascii=False, indent=2)
                
                print(" Запись успешно добавлена!")
                operations_count += 1
                
        except ValueError:
            print(" Ошибка: ID и население должны быть числами!")
    
    elif choice == "4":
        # Удалить запись по полю
        try:
            delete_id = int(input("Введите ID города для удаления: "))
            found = False
            
            for i, city in enumerate(cities):
                if city["id"] == delete_id:
                    deleted_city = cities.pop(i)
                    
                    # Сохранение в файл
                    with open(filename, 'w', encoding='utf-8') as file:
                        json.dump(cities, file, ensure_ascii=False, indent=2)
                    
                    print(f" Запись с ID {delete_id} ({deleted_city['name']}) удалена!")
                    found = True
                    operations_count += 1
                    break
            
            if not found:
                print(" Запись с таким ID не найдена!")
                
        except ValueError:
            print(" Ошибка: ID должен быть числом!")
    
    elif choice == "5":
        # Выйти из программы
        print("\n" + "="*50)
        print(f"ПРОГРАММА ЗАВЕРШЕНА")
        print(f"Всего выполнено операций: {operations_count}")
        print("="*50)
        break
    
    else:
        print(" Ошибка: выберите пункт от 1 до 5!")