import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

@st.cache(suppress_st_warning=True)
def load_data(url):
    # st.write("Loading data (uncached)", url)
    return pd.read_csv(url)

# Filter by PA state only, and add `date` column in date-time for altair
def clean(df):
    PA_FIPS = 42
    df_pa = df[df['statefips'] == PA_FIPS]
    cols = ['year', 'month', 'day']
    df_pa['date'] = pd.to_datetime(df_pa[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1))
    return df_pa

# 'day' column is now 'day_endofweek'
def clean_edu(df):
    PA_FIPS = 42
    df_pa = df[df['statefips'] == PA_FIPS]
    cols = ['year', 'month', 'day_endofweek']
    df_pa['date'] = pd.to_datetime(df_pa[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1))
    return df_pa

#################################################

st.title("📚 Reopen schools or restaurants first?! Your attention-grabbing title here 🍢")

"""_Feel free to change any of the provided text, the provided charts, and their captions/labels/titles below! Feel free to remove/reorder things to fit your argument as well, or add additional assets (images, other datasets, etc)._"""

"""_In particular, please feel free to explore different columns of the data (e.g. categories of business, or categories of income), as well as swapping out the provided datasets, which can all be found as CSVs on GitHub [here](https://github.com/OpportunityInsights/EconomicTracker)._"""

"""_Suggestions for visualization components to change:_

* _Labels and legends_
* _Axis/scale ranges & colors (e.g. selectively showing or omitting data)_
* _Color palettes_
* _Data processing (e.g. linear scale, log scale)_
* _Visual representation or marks_
* _Tooltips_
"""

"""Add your names and team affiliation here."""

#################################################

"""# Introduction"""

"""Add your persuasive introduction here."""

#################################################

# Covid, state, daily
covid_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/COVID%20-%20State%20-%20Daily.csv?raw=true"

df_covid = load_data(covid_url)
df_covid_pa = clean(df_covid)

st.write("# COVID cases per state, daily")

covid_chart = alt.Chart(df_covid_pa).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(title='Date')),
    y=alt.Y('new_case_count:Q', axis=alt.Axis(title='New case count')),
).properties(
    width=600, height=400,
    title="Number of new cases in PA over time (Feb 2020-Mar 2021)"
)

"""Add your framing here."""

"""Here is a sample COVID visualization for PA only, showing the new confirmed COVID-19 cases over time (seven day moving average)."""

st.write(covid_chart)

"""Add your framing here."""

if st.checkbox("Show PA COVID data"):
    st.write(df_covid_pa)

#################################################

"""# Percent change in student participation"""

# education, state, daily
edu_url = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Zearn%20-%20State%20-%20Weekly.csv"

df_edu = load_data(edu_url)
df_edu_pa = clean_edu(df_edu)

"""Your framing here.""" 

"""This shows changes in total student participation in online math coursework in Pennsylvania."""

edu_chart = alt.Chart(df_edu_pa).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(title='Date')),
    y=alt.Y('engagement:Q', axis=alt.Axis(title='Engagement', format=".0%"))
).properties(
    width=600, height=400,
    title="PA engagement in online math over time relative to Jan."
).interactive()

st.write(edu_chart)

"""'Engagement' indicates the average level of students using platform relative to January 6-February 21 2020."""

"""Your framing here."""

if st.checkbox("Show PA edu data"):
    st.write(df_edu_pa)

#################################################

st.write("# Small business revenue per state, daily over time")

revenue_url = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Womply%20-%20State%20-%20Daily.csv"

df_revenue = load_data(revenue_url)
df_revenue_pa = clean(df_revenue)

"""Your framing here. Feel free to visualize the effects on different sectors."""

revenue_chart = alt.Chart(df_revenue_pa).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(title='Date')),
    y=alt.Y('revenue_all:Q', axis=alt.Axis(title='Revenue', format=".0%"))
).properties(
    width=600, height=400,
    title="Combined revenue changes in PA relative to Jan"
).interactive()

st.write(revenue_chart)

"""Revenue indicates the percent change in net revenue for small businesses, calculated as a seven-day moving average, seasonally adjusted, and indexed to January 4-31 2020."""

"""Your framing here."""

if st.checkbox("Show PA revenue data"):
    st.write(df_revenue_pa)

#################################################

"""# Percent change in employment since January for Feb 2, 2021"""

"""**Feel free to substitute this geo-dataset out for, e.g. datasets on education or small business revenue. You will just have to use the datasets labeled "County."**"""

# employment, county, daily
country_emp_url = "https://github.com/OpportunityInsights/EconomicTracker/blob/main/data/Employment%20-%20County%20-%20Daily.csv?raw=true"

county_metadata_url = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/GeoIDs%20-%20County.csv"

df_counties_emp_us = load_data(country_emp_url)
counties_metadata = load_data(county_metadata_url)

df_counties_emp_us = df_counties_emp_us.join(counties_metadata.set_index('countyfips'), on='countyfips')

# Filter dataset to the same day as shown on the Track the Recovery site
YEAR = 2021
MONTH = 2
DAY = 5

df_counties_emp_us = df_counties_emp_us[df_counties_emp_us['year'] == YEAR]
df_counties_emp_us = df_counties_emp_us[df_counties_emp_us['month'] == MONTH]
df_counties_emp_us = df_counties_emp_us[df_counties_emp_us['day'] == DAY]

counties = alt.topo_feature(data.us_10m.url, 'counties')

"""Your framing here."""

us_employment_map = alt.Chart(counties).mark_geoshape().encode(
    color=alt.Color('emp_combined:Q', legend=alt.Legend(title="Combined employment", format=".0%"), scale=alt.Scale(domainMid=0))
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_counties_emp_us, 'countyfips', ['emp_combined'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300,
    title="% change in total employment, relative to Jan. for 2/5/21"
)

st.write(us_employment_map)

"""'Combined employment' indicates employment level for all workers, across income quartiles and professions."""

"""Your framing here."""

if st.checkbox("Show US county employment data"):
    st.write(f'Dataset filtered for just the day {MONTH}/{DAY}/{YEAR} (M/D/Y) in the U.S.')
    df_counties_emp_us

"""## Change in employment in counties in PA."""

"""Your framing here."""

# Filter dataset to PA only
df_counties_emp_pa = df_counties_emp_us[df_counties_emp_us['statename'] == "Pennsylvania"]

pa_employment_map = alt.Chart(counties).mark_geoshape().encode(
    color=alt.Color('emp_combined:Q', legend=alt.Legend(title="Combined employment", format=".0%"), scale=alt.Scale(domainMid=0))
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_counties_emp_pa, 'countyfips', ['emp_combined', 'countyname'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300,
    title="% change in total employment, relative to Jan. for 2/5/21"
).encode(
    tooltip=[alt.Text('countyname:N', title="County name"), alt.Text('emp_combined:Q', format=".0%", title="Change in total employment")]
)

st.write(pa_employment_map)

"""'Combined employment' indicates employment level for all workers, across income quartiles and professions."""

"""Your framing here."""

if st.checkbox("Show county metadata (used for filtering counties by state)"):
    counties_metadata

if st.checkbox("Show PA county employment data"):
    df_counties_emp_pa

#################################################

"""# Conclusion"""

"""Add your persuasive conclusion here."""

#################################################

"""# Sources
 
* [_Track the Recovery_ (TTR) interactive frontend](https://tracktherecovery.org/)
* [_Track the Recovery_ datasets](https://github.com/OpportunityInsights/EconomicTracker)
* [_TTR_ data documentation](https://github.com/OpportunityInsights/EconomicTracker/blob/main/docs/oi_tracker_data_documentation.md)
* [_TTR_ data dictionary](https://github.com/OpportunityInsights/EconomicTracker/blob/main/docs/oi_tracker_data_dictionary.md)
"""
