#!/usr/bin/env python
# coding: utf-8

# # San Francisco Rental Prices Dashboard
# 
# In this notebook, you will compile the visualizations from the previous analysis into functions that can be used for a Panel dashboard.

# In[1]:


# imports
import panel as pn
from panel.interact import interact
from panel import widgets
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv


# In[2]:


# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("MAPBOX_API_KEY")
px.set_mapbox_access_token(map_box_api)


# # Import Data

# In[16]:


# Import the necessary CSVs to Pandas DataFrames
file_path1 = Path("..\Resources\sfo_neighborhoods_census_data.csv")
file_path2 = Path("..\Resources\mean_housing_units_sfo.csv")
file_path3 = Path("../Resources/neighborhoods_coordinates.csv")
file_path4 = Path("..\Resources\sfo_neighborhoods_census_data_1.csv")
sf_data = pd.read_csv(file_path4, index_col="value")
sfo_data = pd.read_csv(file_path1, index_col="year")
mean_housing_units_sfo = pd.read_csv(file_path2)
df_neighborhood_locations = pd.read_csv(file_path3)


# - - -

# ## Panel Visualizations
# 
# In this section, you will copy the code for each plot type from your analysis notebook and place it into separate functions that Panel can use to create panes for the dashboard. 
# 
# These functions will convert the plot object to a Panel pane.
# 
# Be sure to include any DataFrame transformation/manipulation code required along with the plotting code.
# 
# Return a Panel pane object from each function that can be used to build the dashboard.
# 
# Note: Remove any `.show()` lines from the code. We want to return the plots instead of showing them. The Panel dashboard will then display the plots.

# In[20]:


# Define Panel Visualization Functions
def housing_units_per_year():
    """Housing Units Per Year."""
    mean_housing_units_sfo
    return mean_housing_units_sfo.hvplot.bar(x="year", y="housing_units", xlabel= "Year", ylabel="housing_units", ylim = (370000, 385000), title = "Housing Units in San Francisco from 2010 to 2016")

def average_gross_rent():
    """Average Gross Rent in San Francisco Per Year."""
    gross_rent = mean_housing_units_sfo["gross_rent"]
    return gross_rent.hvplot.line(y="gross_rent", xlabel= "Year", ylabel="gross_rent", ylim = (1100, 4500), title = "Average Gross Rent by Year")   

def average_sales_price():
    """Average Sales Price Per Year."""
    sale_price_sqr_foot = mean_housing_units_sfo["sale_price_sqr_foot"]
    return sale_price_sqr_foot.hvplot.line(y="sale_price_sqr_foot", xlabel= "Year", ylabel="sale_price_sqr_foot", ylim = (300, 720), title = "Average Price per Square Foot by Year",)  

def average_price_by_neighborhood():
    """Average Prices by Neighborhood."""
    average_price_by_neighborhood = sfo_data.groupby(['year','neighborhood']).mean()
    return average_price_by_neighborhood.hvplot.line(x="year", y="sale_price_sqr_foot", xlabel= "Year", ylabel="Average Price/Square Foot", groupby="neighborhood") 

def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""
    mean_neighborhood_sfo = sfo_data.groupby(["neighborhood"]).mean()
    mean_sale_price_sfo = mean_neighborhood_sfo.sort_values("sale_price_sqr_foot", ascending=False)
    sfo = mean_sale_price_sfo.head(10)
    
    top_10 = sfo.hvplot.bar(y='sale_price_sqr_foot', ylim= (100, 1500), title = "Top 10 Most Expensive Neighborhoods in SFO").opts(xrotation=90)
    return top_10

def most_expensive_neighborhoods_rent_sales():
    """Comparison of Rent and Sales Prices of Most Expensive Neighborhoods."""   
    average_price_by_neighborhood = sfo_data.groupby(['year','neighborhood']).mean()
    return average_price_by_neighborhood.hvplot.bar(x="year", y=["gross_rent",'sale_price_sqr_foot'], xlabel= "Neighborhood", ylabel="Average Gross Rent per Year", groupby="neighborhood", title="Top 10 Expensive Neighborhoods in SFO").opts(xrotation=90)

def parallel_coordinates():
    """Parallel Coordinates Plot."""
    mean_neighborhood_sfo = sfo_data.groupby(["neighborhood"]).mean()
    mean_sale_price_sfo = mean_neighborhood_sfo.sort_values("sale_price_sqr_foot", ascending=False)
    sfo = mean_sale_price_sfo.head(10)
    a = sfo.reset_index()
    parallel_coordinates_top_10 = px.parallel_coordinates(a, color='sale_price_sqr_foot')
    return parallel_coordinates_top_10
    
def parallel_categories():
    """Parallel Categories Plot."""
    mean_neighborhood_sfo = sfo_data.groupby(["neighborhood"]).mean()
    mean_sale_price_sfo = mean_neighborhood_sfo.sort_values("sale_price_sqr_foot", ascending=False)
    sfo = mean_sale_price_sfo.head(10)
    a = sfo.reset_index()
    parallel_categories_top_10 = px.parallel_categories(a, color="sale_price_sqr_foot", color_continuous_scale=px.colors.sequential.Inferno, title='Average House Value/Neighborhood', labels={'neighborhood': "Neighborhood", 'sale_price_sqr_foot':'Sales Price/Square Foot', 'housing_units':'Housing Units', 'gross_rent':'Gross Rent'})
    return parallel_categories_top_10
  
def neighborhood_map():
    """Neighborhood Map."""
    mean_neighborhood_sfo = sfo_data.groupby(["neighborhood"]).mean()
    mean_sale_price_sfo = mean_neighborhood_sfo.sort_values("sale_price_sqr_foot", ascending=False)
    msp = mean_sale_price_sfo.reset_index()
    avg_value_location = pd.concat([msp, df_neighborhood_locations], axis="columns", join="inner")
    px.set_mapbox_access_token(map_box_api)
    maps = px.scatter_mapbox(
    avg_value_location,
    lat="Lat",
    lon="Lon",
    size="sale_price_sqr_foot",
    color="gross_rent",
    title="Average Sale Price per Square Foot and Gross Rent in San Francisco"
    )
    return maps

def sunburst():
    """Sunburst Plot."""
    fig = px.sunburst(sf_data, path=['year', 'neighborhood'],
                  color='gross_rent',
                  color_continuous_scale='RdBu', title = "Cost Analysis of Most Expensive Neighborhoods in San Francisco per Year")
    return fig


# ## Panel Dashboard
# 
# In this section, you will combine all of the plots into a single dashboard view using Panel. Be creative with your dashboard design!

# In[24]:


# Create a Title for the Dashboard
title = '##Real Estate Analysis of San Francisco from 2010-2016'


# Create a tab layout for the dashboard
welcome_tab = pn.Column((title),
                        neighborhood_map(),
                        background='grey')

neighborhood_analysis_tab = pn.Column(average_price_by_neighborhood(),
                                      top_most_expensive_neighborhoods(),
                                      most_expensive_neighborhoods_rent_sales())

market_analysis_row = pn.Row(housing_units_per_year(),
                             average_gross_rent(),
                             average_sales_price())

parallel_plots_tab = pn.Column(parallel_categories(),
                               parallel_coordinates())

sunburst_tab = pn.Column(sunburst())
                              
# Create the dashboard
SF_dashboard = pn.Tabs(("Welcome", welcome_tab), 
("Yearly Market Analysis", market_analysis_row),
("Neighborhood Analysis", neighborhood_analysis_tab), 
("Interactive Market Analysis by Neighborhood", parallel_plots_tab),
("Whole Market Analysis", sunburst_tab))


# ## Serve the Panel Dashboard

# In[25]:


# Serve the# dashboard
SF_dashboard.servable()


# # Debugging
# 
# Note: Some of the Plotly express plots may not render in the notebook through the panel functions.
# 
# However, you can test each plot by uncommenting the following code

# In[7]:


#housing_units_per_year()


# In[8]:


#average_gross_rent()


# In[9]:


#average_sales_price()


# In[10]:


#average_price_by_neighborhood()


# In[11]:


#top_most_expensive_neighborhoods()


# In[12]:


#most_expensive_neighborhoods_rent_sales()


# In[13]:


#neighborhood_map().show()


# In[14]:


#parallel_categories()


# In[15]:


#parallel_coordinates()


# In[19]:


#sunburst()

