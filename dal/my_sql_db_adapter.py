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
        category_not_found = False
        title_exists = False
        if not product.category_id:
            category_not_found = True
            return json.dumps({"STATUS": "ERROR", "MSG": "category not found"})
        if not product.title or not product.description or not product.price or not product.img_url or not product.category_id:
            return json.dumps({"STATUS": "ERROR", "MSG": "Some parameters are missing"})
        try:
            with self._connection.cursor() as cursor:
                products = json.loads(self.get_all_products())
                for prod in products['PRODUCTS']:
                    if product.title != prod["title"]:
                        add_product = 'INSERT INTO products (title,description,price,img_url,favorite,category_id) VALUES(%(title)s,%(description)s,%(price)s,%(img_url)s,%(category_id)s)'
                    else:
                        title_exists = True
                        prod_id = prod['id']
                        update_product = 'UPDATE products set title = %(title)s,%(description)s,%(price)s,%(img_url)s,%(favorite)s WHERE id= %(prod_id)s'
                        break
                if not title_exists:
                    print(type(product.price))
                    print(product.price)
                    cursor.execute(add_product, {"title": product.title, "description": product.description, "price": product.price,
                                                 "img_url": product.img_url, "favorite": product.favorite, "category_id": product.category_id})
                    # cursor.execute(add_product)
                else:
                    print(type(product.price))
                    cursor.execute(update_product, {"title": product.title, "description": product.description,
                                                    "price": float(product.price), "img_url": product.img_url, "prod_id": int(prod_id)})
                self._connection.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "MSG": "Product was added/updated successfully", "PRODUCT_ID": cursor.lastrowid})

        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f'{e}'
            })

    def get_product(self, product_id):
        try:
            with self._connection.cursor() as cursor:
                get_product = 'SELECT * FROM products WHERE id=%(product_id)s'
                cursor.execute(get_product, {"product_id": product_id})
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was fetched successfully", "PRODUCT": cursor.fetchall()})
        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f'{e}'
            })

    def delete_product(self, product_id):
        try:
            with self._connection.cursor() as cursor:
                del_product = "delete from products where id =%(product_id)s"
                cursor.execute(del_product, {"product_id": product_id})
                self.connection.commit()
                response.status = 201
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was deleted successfully"})
        except Exception as e:
            return json.dumps({
                "STATUS": "ERROR",
                "MSG": f'{e}'
            })

    def get_all_products(self):
        try:
            with self._connection.cursor() as cursor:
                get_all_products = 'select * from products'
                cursor.execute(get_all_products)
                result = cursor.fetchall()
                return json.dumps({"STATUS": "SUCCESS", "MSG": "Products fetched", "PRODUCTS": result})
        except Exception as e:
            return json.dumps({"STATUS": "ERROR", "MSG": f"Internal Error{e}"})

    def get_products_by_category(self, category_id):
        try:
            with self._connection.cursor() as cursor:
                get_product_by_category = 'SELECT * FROM products WHERE category_id=%s ORDER BY id ASC, favorite DESC'
                cursor.execute(get_product_by_category, category_id)
                result = cursor.fetchall()
                return json.dumps({
                    "STATUS": "SUCCESS",
                    "MSG": "Products fetched",
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
