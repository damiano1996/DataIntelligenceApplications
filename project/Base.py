import numpy as np
import matplotlib.pyplot as plt

#Set seed to have always the same behaviour
#np.random.seed(123)

class Product:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price  = base_price


class Class:
    def __init__(self, name, profession, age):
        self.name = name
        self.profession  = profession
        self.age  = age

    """Generate the conversione rate curve associated to the class and the product
    product: Product to advertise
    max_rate: Maximum probability value of the conversione rate
    noise: Noise applied to the curve
    length: Number of prices evalueted by the curve
    """
    def define_conversion_rate(self, product, max_rate, noise, length):
        start_curve = np.exp(max_rate)
        arr = np.linspace(start_curve, 1.0, length)
        log_arr = np.log(arr)
        noise = np.random.normal(0,noise,length)
        price = np.linspace(product.base_price, product.base_price + length, length)
        self.conv_rate = (price , log_arr + noise)

    def plot_conversion_rate(self):
        plt.plot(self.conv_rate[0] , self.conv_rate[1])
        plt.show()


class SubCampaign:
    def __init__(self, Class):
        self.Class = Class
        
    """Generate the clicks over budget curve associated to the sub campaign
    max_n_click: Define the maximum number of click of the curve
    max_budget: Define the maximum budget of the curve
    zero_perc: Define the percentage of the curve (first part) that is zero
    full_perc: Define the percentage of the curve (last part) that is at the max_n_click
    length: Number of budgetes evalueted by the curve
    """
    def define_clicks_over_budget(self, max_n_click, max_budget, zero_perc, full_perc, noise, length):
        budget = np.linspace(0, max_budget, length)

        zero = np.zeros(int(length*zero_perc))

        line = np.linspace(0, max_n_click, int(length*(full_perc-zero_perc)))
        noise = np.random.normal(0,noise,int(length*(full_perc-zero_perc)))
        line = line + noise

        plate = np.full(length-len(line)-len(zero), max_n_click)

        clicks = np.append(zero, line)
        clicks = np.append(clicks, plate)
        self.cob_curve = (budget, clicks)

    def plot_clicks_over_budget(self):
        plt.plot(self.cob_curve[0] , self.cob_curve[1])
        plt.show()



prod = Product('shoes', 30)

c1 = Class('elegant', 'worker', 'adult')
c1.define_conversion_rate(prod, 0.85, 0.01, 50)

c1.plot_conversion_rate()



sub = SubCampaign(c1)
sub.define_clicks_over_budget(50, 100, 0.3, 0.8, 0.5, 50)

sub.plot_clicks_over_budget()