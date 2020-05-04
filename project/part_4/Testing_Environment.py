# sys.path.insert(0, 'D:\\usw-andreab\\Desktop\\DataIntelligenceApplications\\')

import matplotlib.pyplot as plt
import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
# first of all we define our campaign
from project.part_4.Env_4 import Env_4
from project.part_4.TS_Learner import TS_Learner

n_arms = 10

campaign = Campaign(max_budget=seller_max_budget,
                    max_n_clicks=max_n_clicks)

# one product to sell
product = Product(name=product_name,
                  base_price=product_base_price,
                  max_price=product_max_price,
                  production_cost=product_production_cost)

# three classes of users:
class_names = list(classes.keys())
print('Classes:', class_names)

# initialization of the three classes
class_1 = Class(class_name=class_names[0], class_features=classes[class_names[0]], product=product,
                n_abrupt_phases=n_abrupts)
class_2 = Class(class_name=class_names[1], class_features=classes[class_names[1]], product=product,
                n_abrupt_phases=n_abrupts)
class_3 = Class(class_name=class_names[2], class_features=classes[class_names[2]], product=product,
                n_abrupt_phases=n_abrupts)

env = Env_4(initial_date=initial_date,
            n_days=n_days,
            # users_per_day=avg_users_per_day,
            users_per_day=1,
            class_1=class_1,
            class_2=class_2,
            class_3=class_3,
            n_arms=n_arms)

optimals = env.get_optimals()
plt.plot(env.classes[0].conv_rates[0][0], env.classes[0].conv_rates[0][1], label=class_1.name, linestyle='--')
plt.plot(env.classes[1].conv_rates[0][0], env.classes[1].conv_rates[0][1], label=class_2.name, linestyle='--')
plt.plot(env.classes[2].conv_rates[0][0], env.classes[2].conv_rates[0][1], label=class_3.name, linestyle='--')
plt.plot(env.aggregate_demand_curve[0], env.aggregate_demand_curve[1], label='aggregate')

plt.scatter(optimals[class_1.name]['price'], optimals[class_1.name]['probability'], marker='o',
            label=f'opt {class_1.name}')
plt.scatter(optimals[class_2.name]['price'], optimals[class_2.name]['probability'], marker='o',
            label=f'opt {class_2.name}')
plt.scatter(optimals[class_3.name]['price'], optimals[class_3.name]['probability'], marker='o',
            label=f'opt {class_3.name}')
plt.scatter(optimals['aggregate']['price'], optimals['aggregate']['probability'], marker='o', label='opt aggregate')

plt.xlabel('Price')
plt.ylabel('Conversion Rate')
plt.legend()
plt.show()

n_experiments = 200  # the number is small to do a raw test, otherwise set it to 1000
rewards_per_experiment = [] #collect all the rewards achieved from the TS 
arm_prices = env.get_arm_price(np.arange(n_arms))

for e in range(0, n_experiments):
    current_date, done = env.reset()
    ts_learner = TS_Learner(n_arms=n_arms, arm_prices=arm_prices)

    while not done:
        #pulled_arm = ts_learner.pull_arm() #optimize by demand
        pulled_arm = ts_learner.pull_arm_v2()  # optimize by revenue

        user = User(random=True)
        reward, current_date, done = env.user_step(pulled_arm, user)
        
        ts_learner.update(pulled_arm, reward)

    rewards = ts_learner.collected_rewards
    rewards_per_experiment.append(rewards)

aggregate_opt = optimals['aggregate']['price'] * optimals['aggregate']['probability']  
class1_opt = optimals[class_1.name]['price'] * optimals[class_1.name]['probability']  
class2_opt = optimals[class_2.name]['price'] * optimals[class_2.name]['probability'] 
class3_opt = optimals[class_3.name]['price'] * optimals[class_3.name]['probability'] 

plt.plot(np.cumsum(np.mean(class1_opt - rewards_per_experiment, axis=0)), label='Regret of the ' + class_1.name + ' model')
plt.plot(np.cumsum(np.mean(class2_opt - rewards_per_experiment, axis=0)), label='Regret of the ' + class_2.name + ' model')
plt.plot(np.cumsum(np.mean(class3_opt - rewards_per_experiment, axis=0)), label='Regret of the ' + class_3.name + ' model')
plt.plot(np.cumsum(np.mean(aggregate_opt - rewards_per_experiment, axis=0)), label='Regret of the aggregate model')

plt.xlabel('Time')
plt.ylabel('Regret')
plt.legend()
plt.show()
