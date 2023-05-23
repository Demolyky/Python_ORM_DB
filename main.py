from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Publisher, Book, Stock, Shop, Sale
from json_reader import populate_database_from_json

# url в формате postgresql://postgres:<password>@localhost:5432/postgres
url_db = 'postgresql://demolyky:123456@localhost:5432/postgres'

def print_db():
    # подключаемся к БД
    engine = create_engine(url_db)

    # создаем фабрику сессий
    Session = sessionmaker(bind=engine)

    # получаем экземпляр класса Session
    session = Session()

    # Получаем имя издателя от пользователя
    publisher_name = input('Введите имя издателя: ')

    # Выполняем запрос и выводим результаты
    sales = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Book.publisher) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Sale, Sale.id_stock == Stock.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .filter(Publisher.name == publisher_name) \
        .order_by(Sale.date_sale.desc()).all()

    for sale in sales:
        print(f'{sale[0]} | {sale[1]} | {sale[2]} | {sale[3].strftime("%d-%m-%Y")}')


def main():
    # заполняем БД из Json-файла
    populate_database_from_json('tests_data.json', url_db)

    print_db()


if __name__ == '__main__':
    main()
