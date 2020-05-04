import matplotlib.pyplot as plt
import numpy as np

from project.dia_pckg.Campaign import Campaign
from project.dia_pckg.Class import Class
from project.dia_pckg.Config import *
from project.dia_pckg.Product import Product
from project.dia_pckg.User import User
from project.part_4.Env_4 import Env_4
from project.part_4.TS_Learner import TS_Learner

np.random.seed(23)
n_arms = 20

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
            #users_per_day=avg_users_per_day,
            users_per_day=50,
            class_1=class_1,
            class_2=class_2,
            class_3=class_3,
            n_arms=n_arms)

optimals = env.get_optimals()

plt.plot(env.classes['class_1'].conv_rates['phase_0']['prices'],
        env.classes['class_1'].conv_rates['phase_0']['probabilities'], label=class_1.name, linestyle='--')
plt.plot(env.classes['class_2'].conv_rates['phase_0']['prices'],
        env.classes['class_2'].conv_rates['phase_0']['probabilities'], label=class_2.name, linestyle='--')
plt.plot(env.classes['class_3'].conv_rates['phase_0']['prices'],
        env.classes['class_3'].conv_rates['phase_0']['probabilities'], label=class_3.name, linestyle='--')
plt.plot(env.aggregate_demand_curve['prices'],
        env.aggregate_demand_curve['probabilities'], label='aggregate')

plt.scatter(optimals['class_1']['price'],
            optimals['class_1']['probability'], marker='o', label=f'opt {class_1.name}')
plt.scatter(optimals['class_2']['price'],
            optimals['class_2']['probability'], marker='o', label=f'opt {class_2.name}')
plt.scatter(optimals['class_3']['price'],
            optimals['class_3']['probability'], marker='o', label=f'opt {class_3.name}')
plt.scatter(optimals['aggregate']['price'],
            optimals['aggregate']['probability'], marker='o', label='opt aggregate')

plt.xlabel('Price')
plt.ylabel('Conversion Rate')
plt.legend()
plt.show()

n_experiments = 200  # the number is small to do a raw test, otherwise set it to 1000
rewards_per_experiment = [] #collect all the rewards achieved from the TS 
optimals_per_experiment = [] #collect all the optimals of the users generated

for e in range(0, n_experiments):

    current_date, done = env.reset()
    ts_learner = TS_Learner(n_arms=n_arms, arm_prices=env.arm_prices['prices'])
    optimal_revenues = np.array([])

    while not done:
        # pulled_arm = ts_learner.pull_arm() #optimize by demand
        pulled_arm = ts_learner.pull_arm_revenue()  # optimize by revenue

        user = User(random=True)
        reward, current_date, done, opt_revenue = env.user_step(pulled_arm, user)
        
        ts_learner.update(pulled_arm, reward)
        optimal_revenues = np.append(optimal_revenues, opt_revenue)

    rewards_per_experiment.append(ts_learner.collected_rewards)
    optimals_per_experiment.append(optimal_revenues)

aggregate_opt = optimals['aggregate']['price'] * optimals['aggregate']['probability']
class1_opt = optimals['class_1']['price'] * optimals['class_1']['probability']
class2_opt = optimals['class_2']['price'] * optimals['class_2']['probability']
class3_opt = optimals['class_3']['price'] * optimals['class_3']['probability']

plt.plot(np.cumsum(np.mean(class1_opt - rewards_per_experiment, axis=0)),label='Regret of the ' + class_1.name + ' model')
plt.plot(np.cumsum(np.mean(class2_opt - rewards_per_experiment, axis=0)),label='Regret of the ' + class_2.name + ' model')
plt.plot(np.cumsum(np.mean(class3_opt - rewards_per_experiment, axis=0)),label='Regret of the ' + class_3.name + ' model')
plt.plot(np.cumsum(np.mean(aggregate_opt - rewards_per_experiment, axis=0)), label='Regret of the aggregate model')
plt.plot(np.cumsum(np.mean(optimals_per_experiment, axis=0) - np.mean(rewards_per_experiment, axis=0)), label='Regret of the true evaluation')

plt.xlabel('Time')
plt.ylabel('Regret')
plt.legend()
plt.show()
