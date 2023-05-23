import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Base, Publisher, Book, Shop, Stock, Sale

def populate_database_from_json(json_file_path, db_url):
    # Создаем соединение с базой данных
    engine = create_engine(db_url)
    # Создаем все таблицы, определенные в Base, если их еще нет в базе данных
    Base.metadata.create_all(engine)
    # Создаем фабрику сессий
    Session = sessionmaker(bind=engine)
    # Создаем экземпляр сессии
    session = Session()

    # Открываем JSON-файл
    with open(json_file_path, 'r') as f:
        # Загружаем данные из JSON-файла
        data = json.load(f)

        # Обрабатываем каждый элемент данных
        for item in data:
            # Получаем модель и поля элемента
            model = item['model']
            fields = item['fields']

            # В зависимости от модели создаем соответствующий объект и добавляем его в сессию
            if model == 'publisher':
                publisher = Publisher(id=item['pk'], name=fields['name'])
                session.add(publisher)
                session.commit()
            elif model == 'book':
                book = Book(id=item['pk'], title=fields['title'], id_publisher=fields['id_publisher'])
                session.add(book)
                session.commit()
            elif model == 'shop':
                shop = Shop(id=item['pk'], name=fields['name'])
                session.add(shop)
                session.commit()
            elif model == 'stock':
                stock = Stock(id=item['pk'], id_shop=fields['id_shop'], id_book=fields['id_book'], count=fields['count'])
                session.add(stock)
                session.commit()
            elif model == 'sale':
                sale = Sale(id=item['pk'], price=fields['price'], date_sale=fields['date_sale'], count=fields['count'], id_stock=fields['id_stock'])
                session.add(sale)
                session.commit()

        # Фиксируем изменения в базе данных
        session.commit()


