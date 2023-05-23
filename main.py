from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Publisher, Book, Stock, Shop, Sale
from json_reader import populate_database_from_json

# url в формате postgresql://postgres:<password>@localhost:5432/postgres
url_db = 'postgresql://demolyky:123456@localhost:5432/postgres'

def get_shops(data):
    # подключаемся к БД
    engine = create_engine(url_db)

    # создаем фабрику сессий
    Session = sessionmaker(bind=engine)

    # получаем экземпляр класса Session
    session = Session()

    # Выполняем запрос и фильтруем результаты
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .select_from(Publisher) \
        .join(Book) \
        .join(Stock) \
        .join(Sale) \
        .join(Shop)

    if not data.isdigit():
        query = query.filter(Publisher.name == data)
    else:
        query = query.filter(Publisher.id == data)

    # Выполняем запрос и выводим результаты
    sales = query.order_by(Sale.date_sale.desc()).all()

    for sale in sales:
        print(f'{sale[0]: <40} | {sale[1]: <10} | {sale[2]: <8} | {sale[3].strftime("%d-%m-%Y")}')


if __name__ == '__main__':
    populate_database_from_json('tests_data.json', url_db)
    data = input('Введите имя или айди: ')
    get_shops(data)
