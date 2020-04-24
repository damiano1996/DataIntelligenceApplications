class Product:

    def __init__(self, name, base_price, max_price):
        """
        :param name: name of the product
        :param base_price: minimum price
        :param max_price: maximum price
        """
        self.name = name
        self.base_price = base_price
        self.max_price = max_price
