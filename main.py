"""
Name: Nick Gavca
CS 230: Section SN1
Data Set: Skyscrapers around the World
URL:

Description:
This program analyzes the skyscrapers dataset by creating two different charts: scatter plot and barchart.
The scatter plot measures the relationship between the year the skyscraper was built and it's height. In addition,
user may choose what he/she desires to display on the page by checking the according radio button on the sidebar(r-value,
min,max,mean, standard deviation). The bar chart allows the user to choose the specific countries and its skyscrapers
to display as well as set the height limit for the skyscrapers using the slider.
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# reads the data from the csv file
def read_data(filename):
    df = pd.read_csv(filename)
    lst = []
    columns = ["Name", "Country", "Metres", "City", "Lat", "Lon",]
    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)
    return lst

# creates a list of all countries
def countries_list(data):
    countries = []
    for i in range(len(data)):
        if data[i][1] not in countries:
            countries.append(data[i][1])

    return countries

# gets the number of skyscrapers in each country
def freq_data(data, countries, height):
    freq_dict = {}

    for country in countries:
        freq = 0
        for i in range(len(data)):
            if data[i][1] == country and height >= data[i][2]:
                freq += 1
        freq_dict[country] = freq

    return freq_dict

# bar chart displaying how many skyscrapers each building has
def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.xlabel("Countries")
    plt.ylabel("Number of Skyscrapers")
    plt.title("Skyscrapers around the World")
    return plt

# scatterplot the showcases the realtionship between the year the skyscraper was built and it's height
def scatter_plot():
    plt.xlabel("Year Built")
    plt.ylabel("Height of the Skyscraper")
    scatter = pd.read_csv("skyscrapers.csv")
    x = scatter["Year"]
    y = scatter["Metres"]
    plt.xticks(rotation=45)
    plt.title(f"Relationship between the year built and height")
    plt.scatter(x, y, marker="X", color="red")
    return plt

# function that uses the numpy module to return the r-value of the dataset
def statistics():
    df = pd.read_csv("skyscrapers.csv")
    height = np.array(df["Metres"])
    year_built = np.array(df["Year"])
    correlation = np.corrcoef(year_built, height)
    return round(correlation[0][1], 2)

# putting all the functions together
def main():
    data = read_data("skyscrapers.csv")
    st.title("Skyscrapers Web Application")
    st.write("Welcome!")
    st.sidebar.title("Sidebar")
    df = pd.DataFrame(data, columns=["Name", "Country", "Height", "City", "Lat", "Lon"])
    st.dataframe(df)
    st.subheader("Scatter Plot")
    st.pyplot(scatter_plot())
    scatter_data = pd.read_csv("skyscrapers.csv")
    stats = st.sidebar.radio("Select statistics that you would like to display?",
                             ("R-value", "Average Height", "Min Height", "Max Height", "Standard Deviation"))
    # displaying the statistic that the user chose
    if stats == "R-value":
        st.write("The r-value is:", statistics())
    elif stats == "Average Height":
        st.write("The average height for all skyscrapers is:", round(scatter_data["Metres"].mean(), 2), "meters")
    elif stats == "Min Height":
        st.write("The smallest skyscraper is:", round(scatter_data["Metres"].min(), 2), "metres")
    elif stats == "Max Height":
        st.write("The highest skyscraper is:", round(scatter_data["Metres"].max(), 2), "metres")
    elif stats == "Standard Deviation":
        st.write("The standard deviation for all skyscrapers is:", round(np.std(scatter_data["Metres"]), 2), "meters")

    # user selects which countries he/she wants to display in the bar chart
    countries = st.sidebar.multiselect("Select Countries to Display", countries_list(data))
    heightLimit = st.sidebar.slider("Set The Height Limit for Skyscrapers", 50, 1000)
    if len(countries) > 0:
        st.subheader("Bar Chart")
        st.pyplot(bar_chart(freq_data(data, countries, heightLimit)))


main()
