

class Basket:
    """
   A base Basket class, providing some default behaviors that
   can be inherited or override, as necessary.
   """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')  # for new user checking if the session is already present or not
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, productqty):
        """
        Adding and updating the user basket session data
        """
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {"price": str(product.price),
                                       'qty': int(productqty)}
        else:
            self.basket[product_id]["qty"] += int(productqty)
        self.session.modified = True  # tells django that I have modified session now you can save it

    def __len__(self):
        """
        Get the basket data and count the item
        """
        for item in self.basket.values():
            a = 120
        return sum(item["qty"] for item in self.basket.values())
