##########################################
#             Configurations             #
##########################################

# Seller wallet and ambitions
seller_max_budget = 20000  # $
max_n_clicks = 10000

# one product to sell
product_name = 'shoes'
product_base_price = 100
product_max_price = 500

# features space
features_space = {
    'age': ['<30', '>30'],
    'profession': ['student', 'worker']
}

# three classes of users
classes = {
    'elegant': [1, 1],  # >30, worker
    'casual': [0, 0],  # <30, student
    'sports': [0, 1]  # <30, worker
}
# number of abrupt phases
n_abrupts = 3
