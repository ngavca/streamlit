"""
Name: Nick Gavca
MA346: Section 3
Data Set: Skyscrapers around the World
URL: https://share.streamlit.io/ngavca/streamlit/main/main.py

Description:
This project analyzes the skyscrapers dataset taken from kaggle database by creating a dataframe with two different charts: scatter plot and barchart.
The scatter plot measures the relationship between the year the skyscraper was built and it's height. In addition,
user may choose what he/she desires to display on the page by checking the according radio button on the sidebar(r-value,
min,max,mean, standard deviation). The bar chart allows the user to choose the specific countries and its skyscrapers
to display as well as set the height limit for the skyscrapers using the slider"
"""
# First we need to import the necessary modules for this project
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# The modules have now been imported and we can start creating the functions that we would need for our analysis.

# Before we start building graphs,we first need to create a function that would read in the data when we compile our main function
# as well as clean the data a bit by choosing which columns we want to use in our analysis
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
# We have successfully create the read_data function which reads the csv file data and did some cleaning by choosing
# only the columns that we need in our data such as the "Name", "Country", "Metres", "City", "Lat", "Lon" columns

# Next we need to create a function that would read in the all the skyscrapers and create a list that we can use
# for our sidebar.multiselect feature that we will use later in our main function. This will enable the user to choose
# which countries he/she wants to be displayed in the bargraph in order to compare the amount of skyscrapers each country has.
def countries_list(data):
    countries = []
    for i in range(len(data)):
        if data[i][1] not in countries:
            countries.append(data[i][1])

    return countries
# Now that the countries_list function is created, we will be able to create a sidebar on our streamLit app that would allow
# the user to choose which country he/she wants to display into the app fro comparison reasons

# Next we want to get the number of skyscrapers in each country so that we can display the barchart depending on what the user chose.
def freq_data(data, countries, height):
    freq_dict = {}

    for country in countries:
        freq = 0
        for i in range(len(data)):
            if data[i][1] == country and height >= data[i][2]:
                freq += 1
        freq_dict[country] = freq

    return freq_dict
# We have created a dictionary with all the countries and amount of skyscrapers each country has.

# Next we want to create a function that we will use later on in our main function in order to display the bar graph
# with the number of skyscrapers each country has
def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.xlabel("Countries")
    plt.ylabel("Number of Skyscrapers")
    plt.title("Skyscrapers around the World")
    return plt
# We have created a function that would display bar graph in the streamLit app and added the labels and a title.

# Next we want to create a function that would display a scatter plot that would illustrate the relationship between the year the skyscraper was built
# and its height. Thus, we want to see if there is a positive correlation between the year and the height of the skyscraper.
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
# We have created a function that displays the year and height of the skyscraper that was built during that year to see if there
# is any correlation between the year and height

# Next we want to create a function that would calculate the r-value between teh year and height of the skyscraper.
# We will use the numpy module in order to calculate that value
def statistics():
    df = pd.read_csv("skyscrapers.csv")
    height = np.array(df["Metres"])
    year_built = np.array(df["Year"])
    correlation = np.corrcoef(year_built, height)
    return round(correlation[0][1], 2)
# We have created a function that calculates the r-value and we can now use it in our main function to display it on the streamLit app.

# Now that we have all the functions created, we will put all the previous functions into the main function and so that we can display all our
# analysis and results on the streamLit app
def main():
    # we will read in the data and display it in our streamLit app using the streamLit module
    data = read_data("skyscrapers.csv")
    st.title("Skyscrapers Web Application")
    st.write("Welcome!, This project analyses a dataset containing the tallest skyscrapers around the world")
    st.sidebar.title("Sidebar")
    df = pd.DataFrame(data, columns=["Name", "Country", "Height", "City", "Lat", "Lon"])
    st.dataframe(df)
    st.subheader("Scatter Plot")
    st.pyplot(scatter_plot())
    scatter_data = pd.read_csv("skyscrapers.csv")
    stats = st.sidebar.radio("Select statistics that you would like to display? P.S China and U.S has the most skyscrapers.",
                             ("R-value", "Average Height", "Min Height", "Max Height", "Standard Deviation"))
    # displaying the statistic that the user chose
    if stats == "R-value":
        st.write("The r-value is:", statistics(), " which indicates that while there is a positive correlation between the year and height of the skyscraper, it is quite weak.")
    elif stats == "Average Height":
        st.write("The average height for all skyscrapers is:", round(scatter_data["Metres"].mean(), 2), "meters")
    elif stats == "Min Height":
        st.write("The shortest skyscraper is:", round(scatter_data["Metres"].min(), 2), "metres")
    elif stats == "Max Height":
        st.write("The tallest skyscraper is:", round(scatter_data["Metres"].max(), 2), "metres")
    elif stats == "Standard Deviation":
        st.write("The standard deviation for all skyscrapers is:", round(np.std(scatter_data["Metres"]), 2), "meters")

    # user selects which countries he/she wants to display in the bar chart
    countries = st.sidebar.multiselect("Select Countries to Display", countries_list(data))
    heightLimit = st.sidebar.slider("Set The Height Limit for Skyscrapers", 350, 830)
    if len(countries) > 0:
        st.subheader("Bar Chart")
        st.pyplot(bar_chart(freq_data(data, countries, heightLimit)))
# we have put all the functions together and now we are ready to call the main function to finish it off
main()
