"""
    Definition of the Product.
"""


class Product:

    def __init__(self, product_config):
        """

        @param product_config: product configuration dictionary.
        """
        self.name = product_config['name']
        self.base_price = product_config['base_price']
        self.max_price = product_config['max_price']
        self.production_cost = product_config['production_cost']
