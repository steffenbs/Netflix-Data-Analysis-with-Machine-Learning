import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def all_years():
    return ["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"] #All the years that content has been added to neflix

def all_months():
    return ["January","February","March","April","May","June","July","August","September","October","November","December"] #All months in a year

def valid_dates(dataframe):
    """
    Returns the dataframe where entries with "Uknown date_added" are removed
    """
    dataframe = dataframe[dataframe.date_added != "Unknown date_added"]
    return dataframe

def create_year_column(dataframe):
    """
    Returns the dataframe with a new column addition containing information about the year the content was added
    """
    dataframe["year"] = dataframe["date_added"].apply(lambda x: x.split(", ")[-1])  #Lambda: Iterates though every entry. Splits by comma and extracts the last value (which is year)
    return dataframe

def create_month_column(dataframe):
    """
    Returns the dataframe with a new column addition containing information about the month the content was added
    """
    dataframe["month"] = dataframe["date_added"].apply(lambda x: x.lstrip().split(" ")[0]) #Remove leading whitespace using lstrip(), then using split by whitespace and extracting the first value
    return dataframe 


def monthly_yearly_table(dataframe):
    """
    Return a new dataframe shaped as a table of years vs months of the added content
    """
    df = dataframe.groupby("year") #Combining the 
    df = df['month'].value_counts() #count values in month
    df = df.unstack() 
    df = df.fillna(0) #fill nans with 0
    return df


def heatmap(dataframe,title,xlab,ylab):
    """
    Creates a heatplot from a "tabled" dataframe (ref to monthly_yearly_table)
    """
    plt.figure(figsize=(15,15))
    plt.pcolor(dataframe, cmap="Greens", edgecolors = "white",linewidths=2) #Source: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolor.html
    plt.xticks(np.arange(0.5, len(dataframe.columns), 1), dataframe.columns)  #Notice 0.5 to get months and years in middle of sqaures
    plt.yticks(np.arange(0.5, len(dataframe.index), 1), dataframe.index) 
    plt.colorbar(orientation="horizontal")
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

def find_missing_months(dataframe):
    """
    identify missing months in dataframe (if content is not added in a month, then this month will be missing)
    """
    months = all_months()
    missing_months = []
    for m in months:
        if m not in dataframe.columns:
            missing_months.append(m)
    return missing_months

def add_missing_months(dataframe):
    """
    add missing months to dataframe
    """
    missing = find_missing_months(dataframe)
    for m in missing:
        dataframe[m] = np.zeros(len(dataframe.index)) #add column with 0 for every row in the dataframe
    return dataframe

def find_missing_years(dataframe):
    """
    identify missing years in dataframe
    """
    years = all_years()
    missing_yrs = []
    for y in years:
        if y not in dataframe.index:
            missing_yrs.append(y)
    return missing_yrs

def add_missing_yrs(dataframe):
    """
    add missing years to dataframe
    """
    missing = find_missing_years(dataframe)
    for y in missing:
        dataframe.loc[y] = np.zeros(len(dataframe.columns)) #add empty row with zeros for every column in the dataframe
    return dataframe 


def create_table(dataframe):
    """
    create a "table" dataframe to be used for heatplot
    """
    df = monthly_yearly_table(dataframe)
    df = add_missing_months(df)
    df = add_missing_yrs(df)
    df = df[all_months()] #align columns by month
    df = df.sort_values(by = "year") #sorth by year descending
    return df

def heatplot_analysis(dataframe,title,xlab,ylab):
    """
    Dataframe "table" creation and heatplot (overall function)
    """
    dataframe = valid_dates(dataframe)
    dataframe = create_month_column(dataframe)
    dataframe = create_year_column(dataframe)
    dataframe_table = create_table(dataframe)
    heatmap(dataframe_table,title=title,xlab=xlab,ylab=ylab)
    return dataframe_table

    