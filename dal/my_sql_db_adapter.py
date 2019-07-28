from .base_db_adapter import BaseDbAdapter
from pymysql import cursors, connect
from bottle import request, get, HTTPError, response
import json


class MySqlDBAdapter(BaseDbAdapter):
    def __init__(self):
        self._connection = connect(
            host="localhost",
            user="root",
            password="yakir1990",
            db="store",
            charset="utf8",
            cursorclass=cursors.DictCursor,
        )

    def get_all_categories(self):
        try:
            with self._connection.cursor() as cursor:
                get_all_categories = 'SELECT * FROM categories'
                cursor.execute(get_all_categories)
                result = cursor.fetchall()
                return json.dumps(
                    {
                        "STATUS": "SUCCESS",
                        "CATEGORIES": result
                    })
        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f"{e}"
            })

    def delete_category(self, category_id):
        try:
            with self._connection.cursor() as cursor:
                delete_category = 'DELETE FROM categories WHERE id=%(id)s'
                cursor.execute(delete_category, {"id": category_id})
                self._connection.commit()
        except:
            return json.dumps({'error': 'something is worng with the DB'})

    def add_product(self, product):
        missing_paramenter = False
        category_not_found = False
        if not product.category_id:
            category_not_found = True
            raise "category not found"
        if not product.title or not product.description or not product.price or not product.img_url or not product.category_id:
            missing_paramenter = True
            raise "missing parameters"
        if not missing_paramenter and not category_not_found:
            try:
                print(
                    f'title: {product.title} , desc: {product.description} , price:{product.price} , img_url:{product.img_url} , favorite:{product.favorite} , cat_id: {product.category_id} ')
                with self._connection.cursor() as cursor:
                    add_product = 'INSERT INTO products (title,description,price,img_url,favorite,category_id) VALUES(%(title)s,%(description)s,%(price)s,%(img_url)s,%(category_id)s)'
                    cursor.execute(add_product, {"title": product.title, "description": product.description, "price": product.price,
                                                 "img_url": product.img_url, "favorite": product.favorite, "category_id": product.category_id})
                    id = cursor.lastrowid
                    self._connection.commit()
                    return json.dumps({
                        "STATUS": "SUCCESS",
                        "PRODUCT_ID": id
                    })
                    response.status_code = 201
            except Exception as e:
                return json.dumps({
                    "STATUS": "ERROR",
                    "MSG": f'{e}'
                })

    def get_product(self, product_id):
        return super().get_product(product_id)

    def delete_product(self, product_id):
        return super().delete_product(product_id)

    def get_all_products(self):
        try:
            with self._connection.cursor() as cursor:
                get_all_products = 'SELECT * FROM products'
                cursor.execute(get_all_products)
                result = cursor.fetchall()
                return json.dumps(
                    {
                        "STATUS": "SUCCESS",
                        "CATEGORIES": result
                    })
        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f"{e}"
            })

    def get_products_by_category(self, category_id):
        try:
            with self._connection.cursor() as cursor:
                get_product_by_category = 'SELECT * FROM products WHERE category_id=%s'
                cursor.execute(get_product_by_category, category_id)
                result = cursor.fetchall()
                return json.dumps({
                    "PRODUCTS": result
                })

        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f"{e}"
            })

    def add_category(self):
        try:
            with self._connection.cursor() as cursor:
                category_name = request.forms.get('name')
                if len(category_name) == 0:
                    raise "Name parameter is missing"
                category_exists = False
                categories = json.loads(self.get_all_categories())
                categories_list = [li['name']
                                   for li in categories["CATEGORIES"]]
                if category_name in categories_list:
                    print('Category already exists')
                    response.status_code = 200
                    category_exists = True
                    raise "Category already exists"
                if not category_exists:
                    print('create_category')
                    add_category = 'INSERT INTO categories (name) VALUES (%(category_name)s)'
                    cursor.execute(
                        add_category, {"category_name": category_name})
                    id = cursor.lastrowid
                    self._connection.commit()
                return json.dumps({
                    "STATUS": "SUCCESS",
                    "CAT_ID": id
                })
                response.status_code = 201
        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f'{e}'
            })
