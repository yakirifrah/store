from .category import Category


class Product:
    def __init__(self, category_id, description, price, title, favorite, img_url):
        self.category_id = category_id
        self.description = description
        self.price = price
        self.title = title
        self.favorite = "1" if favorite == "on" else "0"
        self.img_url = img_url
