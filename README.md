
# Data Intelligence Applications

## Team 15
---
| Surname   | Name      | Contact Info                      |
|:----------|:----------|:----------------------------------|
| Bionda    | Andrea    | andrea.bionda@mail.polimi.it      |
| Derin     | Damiano   | damiano.derin@mail.polimi.it      |
| Diecidue  | Andrea    | andrea.diecidue@mail.polimi.it    |
| Urbano    | Antonio   | antonio.urbano@mail.polimi.it     |
| Voltan    | Enrico    | enrico.voltan@mail.polimi.it      |


## Description
---
This repository contains the implementation of the project [Pricing + Advertising](project/README.md) for the year 2019/2020 of the course Data Intelligence Application held at Politecnico di Milano.

The full description of our implementation is contained in [report.pdf](report/report.pdf).

## Usage
---
Execute the project
* PART: part to execute, one of: '2', '3', '4', '5', '6', '7_n' (part 7 normal), '7_b' (part 7 binomial) or 'all' (execute all the parts in sequence)
* EXPERIMENTS: number of different experiments for each part
* SEED: seed parameter (optional)

```sh
cd DataIntelligenceApplications
python TestingOneShot.py -p PART -e EXPERIMENTS -s SEED
```
It is possible to configure other implementation parameters in [Config.py](project/dia_pckg/Config.py).

In [this](project/results_charts) directory will be saved the charts of the execution.

## Installation
Clone and install: 
```sh
git clone https://github.com/damiano9669/DataIntelligenceApplications.git
cd DataIntelligenceApplications
pip install -r requirements.txt
```

## Requirements
* scikit-learn==0.20.0
* seaborn>=0.10.1
* numpy>=1.18.5
* pandas>=1.1.1
* scipy>=1.4.1
* matplotlib>=3.3.1