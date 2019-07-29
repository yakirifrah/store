from bottle import route, run, template, static_file, get, post, delete, request, HTTPResponse
from sys import argv
import json
from entities.product import Product
import pymysql
from dal.my_sql_db_adapter import MySqlDBAdapter
_db_adapter = MySqlDBAdapter()


@get("/")
def index():
    return template("index.html")


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/categories')
def get_all_categories():
    result = _db_adapter.get_all_categories()
    return result


@get('/category/<id:int>/products')
def get_products_by_category(id):
    result = _db_adapter.get_products_by_category(id)
    return result


@get('/products')
def get_all_products():
    result = _db_adapter.get_all_products()
    return result


@get('/product/<id:int>')
def get_product(id):
    get_product = _db_adapter.get_product(id)
    return get_product


@post('/category')
def add_category():
    result = _db_adapter.add_category()
    return result


@delete('/category/<catId:path>')
def delete_category(catId):
    _db_adapter.delete_category(catId)


@delete('/product/<id:int>')
def delete_product(id):
    delete_product = _db_adapter.delete_product(id)
    return delete_product


@post('/product')
def add_product():
    category_id = request.forms.get('category')
    title = request.forms.get('title')
    description = request.forms.get('desc')
    favorite = request.forms.get('favorite')
    price = request.forms.get('price')
    img_url = request.forms.get('img_url')
    product = Product(category_id, description,
                      price, title, favorite, img_url)
    result = _db_adapter.add_product(product)
    return result


run(host='localhost', port=4000, debug=True, reloader=True)
