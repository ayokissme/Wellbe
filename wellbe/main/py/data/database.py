# import mysql.connector
#
# try:
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="2002",
#     )
#     print("successfully")
#
#     try:
#         with db.cursor(buffered=True) as cursor:
#             cursor.execute("SHOW DATABASES;")
#             cursor.execute('use wellbe;')
#             # cursor.execute('insert into product (name, brand, price, rating, reviews_count, stock_status, size, size_type, link) '
#             #                f'values ("нов", "бре", 20.5, 4.4, 70, 1, 80, "гм", "фа");')
#             # cursor.execute('select id from product where name = "A Taste Of Thai, Соус с чесноком и перцем чили, 207 мл (7 жидк. Унций)" limit 1;')
#             # print(cursor.fetchone()[0])
#             cursor.execute('delete from category')
#             cursor.execute('delete from product')
#             db.commit()
#             print('OK')
#             # cursor.execute("SHOW DATABASES;")
#             # cursor.execute('use wellbe;')
#             # cursor.execute('select * from product;')
#             # for e in cursor:
#             #     print(e)
#     finally:
#         db.close()
# except Exception as e:
#     print(e)

from wellbe.main.py.data.web_parser.spiders.products_spider import StartSpider
StartSpider()

# from wellbe.main.py.data.web_parser.spiders.testing_spider import StartSpider
# StartSpider()