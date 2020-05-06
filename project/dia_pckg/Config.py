##########################################
#             Configurations             #
##########################################

# campaign
initial_date = '20200101'
n_days = 365

# Seller wallet and ambitions
seller_max_budget = 20000  # $
max_n_clicks = 10000
avg_users_per_day = 30  # this param must be changed after budget allocation available!

# one product to sell
product_config = {
    'name': 'shoes',
    'base_price': 100,
    'max_price': 500,
    'production_cost': 0
}

# features space
features_space = {
    'age': ['<30', '>30'],
    'profession': ['student', 'worker']
}

# three classes of users
classes_config = {
    'elegant': {'name': 'elegant', 'features': [1, 1], 'max_demand': 0.6},  # >30, worker
    'casual': {'name': 'casual', 'features': [0, 0], 'max_demand': 0.9},  # <30, student
    'sports': {'name': 'sports', 'features': [0, 1], 'max_demand': 0.75}  # <30, worker
}
# number of abrupt phases
n_abrupts = 3
