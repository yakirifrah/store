from api.store_api import StoreApi
from dal.my_sql_db_adapter import MySqlDBAdapter


if __name__ == "__main__":
    api = StoreApi(MySqlDBAdapter())
    api.run()
