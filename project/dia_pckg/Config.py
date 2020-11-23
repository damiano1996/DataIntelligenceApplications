##########################################
#             Configurations             #
##########################################

# campaign
initial_date = '20200101' # Initial day of the campaign

# Seller wallet and ambitions
seller_max_budget = 5000    # Necessary(?)
max_n_clicks = 1000         # Max number of clicks in a single day        
avg_users_per_day = 100     # Number of users in the system when advertising section is not present (part 4 and 5)

# Product configuration
product_config = {
    'name': 'shoes',
    'base_price': 100,
    'max_price': 500,
    'production_cost': 0
}

# Features space
features_space = {
    'age': ['<30', '>30'],
    'profession': ['student', 'worker']
}

# Users' classes
classes_config = {
    'elegant': [1, 1],  # >30, worker
    'casual': [0, 0],  # <30, student
    'sports': [0, 1]  # <30, worker
}

# Directory where to store the Conversion Rate's curves
demand_path = 'demand_curves'

# PART 3 CONFIG
min_len = 10
z_score = 2.58
phase_lens = [60, 60, 80]  # n_days // n_abrupts_phases
n_abrupts_phases = len(phase_lens)
n_days = sum(phase_lens)

window_length = round(n_days / 6)

n_subcamp = 3

max_bid = 1
n_arms_advertising = 21
n_arms_pricing = 21

noise_std = 0.05

# PART 7 artificial noises
artificial_noise_ADV = 0.2
artificial_noise_CR = 0.2
