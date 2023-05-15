import requests

from typing import List

from cart import Cart
from schemas.product import Product
from services.parser import Parser


class ShopifyImporter:
    def __init__(self, cart: Cart) -> None:
        self.cart = cart

    def start(self) -> List[Product]:

        data = self.get_list_products()
        # products: List[Product] = []

        # implement the importer logic here

        return data

    def get_list_products(self):
        headers = {
            "X-Shopify-Access-Token": self.cart.token,
            "Content-Type": "application/json",
        }
        api_v = "2023-04"
        request_url = f"{self.cart.url}/admin/api/{api_v}/products.json"
        response = requests.get(url=request_url, headers=headers)
        data = response.json()
        products = data.get("products", [])
        final_data: List[Product] = []
        
        for product in products:
            handled_product = Parser(product).handle_product()
            final_data.append(handled_product)

        return final_data
            

def get_importer(cart):
    return ShopifyImporter(cart)