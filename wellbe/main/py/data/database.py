# import mysql.connector
#
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
#         with db.cursor() as cursor:
#             cursor.execute("SHOW DATABASES;")
#             for e in cursor:
#                 print(e)
#     finally:
#         db.close()
# except Exception as e:
#     print(e)

from wellbe.main.py.data.web_parser.spiders.testing_spider import StartSpider
StartSpider()