### Title of the Report
<p align="center"><b>
 Enrico Voltan <sup>[1]</sup>,
 Damiano Derin <sup>[2]</sup>, 
 Antonio Urbano <sup>[3]</sup>, 
 Andrea Diecidue <sup>[4]</sup>, 
 Andrea Bionda <sup>[5]</sup>
</b></p>

[1] enrico.voltan@mail.polimi.it<br>
[2] damiano.derin@mail.polimi.it<br>
[3] antonio.urbano@mail.polimi.it<br>
[4] andrea.diecidue@mail.polimi.it<br>
[5] andrea.bionda@mail.polimi.it<br>

#### Abstract
The goal of the project is to model a scenario in which a seller exploits advertising tools in order to attract
more and more users to its website, thus increasing the number of possible buyers.
The seller has to learn simultaneously the conversion rate and the number of users the advertising tools can attract.
In this report, we walk through the description of the specific scenario we have studied and the definition 
of the algorithm design choices we adopted in order to reach our goal.
Then the achieved experimental results will be presented via some useful plots and 
a final conclusion summarizing the whole work.

#### 1. Introduction

We have studied a possible real world scenario in which a seller wants to increase the number of possible buyers 
by exploiting advertising tools. The product we have considered is a particular pair of shoes 
which has a production cost (without loss of generality we can assume that the production cost is null) and a sell price.
<br>
The analysed campaign consists of three sub-campaigns, each with a different ad to advertise the product
and each targeting a different class of users. 
Each class is defined by the values of pre-defined features.<br>
The feature space we have considered is characterized by two binary features: 
* *Age>30* or *Age<30*
* Profession that can be either *student* or *worker*
<br>

So according to the values of the above described features, we can distinguish among the following classes of users:
* *Elagant*: a worker with age>30
* *Casual*: a student with age<30
* *Sport*: a worker with age<30
<br>

#### 2. Algorithm design choices and Results
This section deals with the description of the algorithm design choices we adopted and
it also contains the most relevant reference to the code.
For the description we will adopt the following structure: for each sub-section we will describe the actual scenario
we are interested in by defining its goals and then we focus on how we have solved the problem and 
the results we have obtained.
##### 2.1 Budget allocation optimization
The goal of this part is to design a combinatorial bandit algorithm to optimize the budget allocation
over the three sub-campaigns in order to maximize the total number of clicks.
For this section we can assume, for simplicity,that there is only one phase.
<p>
First of all in the class <i>BiddingEnvironment.py</i>, which extends the class <i>Environment.py</i> we have defined 
the actual environment we are working in, with the definition of the bids space and the three curves we want to learn,
one for each sub-campaign.
The function we want to estimate, i.e. the functions mapping a value of bid(x) to the corresponding
expected number of clicks have been defined in the <i>SubCampaign.py</i> class.<br>
As follows the mathematical formulation the curves of the function generating  the number of clicks given a bid value
and the plots of the three curves (one for each sub-campaign):
</p>
<i><b>curve = max_n_clicks * (max_value - np.exp(-param * x))</b></i>

where:
<ul>
<li><i><b>max_n_clicks</b></i>: is the maximum number of clicks the considered sub-campaign can reach in a day</li>
<li><i><b>max_value</b></i> and <i><b>param</b></i>: are values associated to each sub-campaign defining the actual bidding curve</li>
</ul>
<br>

[TODO: 3 FUNCTIONS PLOT]

<br>

<p>
In order to find the best budget allocation over the three sub-campaigns able to maximize the total number of clicks,
we have designed a combinatorial bandit algorithm.
<br>
In the first phase of the algorithm we learn the model of each sub-campaign from the observation we get.
To do that we have used a GP_Learner that, for each sub-campaign, given the index of the pulled arm, 
i.e. the index of the chosen bid, returns the reward.
Afterward, the model of each sub-campaign is updated using those observations.
<br>
In the second phase of the algorithm we have used the values of learned model to solve the problem of
finding the best budget allocation to be set for the current day.
<br>
In the <i>Optimizer.py</i> class we have implemented a modified version of the dynamic programming algorithm 
used for solving the knapsack problem.
<br>
More precisely,we have used a matrix in which each row represent the fact that at each step a new sub-campaign
enters the problem, while in the columns we have the values of 20 possible budget allocation (we have discretized the 
whole budget in 20 possible uniformly distributed combinations of budget allocation).
<br>
Then for each cell of the matrix, we have to find the value of the best allocation of that cell. 
The result is given by the maximization of the sum of the values provided by the best solution of the problem solved in
the previous row (i.e. without considering the new entered sub-campaign) and 
the value of the new considered sub-campaign (considered singularly) s.t. the daily budget over the three sub-campaigns
sums to the total daily budget.
<br>
Once we have filled the entire table, we have the best solution in the last row, 
i.e. when all the 3 sub-campaigns are considered.
</p>

####### Performance evaluation

<p>
Finally, in order to evaluate the performance of the algorithm we have computed the <u>cumulative regret</u> as the difference
between the expected reward of the <i>Clairvoyant algorithm</i> and the expected reward of the implemented 
combinatorial bandit algorithm. 
<br>
As follows the plot of the cumulative regret
</p>

####### [TODO: CUMULATIVE REGRET PLOT] + "Eventuali Considerazioni"  


##### 2.2 Budget allocation optimization and abrupt phases
<p>
The object of this section is the design a sliding-window combinatorial bandit algorithm for 
optimizing the budget allocation over the three sub-campaigns in order to maximize the total number of clicks,
in the case in which there are the three abrupt phases. 
</p>

<p>
For addressing this task we started from the simplified case of one single phase solved in the previous section and 
we extended it in order to take in consideration the more general scenario of multiple phases.
<br>
For this purpose we have implemented the <i>AbruptBiddingEnvironment.py</i> class which
extends the <i>BiddingEnvironment.py</i> class. This class works in a scenario of multiple abrupt phases by 
returning, for each sub-campaign, the reward of a given pulled arm, depending on the phase we are.
<br>
In this case, the functions generating  the number of clicks given a bid value can change dynamically, according
the phase we are in.
As follows the mathematical formulation and the plots of the three curves (one for each sub-campaign):
</p>
<i><b>curve = max_n_clicks * (max_value[phase] - np.exp(-param[phase] * x))</b></i>
<br>
We can notice that now the <i>max_value</i> and <i>param</i> variables depends on the phase we are in.
<br>

######### [TODO: 3 FUNCTIONS PLOT]

<br>

<p>
In order to learn the three curves in the case of multiple abrupt phase, we have implemented the <i>DynamicLerner.py</i>
class as an extension of the standard GP_Learner.
<br>
It implements a sliding window mechanism in which we pull a new arm and add the collected rewards until
the length of the window is reached. When the window is full, for each new pulled arm we get, we delete the last recent value
and add the new one to the collected rewards.
</p>

<h6>Another implementation: Changes Detection</h6>
For solving this problem we have implemented, in the <i>DLChangeDetect.py</i> class, an innovative method 
which is based on the concept of the Statistical test.
<br>
We recall that a statistical test is a procedure for deciding whether a hypothesis about a quantitative feature
of a population is true or false. Then for testing a hypothesis, we draw a random sample and calculate an appropriate
statistic on its items. If, in doing so, we obtain a value of the statistic that would occur rarely when the hypothesis
is true, we would have reason to reject the hypothesis.
<br>
To detect change in our scenario, we need to compare the value of the new drawn sample with the distribution of 
the points belonging to the same arm in order to decide whether the hypothesis H<sub>0</sub>,that the new drawn point  
belongs to that distribution, is true.
<br>
Let us suppose to draw a sample whose value is x<sub>0</sub> and let μ and σ<sup>2</sup> be respectively the average
and the standard deviation of the the distribution of the points belonging to the pulled arm. 
If the point doesn't belong to that distribution the hypothesis test should reject H<sub>0</sub>, 
with a confidence interval of [TODO: CONFIDENCE INTERVAL]%. So we have:
<br>

<p align="center">
Pr[(|x<sub>0</sub> - μ| / sqrt(σ<sup>2</sup>) > h)] = [TODO: p-value]
</p>

We have that the critical z-score when using a c confidence level are [TODO: z-score asssociated] standard deviations.

In the <i>DLChangeDetect.py</i> class we have implemented such change detector. When an arm is pulled more than 
<i>'min_len'</i> times (min_len indicates the minimum number of data we considering in an arm), 
for each pull we run the statistical test. When the test reject H<sub>0</sub>, it means that the point doesn't belong 
to that distribution and so it means that it is changed. In this case we reset the arm 
<br>

####### Performance evaluation

<p>
In order to evaluate the performance of the algorithm, we have computed the <u>cumulative regret</u> as the difference
between the expected reward of the <i>Clairvoyant algorithm</i> and the expected reward of the implemented algorithms. 
In the plot we can see the comparison of the cumulative regrets in the three cases:
<uo>
<li>Combinatorial bandit algorithm without sliding window</li>
<li>Combinatorial bandit algorithm with sliding window</li>
<li>Change detection implementation</li>
</uo> 
<br>
</p>

######### [TODO: REGRET OF PART 3] + "Eventuali Considerazioni" 

##### 2.3 Learning the price
Design a learning algorithm for pricing when the users that will 
buy the product are those that have clicked on the ads. 
Assume that the allocation of the budget over the three subcampaigns is 
fixed and there is only one phase (make this assumption also in the next steps). Plot the cumulative regret.

##### 2.4 Context generation algorithm for pricing
Design and run a context generation algorithm for the pricing when 
the budget allocated to each single subcampaign is fixed. 
At the end of every week, use the collected data to generate contexts and then
use these contexts for the following week. Plot the cumulative regret as time increases. 
In the next steps, do not use the generated contexts, but use all the data together.

##### 2.5 Budget allocation & Pricing
Design an optimization algorithm combining the allocation of budget and the pricing when the seller 
a priori knows that every subcampaign is associated with a different context and charges a different price 
for every context. Suggestion: the value per click to use in the knapsack-like problem depends 
on the pricing, that depends on the number of users of a specific class interested in buying the product.
Notice that the two problems, namely, pricing and advertising, can be decomposed since 
each subcampaign targets a single class of users, thus allowing the computation of
the value per click of a campaign only on the basis of the number of clicks generated by that subcampaign. 
Plot the cumulative regret when the algorithm learns both the conversion rate curves 
and the performance of the advertising subcampaigns.

##### 2.6 Budget allocation & Pricing with fixed price
Do the same of Step 6 under the constraint that the seller charges a unique price to all
 the classes of users. Suggestion: for every possible price, fix this price and repeat the algorithm used 
 in Step 6. Plot the cumulative regret when the algorithm learns both the conversion rate curves and the 
 performance of the advertising subcampaigns.

