import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

st.set_page_config(page_title='Hail Storm Data Analysis',layout="wide")

### Data Import ###

# final_data = pd.read_csv("./data/final_table.csv")
df = pd.read_csv("./data/US_mm.csv")
df = df.drop(df.columns[0], axis=1)
df_hail_days = pd.read_csv("./data/df_hail_days.csv")
df_hail_days = df_hail_days.drop(df_hail_days.columns[0], axis=1)
reset_hail_days_count = pd.read_csv("./data/reset_hail_days_count.csv")
reset_hail_days_count = reset_hail_days_count.drop(reset_hail_days_count.columns[0], axis=1)
### INTRODUCTION ###

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Hail Storm Data Analysis')

row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("This project provides benchmarking of the risk of hail in the field with respect to the IEC 61215 qualification test for Hail testing on PV Modules.")
    st.markdown("PV module qualification standard IEC 61215 involves shooting hail balls with a diameter of 25 mm at a speed of 23 m/s at various positions on a PV module. The module passes this test if there are no visual defects as a result of hail impact, insulation resistance is within acceptable limits and the power loss is within 5% of the original. Reduction in the residual life of the Solar PV Modules due to bombarding with hails can cause damage to the cells (not always visible to the eye)")
    st.markdown("There is a lack of high-quality field data regarding the frequency of hail storms, amount of area affected and exact size of the hail that’s reaching the surface of the Earth.")
    see_data = st.expander('You can click here to see the raw US Hail data first 👉')
    with see_data:
        st.dataframe(data=df.reset_index(drop=True))

## STATISTICS ###

row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.markdown(" ")
    st.subheader("KEY STATISTICS:")
    st.markdown(" ")

row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))

with row2_1:
    num_occ = df.shape[0]
    st.metric(label="Hailstorm Occurrences 📊", value=num_occ)
with row2_2:
    days_hail = df.drop_duplicates(subset = ['Year', 'Month','Day'], keep = 'last').reset_index(drop = True)
    days_hail = days_hail.loc[days_hail.groupby(['Year', 'Month','Day'])['Size'].idxmax()]
    hd = days_hail['Day'].count()
    st.metric(label="Hail Days 📅", value=hd)
with row2_3:
    max_size = df['Size'].max()
    st.metric(label="Maximum Size Recorded (mm) 📈" , value=max_size)
with row2_4:
    min_size = df['Size'].min()
    st.metric(label="Minimum Size Recorded (mm) 📉", value=min_size)


row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader('ANALYSIS PER YEAR')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.0, .2))
with row5_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown('Statistics for hail size each year (1955-2022)')
    st.markdown('Weibull distribution appropriately described the long-tailed distribution of hail sizes observed in the entire US data for each year')  
    select = st.selectbox('Select a Year',df['Year'].unique())
    year_data = df[df['Year'] == select]

rc = {'figure.figsize':(10,6),
        'axes.facecolor':'#0E1117',
        'axes.edgecolor': '#0E1117',
        'axes.labelcolor': 'white',
        'figure.facecolor': '#0E1117',
        'patch.edgecolor': '#0E1117',
        'text.color': '#0E1117',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'font.size' : 13,
        'axes.labelsize': 17,
        'xtick.labelsize': 13,
        'ytick.labelsize': 13}
plt.rcParams.update(rc)
fig, ax = plt.subplots()
with row5_2:
    ax = sns.histplot(x="Size", data=year_data, color = "#0b70f3")
    for p in ax.patches:
        ax.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                textcoords = 'offset points',
                color='white')
    st.pyplot(fig)

def group_measure(measure):
    df_data = df[['Year','Size']]
    df_return = pd.DataFrame()
    # if(measure == "Total"):
    #     df_return = df_data.groupby(['Year']).sum()            
    
    if(measure == "Average"):
        df_return = df_data.groupby(['Year']).mean()
        
    if(measure == "Median"):
        df_return = df_data.groupby(['Year']).median()

    if(measure == "Minimum"):
        df_return = df_data.groupby(['Year']).min()
    
    if(measure == "Maximum"):
        df_return = df_data.groupby(['Year']).max()

    return df_return


### FREQUENCY ###

row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader('FREQUENCY OF HAIL OCCURRENCES')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.0, .2))
with row5_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown('Statistics for frequency of hail occurrences according to particular mesures. Analysis can be done based on average, median, maximum and minimum hail sizes.')  
    st.markdown('There seems to be an increase in occurrences after 2010.')
    measure = ["Average","Median","Maximum","Minimum"]
    measure_select = st.selectbox('Which attribute do you want to analyze?',measure)
with row5_2:
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    df_plot = pd.DataFrame()
    df_plot = group_measure(measure_select)
    ax = sns.lineplot(x="Year", y="Size", data=df_plot.reset_index(), color = "#0b70f3")
    st.pyplot(fig)


### HAIL DAYS ###


row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader('HAIL DAYS')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.0, .2))
with row5_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown('Statistics for the number of hail days more/less than the standard size.')  
    st.markdown('Hail days as a term refers to the unique number of days that hail occurrences were reported.')
    attribute_select = st.selectbox('Which attribute do you want to analyze?',df_hail_days['Intervals'].unique())
    attribute_data = df_hail_days[df_hail_days['Intervals'] == attribute_select]

with row5_2:
    rc = {'figure.figsize':(10,6),
    'axes.facecolor':'#0E1117',
    'axes.edgecolor': '#0E1117',
    'axes.labelcolor': 'white',
    'figure.facecolor': '#0E1117',
    'patch.edgecolor': 'white',
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'font.size' : 13,
    'axes.labelsize': 17,
    'xtick.labelsize': 13,
    'ytick.labelsize': 13}

    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    df_plot = pd.DataFrame()
    ax = sns.lineplot(x="Year", y="Count", data=attribute_data.reset_index(), color = "#0b70f3")

    for p in ax.patches:
        ax.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                fontsize = 8,
                textcoords = 'offset points',
                color = 'white')
    st.pyplot(fig)

### UPTON COUNTY ###


row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.subheader('UPTON COUNTY ANALYSIS')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.0, .2))
with row5_1:
    st.markdown(" ")
    st.markdown(" ")
    st.markdown('Statistics for frequency and size of hailstorms in Upton County, Texas, US.')  
    st.markdown('Reason for selection of this county is that there are major solar installations in the US are around this region, it has a small size (~3200 Km2) which would mean that any extreme weather event in the county is likely to be experienced by every PV installation') 
    upton_county_attribute = st.selectbox('Which attribute do you want to analyze?',reset_hail_days_count['Intervals'].unique(), key = "2")
    upton_data = reset_hail_days_count[reset_hail_days_count['Intervals'] == upton_county_attribute]
with row5_2:
    rc = {'figure.figsize':(10,6),
    'axes.facecolor':'#0E1117',
    'axes.edgecolor': '#0E1117',
    'axes.labelcolor': 'white',
    'figure.facecolor': '#0E1117',
    'patch.edgecolor': 'white',
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'font.size' : 10,
    'axes.labelsize': 15,
    'xtick.labelsize': 10,
    'ytick.labelsize': 13}

    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ax = sns.barplot(x="Year", y="Count", data=upton_data.reset_index(), color = "#0b70f3")
    plt.xticks(rotation=66,horizontalalignment="right")
    for p in ax.patches:
        ax.annotate(format(str(int(p.get_height()))), 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center', 
                xytext = (0, 10),
                fontsize = 13,
                textcoords = 'offset points',
                color = 'white')
    st.pyplot(fig)

