import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

# # ---------------------- REGION ---------------------------
#     def create_regions_table(self):
#         create_table_query = '''
#         CREATE TABLE IF NOT EXISTS regions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             region_name TEXT NOT NULL UNIQUE
#         );
#         '''
#         self.cursor.execute(create_table_query)
#         self.conn.commit()
#
#     def add_region(self, region_name):
#         try:
#             self.cursor.execute(f"INSERT INTO regions (region_name) VALUES (?)", (region_name,))
#             self.conn.commit()
#             return True
#         except Exception as e:
#             print(e)
#             return False
# # ------------------------ NUMBER --------------------------------------
#
#     def create_numbers_table(self, table_name='numbers'):
#         create_table_query = f'''
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             region INTEGER NOT NULL,
#             lot_number TEXT NOT NULL UNIQUE,
#             lot_category TEXT NOT NULL,
#             car_region_number TEXT NOT NULL,
#             car_number TEXT NOT NULL,
#             start_price REAL NOT NULL,
#             number_end_date TEXT NOT NULL,
#             number_end_hour TEXT NOT NULL,
#             FOREIGN KEY (region) REFERENCES regions (id)
#         );
#         '''
#         self.cursor.execute(create_table_query)
#         self.conn.commit()
#
#     def add_number(self, region, lot_number, lot_category, car_region_number, car_number, start_price, number_end_date, number_end_hour):
#         try:
#             self.cursor.execute(
#                 "INSERT INTO numbers "
#                 "(region, lot_number, lot_category, car_region_number,"
#                 "car_number, start_price, number_end_date, number_end_hour)"
#                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
#                 (region, lot_number, lot_category, car_region_number,
#                  car_number, start_price, number_end_date, number_end_hour))
#             self.conn.commit()
#             return True
#         except Exception as e:
#             print(e)
#             return False
#
#     def get_numbers(self, region_id):
#         try:
#             self.cursor.execute(f"SELECT * FROM numbers WHERE region=?", (region_id,))
#             return self.cursor.fetchall()
#         except Exception as e:
#             print(e)
#             return False
#
#     def get_numbers_reg_price(self, region_id, price):
#         try:
#             self.cursor.execute(f"SELECT * FROM numbers WHERE region=? and start_price=?", (region_id, price))
#             return self.cursor.fetchall()
#         except Exception as e:
#             print(e)
#             return False
#
#     def number_update(self, price, start_pr):
#         try:
#             self.cursor.execute(f"UPDATE numbers SET start_price=? WHERE start_price=?", (price, start_pr))
#             self.conn.commit()
#             return True
#         except Exception as e:
#             print(e)
#             return False
#
#     def search_number(self, region_id, number):
#         try:
#             self.cursor.execute(f"SELECT * FROM numbers WHERE car_region_number=? and car_number=?", (region_id, number))
#             return self.cursor.fetchone()
#         except Exception as e:
#             print(e)
#             return False