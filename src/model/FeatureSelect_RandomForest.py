# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 13:09:06 2017

@author: Steff
"""

import ClassifierTemplate as ct
import pandas as pd

data = pd.read_csv("../../data/processed/train_set.csv", index_col=0)

# DataFrame containing label (!)
df = pd.DataFrame(data)

label_column = "productivity_binned_binary"

# Build Classifier object with DataFrame and column name of truth values
c = ct.Classifier(df,label_column)

### drop single columns not needed for Classification
c.dropColumns([
        "original_title"
        #,"adult"
        #,"belongs_to_collection"
        #,"budget"
        #,"runtime"
        #,"year"
        ,"quarter"
        ,"productivity_binned_multi"
        #,"productivity_binned_binary"
])

print(len(c.data.columns))
c.thresholdByColumn(3,"company")
c.thresholdByColumn(8,"actor")
c.thresholdByColumn(3,"director")
print(len(c.data.columns))

### scale something if needed
#c.scale([
#        "budget"
#])

### drop columns by prefix if needed
c.dropColumnByPrefix("belongs")
c.dropColumnByPrefix("actor")
c.dropColumnByPrefix("director")
c.dropColumnByPrefix("company")
#c.dropColumnByPrefix("country")
#c.dropColumnByPrefix("genre")
#c.dropColumnByPrefix("quarter_")



# lets print all non-zero columns of a movie to doublecheck
df = c.data.loc[19898]
df = df.iloc[df.nonzero()[0]]
print(df)
print(c.data.columns)

# get information about the data
c.balanceInfo()

# get parameters for GridSearch
scorer = c.f1(average="macro") # use F1 score with macro averaging
estimator = c.randomForest()
cv = c.fold(
        k=10
        ,random_state=42
) # KStratifiedFold with random_state = 42
# parameters to iterate in GridSearch
param_grid = {"max_depth": [None],
              "max_features": [10],
              "min_samples_split": [2],
              "min_samples_leaf": [1],
              "bootstrap": [False],
              "criterion": ["gini"]}
features = [
            "adult",
            #"belongs_to_collection",
            "budget",
            "runtime",
            "year",
            "actor_",
            "director_",
            "company_",
            "country_",
            "genre_",
            "quarter_"
]

# compute FeatureSelect
gs = c.featureselect_greedy(
        features
        ,param_grid
        ,scorer
        ,estimator
        ,cv
        ,label_column
)

#print(gs)




"""
    CURRENT BEST STATS
    -------------
    param_grid = {"max_depth": [None],
                  "max_features": [10],
                  "min_samples_split": [2],
                  "min_samples_leaf": [1],
                  "bootstrap": [False],
                  "criterion": ["gini"]}
    -------------
    CURRENT: 0.5929870756619212, MAX: 0.5860341040249972, FEATURE: runtime
    DROPPED: ['country_', 'actor_', 'director_']
"""