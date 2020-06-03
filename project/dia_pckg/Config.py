##########################################
#             Configurations             #
##########################################

# campaign
initial_date = '20200101'
n_days = 500

# Seller wallet and ambitions
seller_max_budget = 20000  # $
max_n_clicks = 10000
avg_users_per_day = 1000  # this param must be changed after budget allocation available!

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
    'elegant': [1, 1],  # >30, worker
    'casual': [0, 0],  # <30, student
    'sports': [0, 1]  # <30, worker
}
# number of abrupt phases
n_abrupts = 3
# directory to store the curves
demand_path = 'demand_curves'
