##########################################
#             Configurations             #
##########################################

# campaign
initial_date = '20200101'
n_days = 30

# Seller wallet and ambitions
seller_max_budget = 20000  # $
max_n_clicks = 1000
avg_users_per_day = 100  # this param must be changed after budget allocation available!

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
n_abrupts_phases = 3
# directory to store the curves
demand_path = 'demand_curves'

len_window = 5
phase_len = n_days // n_abrupts_phases
# Since n_abrupts_phases is odd and n_days could be even we add 1 to obtain equal phases
phase_len = phase_len + 1 if n_days % 2 == 0 else phase_len

print_span = 60  # How often we want to print the graphs

n_subcamp = 3

max_bid = 1
n_arms = 20

noise_std = 0.05
