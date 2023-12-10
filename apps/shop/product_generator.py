
import random

from auths.models import MyUser
from bank.models import BankAccount
from shop.models import (
    Category,
    Product
)


def Categoryes_generator():
    category = random.choice([
        "Мебель", "Электроника", "Одежда", "Обувь", "Спорт и отдых", 
        "Красота и здоровье", "Бытовая техника", "Детские товары", 
        "Автотовары", "Книги", "Игрушки", "Хозяйственные товары", 
        "Товары для дома", "Украшения", "Техника для кухни", 
        "Музыкальные инструменты"]
    )
    return category


def Product_generator(category):
    if category == "Мебель":
        product = random.choice([
            "Диван", "Шкаф", "Стол", "Кровать", "Стул", 
        "Комод", "Тумба", "Полка", "Кушетка", "Зеркало", 
        "Кресло", "Кухонный гарнитур", "Письменный стол", 
        "Спальный гарнитур", "Прикроватная тумба"]
        )
        return product
    elif category == "Электроника":
        product = random.choice([
            "Смартфон", "Ноутбук", "Планшет", "Телевизор", 
            "Камера", "Наушники", "Умные часы", "Игровая приставка", 
            "Монитор", "Фотоаппарат", "Маршрутизатор", "Аккумулятор", 
            "Умный дом", "Аудиосистема", "Видеокамера"]
        )
        return product
    elif category == "Одежда":
        product = random.choice([
            "Футболка", "Джинсы", "Куртка", "Платье", "Брюки", 
            "Рубашка", "Юбка", "Свитер", "Пиджак", "Толстовка", 
            "Пальто", "Блузка", "Шорты", "Пиджама", "Костюм"]
        )
        return product
    elif category == "Обувь":
        product = random.choice([
            "Футболка", "Джинсы", "Куртка", "Платье", "Брюки", 
            "Рубашка", "Юбка", "Свитер", "Пиджак", "Толстовка", 
            "Пальто", "Блузка", "Шорты", "Пиджама", "Костюм"]
        )
        return product
    elif category == "Спорт и отдых":
        product = random.choice([
            "Беговая дорожка", "Велосипед", "Теннисная ракетка", 
            "Мяч для баскетбола", "Беговые кроссовки", "Гантели", 
            "Спортивный костюм", "Мат для йоги", "Ролики", "Ласты", 
            "Скейтборд", "Боксерская груша", "Шлем для велосипеда", 
            "Тренажерный зал", "Турник"]
        )
        return product
    elif category == "Красота и здоровье":
        product = random.choice([
            "Шампунь", "Крем для лица", "Тушь для ресниц", "Массажер", 
            "Зубная паста", "Бальзам для губ", "Пудра", "Дезодорант", 
            "Витамины", "Маникюрный набор", "Маска для волос", "Ароматическое масло", 
            "Термометр", "Солнцезащитные очки", "Тренажер для лица"]
        )
        return product
    elif category == "Бытовая техника":
        product = random.choice([
            "Холодильник", "Стиральная машина", "Пылесос", "Микроволновая печь", 
            "Утюг", "Электрочайник", "Кофемашина", "Плита", "Мясорубка", 
            "Блендер", "Фен", "Кондиционер", "Вентилятор", "Мультиварка", 
            "Посудомоечная машина"]
        )
        return product
    elif category == "Детские товары":
        product = random.choice([
            "Детская коляска", "Игрушечный набор", "Детский костюм", "Детская кроватка", 
            "Игрушечный автомобиль", "Кукла", "Конструктор", "Детская книга", 
            "Детская одежда", "Детская мебель", "Детская косметика", "Погремушка", 
            "Детский коврик", "Детская столовая посуда", "Детский манеж"]
        )
        return product
    elif category == "Автотовары":
        product = random.choice([
            "Автомобильное кресло", "Автомобильные шины", "Детский автокресло", 
            "Масло для двигателя", "Автомобильные чехлы", "Автоаксессуары", 
            "Автомобильный аккумулятор", "Коврики для авто", "Автомобильные диски", 
            "Автомагнитола", "Автосигнализация", "Автомобильные фильтры", "Пылесос для авто", 
            "Детское автомобильное кресло", "Автолампы"]
        )
        return product
    elif category == "Книги":
        product = random.choice([
            "Роман", "Учебник", "Детская книга", "Поэзия", "Научная литература", 
            "Фантастика", "Кулинарная книга", "Справочник", "Художественная литература", 
            "Аудиокнига", "Комикс", "Биография", "Историческая литература", 
            "Криминальный роман", "Дневник"]
        )
        return product
    elif category == "Игрушки":
        product = random.choice([
            "Кукла", "Игровой набор", "Конструктор", "Пазл", "Мягкая игрушка", 
            "Игровой автомобиль", "Фигурка героя", "Набор для рисования", 
            "Игрушечный домик", "Игровая кухня", "Игрушечный пистолет", 
            "Настольная игра", "Деревянные игрушки", "Робот-трансформер", 
            "Радиоуправляемый вертолет"]
        )
        return product
    elif category == "Хозяйственные товары":
        product = random.choice([
            "Швабра", "Ведро", "Моющее средство", "Ёршик", "Губка", "Мусорное ведро", 
            "Стиральный порошок", "Салфетки", "Гладильная доска", "Мешки для мусора", 
            "Щетка для унитаза", "Средство от насекомых", "Мыло", "Стиральная машина", 
            "Пылесос"]
        )
        return product
    elif category == "Товары для дома":
        product = random.choice([
            "Подушка", "Одеяло", "Постельное белье", "Халат", "Плед", "Чайный сервиз", 
            "Ковер", "Скатерть", "Фоторамка", "Декоративные свечи", "Ваза", "Картина", 
            "Скатерть", "Настольная лампа", "Блокнот"]
        )
        return product
    elif category == "Украшения":
        product = random.choice([
            "Кольцо", "Браслет", "Ожерелье", "Серьги", "Часы", "Подвеска", "Брошь", 
            "Пирсинг", "Зажимы для волос", "Запонки", "Бусы", "Заколка", "Чокер", "Медальон", "Каффы"]
        )
        return product
    elif category == "Техника для кухни":
        product = random.choice([
            "Миксер", "Хлебопечка", "Соковыжималка", "Мультиварка", "Блендер", "Мясорубка", 
            "Электрогриль", "Сковорода", "Кофеварка", "Чайник", "Тостер", "Печь для пиццы", 
            "Фритюрница", "Кухонные весы", "Хлебница"]
        )
        return product
    elif category == "Музыкальные инструменты":
        product = random.choice([
            "Гитара", "Фортепиано", "Скрипка", "Укулеле", "Барабаны", "Труба", "Саксофон", 
            "Аккордеон", "Флейта", "Баян", "Гармонь", "Тамбурин", "Микрофон", 
            "Электрогитара", "Губная гармошка"]
        )
        return product
    
def price_generator():
    price = random.randint(100, 99999)
    return price

def quantity_generator():
    quantity = random.randint(10, 200)
    return quantity

def rating_generator():
    rating = random.randint(1, 10)
    return rating

def ProductGenerator():
    MyUser.objects.create(
        number='77777777777',
        fio='КАСПИ-МАГАЗИН',
        )
    print('Учетка КАСПИ-МАГАЗИН создана')
    BankAccount.objects.create(
        iban='7777777777777777',
        owner=MyUser.objects.get(number='77777777777'),
        balance='0',
        currency='KZT',
        type='Gold',
        )
    print('Счет КАСПИ-МАГАЗИН создан')
    categoryes = [
            "Мебель", "Электроника", "Одежда", "Обувь", "Спорт и отдых", 
            "Красота и здоровье", "Бытовая техника", "Детские товары", 
            "Автотовары", "Книги", "Игрушки", "Хозяйственные товары", 
            "Товары для дома", "Украшения", "Техника для кухни", 
            "Музыкальные инструменты"]
    for i in categoryes:
        Category.objects.create(
            name = i
        )
        print(f'Категория {i} создана')
    for _ in range(200):
        cat = Categoryes_generator()
        name = Product_generator(cat)
        category = Category.objects.get(name=cat)
        Product.objects.create(
            name = name,
            category = category,
            price = price_generator(),
            quantity = quantity_generator(),
            rating = rating_generator(),
        )
        print(f'Продукт {name} создан')

# def RUN_ProductGenerator():
#     for _ in range(100):
#         return ProductGenerator()



# category = [
#     "Мебель", "Электроника", "Одежда", "Обувь", "Спорт и отдых", 
#     "Красота и здоровье", "Бытовая техника", "Детские товары", 
#     "Автотовары", "Книги", "Игрушки", "Хозяйственные товары", 
#     "Товары для дома", "Украшения", "Техника для кухни", 
#     "Музыкальные инструменты"]
    
# for i in category:
#     Category.objects.create(
#         name = i
#     )
#     print(f'Категория {i} создана')

# for i in range(10):
#     category = Categoryes_generator()
#     product = Product_generator(category)
#     price = price_generator()
#     quantity = quantity_generator()
#     rating = rating_generator()
#     ProductGenerator(category, product, price, quantity, rating)




# print('ok')