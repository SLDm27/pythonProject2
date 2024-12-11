import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_file import create_tables, Publisher, Shop, Sale, Book, Stock


login = 'postgres'
password = 'Jaguar2427'
host_name = "localhost:5432"
data_base_name = 'netology'
DSN = f'postgresql://{login}:{password}@{host_name}/{data_base_name}'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='ABC')
publisher2 = Publisher(name='DNS')
publisher3 = Publisher(name='777')

session.add(publisher1)
session.add(publisher2)
session.add(publisher3)

book1 = Book(title='Our world', publisher=publisher1)
book2 = Book(title='Hero life', publisher=publisher2)
book3 = Book(title='ME', publisher=publisher3)
session.add_all([book1, book2, book3])


shop1 = Shop(name='PUD')
shop2 = Shop(name='Yabloko')
session.add_all([shop1, shop2])


stock1 = Stock(book=book1, shop=shop2, count=10)
stock2 = Stock(book=book3, shop=shop2, count=5)
stock3 = Stock(book=book2, shop=shop1, count=1)
session.add_all([stock3, stock2, stock1])


sale1 = Sale(price='100.8', data_sale="2022-10-25T09:45:24.552Z", stock=stock1, count=2)
sale2 = Sale(price='50.5', data_sale="2022-10-25T09:45:24.552Z", stock=stock1, count=4)
session.add_all([sale1, sale2])
session.commit()

# session.close()


def publisher_data(class_):
    id_ = input('Введите id издателя:')
    name = input('Введите name издателя:')
    if id_:
        for c in session.query(class_).filter(class_.id == id_).all():
            print(c)
    elif name:
        for c in session.query(class_).filter(class_.name == name).all():
            print(c)


def get_shops(res): #Функция принимает обязательный параметр
    query = session.query( #Создаем общее тело запроса на выборку данных и сохраняем в переменную
        Book.title, Shop.name, Sale.price, Sale.data_sale, #Название книги, имя магазина, стоимость продажи и дату продажи
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        query = query.filter(Publisher.id == res).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где айди публициста равно переданным данным в функцию, и сохраняем в переменную
    else:
        query = query.filter(Publisher.name == res).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где имя публициста равно переданным данным в функцию, и сохраняем в переменную
    for title, name, price, date_sale in query: #Проходим в цикле по переменой, в которой сохраняем результат фильтрации, и при каждой итерации получаем кортеж и распаковываем значения в 4 переменные
        print(f"{title: <40} | {name: <10} | {price: <5} | {data_sale.strftime('%d-%m-%Y')}")#Передаем в форматированную строку переменные, которые содержат имя книги, название магазина, стоимость продажи и дату продажи

if __name__ == "__main__":
    res = input('Введите Id (1 или 2) или имя издателя (Лабиринт или Эксмо): ')
    get_shops(res)
