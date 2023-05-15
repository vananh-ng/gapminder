import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

gni_per_capita = pd.read_csv('gnipercapita_ppp_current_international.csv')
life_expectancy = pd.read_csv('life_expectancy_years.csv')
population_total = pd.read_csv('population_total.csv')

gni_per_capita.fillna(method='ffill', inplace=True)
life_expectancy.fillna(method='ffill', inplace=True)
population_total.fillna(method='ffill', inplace=True)

gni_per_capita_tidy = gni_per_capita.melt(id_vars=['country'], var_name='year', value_name='gni_per_capita')
life_expectancy_tidy = life_expectancy.melt(id_vars=['country'], var_name='year', value_name='life_expectancy')
population_total_tidy = population_total.melt(id_vars=['country'], var_name='year', value_name='population_total')

merged_data = gni_per_capita_tidy.merge(life_expectancy_tidy, on=['country', 'year']).merge(population_total_tidy, on=['country', 'year'])
merged_data = merged_data[['country', 'year', 'gni_per_capita', 'life_expectancy', 'population_total']]

'''
# Plotting GNI per capita
plt.figure(figsize=(10, 6))
for country in merged_data['country'].unique():
    data = merged_data[merged_data['country'] == country]
    plt.plot(data['year'], data['gni_per_capita'], label=country)
plt.xlabel('Year')
plt.ylabel('GNI per capita')
plt.title('GNI per Capita by Country')
plt.legend()
st.pyplot(plt)

# Plotting life expectancy
plt.figure(figsize=(10, 6))
for country in merged_data['country'].unique():
    data = merged_data[merged_data['country'] == country]
    plt.plot(data['year'], data['life_expectancy'], label=country)
plt.xlabel('Year')
plt.ylabel('Life Expectancy')
plt.title('Life Expectancy by Country')
plt.legend()
st.pyplot(plt)

# Plotting population
plt.figure(figsize=(10, 6))
for country in merged_data['country'].unique():
    data = merged_data[merged_data['country'] == country]
    plt.plot(data['year'], data['population_total'], label=country)
plt.xlabel('Year')
plt.ylabel('Population')
plt.title('Population by Country')
plt.legend()
st.pyplot(plt)
'''

merged_data['year'] = merged_data['year'].astype(int)

st.title('GNI, Life Expectancy, and Population Dashboard')

year = st.slider('Year', min_value=int(merged_data['year'].min()), max_value=int(merged_data['year'].max()), value=int(merged_data['year'].max()))

countries = st.multiselect('Countries', options=list(merged_data['country'].unique()), default=list(merged_data['country'].unique()))

filtered_data = merged_data[(merged_data['year'] == year) & (merged_data['country'].isin(countries))]

filtered_data['gni_per_capita'] = np.log(filtered_data['gni_per_capita'])

chart = alt.Chart(filtered_data).mark_circle().encode(
    alt.X('gni_per_capita:Q', scale=alt.Scale(zero=False), title='Log(GNI per Capita, PPP adjusted)'),
    alt.Y('life_expectancy:Q', scale=alt.Scale(zero=False), title='Life Expectancy'),
    alt.Size('population_total:Q', title='Population'),
    alt.Color('country:N', title='Country'),
    tooltip=['country', 'gni_per_capita', 'life_expectancy', 'population_total']
).properties(
    width=600,
    height=400
)

st.altair_chart(chart)