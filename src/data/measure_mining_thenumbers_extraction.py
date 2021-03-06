# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:43:26 2017

@author: Steff
"""

import pandas as pd

movies = pd.read_csv("../../data/external/thenumbers_measures.csv", index_col=0)

# extract budgets
#budget = movies["raw"][0:10].str.replace(r".+Budget</h5>\\n([$,0-9]+) \(.+",r"\1")
budget = movies["raw"]
budget = budget[budget.str.contains("Production&nbsp;Budget").fillna(False)]
budget = budget.str.replace(r".+?<b>Production&nbsp;Budget:</b></td><td>([$,0-9]+)</td>.*",r"\1")
budget = budget.str.replace(r"[$,]","")

# budget

df_budget = pd.DataFrame(budget)
df_budget = df_budget.dropna()

# df_budget

# extract revenue
revenue = movies["raw"]
revenue = revenue[revenue.str.contains("<b>Worldwide Box Office</b>").fillna(False)]
revenue = revenue.str.replace(r'.+?<td><b>Worldwide Box Office</b></td>\\n<td class="data">([$,0-9]+)</td>.*',r"\1")
revenue = revenue.str.replace(r"[$,]","")

df_revenue = pd.DataFrame(revenue)
df_revenue = df_revenue.dropna()

# join and save file
joined = df_budget.join(df_revenue,how="inner",lsuffix="_budget",rsuffix="_revenue")

# extract year
year = movies["raw"][joined.index.values]
year = year[year.str.contains('<h1 itemprop="name">').fillna(False)]
year = year.str.replace(r'.+?<h1 itemprop="name">.+\(([0-9]{4})\)</h1>.*',r"\1")
df_year = pd.DataFrame(year)
df_year = df_year.dropna()

joined = joined.join(df_year,how="left",lsuffix="",rsuffix="_year")
joined.to_csv("../../data/external/thenumbers_measures_extracted.csv", encoding="utf-8")