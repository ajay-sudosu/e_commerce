from django.conf import settings

from store.models import Product
from decimal import Decimal


class Basket:
    """
   A base Basket class, providing some default behaviors that
   can be inherited or override, as necessary.
   """
    BASKET_PRICE = 0

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)  # for new user checking if the session is already present or not
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, productqty):
        """
        Adding and updating the user basket session data
        """
        product_id = product.id
        if product_id not in self.basket:
            self.basket[str(product_id)] = {"price": str(product.price),
                                            'qty': int(productqty)}
        else:
            self.basket[product_id]["qty"] += int(productqty)
        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data and query in the database and return products.
        """
        product_ids = self.basket.keys()
        products = Product.is_active_products.filter(id__in=product_ids)
        extra_data_basket = self.basket.copy()
        for product in products:
            extra_data_basket[str(product.id)]["product"] = product

        for item in extra_data_basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def delete(self, product):
        """
        Delete item from session data.
        """
        product_id = product
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product, productqty):
        """
        Update item in session data.
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = int(productqty)
        self.save()

    def save(self):
        self.session.modified = True  # tells django that session has been modified now you can save it

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def __len__(self):
        """
        Get the basket data and count the item
        """
        # total = 0
        # for item in self.basket.values():
        #     total += item["qty"]
        # return sum(item["qty"] for item in self.basket.values())
        return len(self.basket)

    def get_item_subtotal_price(self, product_id):
        item = self.basket[str(product_id)]
        return f'Rs.{Decimal(item["price"]) * item["qty"]}'

    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(80.00)
        return subtotal + shipping
