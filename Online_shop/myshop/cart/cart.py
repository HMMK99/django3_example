from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    """
    this is to initialize the cart
    """
    # store the session to make it accessable
    self.session = request.session
    cart = self.session.get(settings.CART_SESSION_ID)
    if not cart:
        # save an empty cart_session
        cart = self.session[settings.CART_SESSION_ID] = {}
    self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        add or updeate product quantity
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # to make sure it's saved we mark it as modified
        self.session.modified = True

    def remove(self, product):
        # remove product
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save

    def __iter__(self):
        '''
        iterate over items in cart
        '''
        product_ids = self.cart.keys()
        # get product objects
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

        def __len__(self):
            '''counter'''
            return sum(item['quantity'] for item in self.cart.values())

        def get_total_price(self):
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values)

        def clear(self):
            # delete all
            del self.session[settings.CART_SESSION_ID]
            self.save()
