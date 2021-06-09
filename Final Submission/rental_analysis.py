#!/usr/bin/env python
# coding: utf-8

# # San Francisco Housing Cost Analysis
# 
# In this assignment, you will perform fundamental analysis for the San Francisco housing market to allow potential real estate investors to choose rental investment properties.

# In[ ]:


# imports
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np


# In[ ]:


# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("MAPBOX_API_KEY")


# ## Load Data

# In[ ]:


# Read the census data into a Pandas DataFrame
file_path = Path("..\Resources\sfo_neighborhoods_census_data.csv")
sfo_data = pd.read_csv(file_path, index_col="year")


# - - - 

# ## Housing Units Per Year
# 
# In this section, you will calculate the number of housing units per year and visualize the results as a bar chart using the Pandas plot function.
# 
# **Hint:** Use the Pandas `groupby` function.
# 
# **Optional challenge:** Use the min, max, and std to scale the y limits of the chart.
# 
# 

# In[ ]:


# Calculate the mean number of housing units per year (hint: use groupby) 
mean_housing_units_sfo = sfo_data.groupby(["year"]).mean()


# In[ ]:


# Save the dataframe as a csv file
mean_housing_units_sfo.to_csv(r"..\Resources\mean_housing_units_sfo.csv")


# In[ ]:


# Use the Pandas plot function to plot the average housing units per year.
mean_housing_units_sfo.plot.bar(y='housing_units',
                                ylim = (370000, 385000),
                                title = "Housing Units in San Francisco from 2010 to 2016")


# - - - 

# ## Average Housing Costs in San Francisco Per Year
# 
# In this section, you will calculate the average monthly rent and the average price per square foot for each year. An investor may wish to better understand the sales price of the rental property over time. For example, a customer will want to know if they should expect an increase or decrease in the property value over time so they can determine how long to hold the rental property.  Plot the results as two line charts.
# 
# **Optional challenge:** Plot each line chart in a different color.

# In[ ]:


# Calculate the average sale price per square foot and average gross rent
gross_rent = mean_housing_units_sfo["gross_rent"]


# In[ ]:


sale_price_sqr_foot = mean_housing_units_sfo["sale_price_sqr_foot"]


# ### Create two line charts, one to plot the average sale price per square foot and another for average montly rent

# In[ ]:


# Line chart for average sale price per square foot
gross_rent.plot.line(y='gross_rent',
                     ylim = (1100, 4500),
                     title = "Average Gross Rent by Year",
                     colormap='Spectral_r')


# In[ ]:


# Line chart for average montly rent
sale_price_sqr_foot.plot.line(y='sale_price_sqr_foot',
                                ylim = (300, 720),
                                title = "Average Price per SqFt by Year",
                                 colormap='cet_glasbey_dark')


# - - - 

# ## Average Prices by Neighborhood
# 
# In this section, you will use hvplot to create two interactive visulizations of average prices with a dropdown selector for the neighborhood. The first visualization will be a line plot showing the trend of average price per square foot over time for each neighborhood.  The second will be a line plot showing the trend of average montly rent over time for each neighborhood.
# 
# **Hint:** It will be easier to create a new DataFrame from grouping the data and calculating the mean prices for each year and neighborhood

# In[ ]:


# Group by year and neighborhood and then create a new dataframe of the mean values
average_price_by_neighborhood = sfo_data.groupby(['year','neighborhood']).mean()


# In[ ]:


# Use hvplot to create an interactive line chart of the average price per sq ft.
# The plot should have a dropdown selector for the neighborhood
average_price_by_neighborhood.hvplot.line(x="year",
                                          y="sale_price_sqr_foot",
                                          xlabel= "Year",
                                          ylabel="Average Price/Square Foot",
                                          groupby="neighborhood",
                                          color ='green')


# In[ ]:


# Use hvplot to create an interactive line chart of the average monthly rent.
# The plot should have a dropdown selector for the neighborhood
average_price_by_neighborhood.hvplot.line(x="year",
                                          y="gross_rent",
                                          xlabel= "Year",
                                          ylabel="Average Gross Rent per Year",
                                          groupby="neighborhood")


# ## The Top 10 Most Expensive Neighborhoods
# 
# In this section, you will need to calculate the mean sale price per square foot for each neighborhood and then sort the values to obtain the top 10 most expensive neighborhoods on average. Plot the results as a bar chart.

# In[ ]:


# Getting the data from the top 10 expensive neighborhoods to own
mean_neighborhood_sfo = sfo_data.groupby(["neighborhood"]).mean()
mean_sale_price_sfo = mean_neighborhood_sfo.sort_values("sale_price_sqr_foot", ascending=False)
sfo = mean_sale_price_sfo.head(10)


# In[ ]:


# Plotting the data from the top 10 expensive neighborhoods
sfo.hvplot.bar(y='sale_price_sqr_foot', title = "Top 10 Most Expensive Neighborhoods in SFO").opts(xrotation=90)


# - - - 

# ## Comparing cost to purchase versus rental income
# 
# In this section, you will use `hvplot` to create an interactive visualization with a dropdown selector for the neighborhood. This visualization will feature a side-by-side comparison of average price per square foot versus average montly rent by year.  
# 
# **Hint:** Use the `hvplot` parameter, `groupby`, to create a dropdown selector for the neighborhood.

# In[ ]:


# Fetch the previously generated DataFrame that was grouped by year and neighborhood
average_price_by_neighborhood


# In[ ]:


# Plotting the data from the top 10 expensive neighborhoods
average_price_by_neighborhood.hvplot.bar(x="year",
                                         y=["gross_rent",'sale_price_sqr_foot'],
                                         xlabel= "Neighborhood",
                                         ylabel="Average Gross Rent per Year",
                                         groupby="neighborhood",
                                         title="Top 10 Expensive Neighborhoods in SFO").opts(xrotation=90)


# - - - 

# ## Neighborhood Map
# 
# In this section, you will read in neighborhoods location data and build an interactive map with the average house value per neighborhood. Use a `scatter_mapbox` from Plotly express to create the visualization. Remember, you will need your Mapbox API key for this.

# ### Load Location Data

# In[ ]:


# Load neighborhoods coordinates data
file_path = Path("../Resources/neighborhoods_coordinates.csv")
df_neighborhood_locations = pd.read_csv(file_path)


# ### Data Preparation
# 
# You will need to join the location data with the mean values per neighborhood.
# 
# 1. Calculate the mean values for each neighborhood.
# 
# 2. Join the average values with the neighborhood locations.

# In[ ]:


# Calculate the mean values for each neighborhood
msp = mean_sale_price_sfo.reset_index()


# In[ ]:


# Join the average values with the neighborhood locations
avg_value_location = pd.concat([msp, df_neighborhood_locations], axis="columns", join="inner")


# ### Mapbox Visualization
# 
# Plot the average values per neighborhood using a Plotly express `scatter_mapbox` visualization.

# In[ ]:


# Set the mapbox access token
px.set_mapbox_access_token(map_box_api)


# In[ ]:


# Create a scatter mapbox to analyze neighborhood info
px.scatter_mapbox(
    avg_value_location,
    lat="Lat",
    lon="Lon",
    size="sale_price_sqr_foot",
    color="gross_rent",
    title="Average Sale Price per Square Foot and Gross Rent in San Francisco"
)


# - - -

# ## Cost Analysis - Optional Challenge
# 
# In this section, you will use Plotly express to create visualizations that investors can use to interactively filter and explore various factors related to the house value of the San Francisco's neighborhoods. 
# 
# ### Create a DataFrame showing the most expensive neighborhoods in San Francisco by year

# In[ ]:


# Fetch the data from all expensive neighborhoods per year.
a = sfo.reset_index()


# ### Create a parallel coordinates plot and parallel categories plot of most expensive neighborhoods in San Francisco per year
# 

# In[ ]:


# Parallel Categories Plot
px.parallel_categories(a,
                       color="sale_price_sqr_foot",
                       color_continuous_scale=px.colors.sequential.Inferno,
                       title='Average House Value/Neighborhood',
                       labels={'neighborhood': "Neighborhood", 'sale_price_sqr_foot':'Sales Price/Square Foot', 'housing_units':'Housing Units', 'gross_rent':'Gross Rent'})


# In[ ]:


# Parallel Coordinates Plot
px.parallel_coordinates(a, color='sale_price_sqr_foot')

