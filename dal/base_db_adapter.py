from abc import ABC, abstractclassmethod


class BaseDbAdapter(ABC):
    @abstractclassmethod
    def add_category(self, category):
        pass

    @abstractclassmethod
    def delete_category(self, category_id):
        pass

    @abstractclassmethod
    def get_all_categories(self):
        pass

    @abstractclassmethod
    def add_product(self, product):
        pass

    @abstractclassmethod
    def get_product(self, product_id):
        pass

    @abstractclassmethod
    def delete_product(self, product_id):
        pass

    @abstractclassmethod
    def get_all_products(self):
        pass

    @abstractclassmethod
    def get_products_by_category(self, category_id):
        pass
