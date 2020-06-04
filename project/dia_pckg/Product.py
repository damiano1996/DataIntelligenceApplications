class Product:

    def __init__(self, product_config):
        """
        :param name: name of the product
        :param base_price: minimum price
        :param max_price: maximum price
        :param production_cost: production cost
        """
        self.name = product_config['name']
        self.base_price = product_config['base_price']
        self.max_price = product_config['max_price']
        self.production_cost = product_config['production_cost']
