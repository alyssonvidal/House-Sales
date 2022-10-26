from queue import Empty
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, time, date
import altair as alt
import folium
from folium import plugins
from streamlit_folium import folium_static, st_folium
from sklearn.ensemble import RandomForestRegressor

def get_data( path ):
    data = pd.read_csv( path )
    return data

data = get_data( 'dataset/kc_house_data.csv')



# Data Preparation 
data['date'] = pd.to_datetime( data['date'] )
data['price_sqft'] = round(data['price'] / data['sqft_living'],2)
data['price'] = round(data['price'],2)
data.drop_duplicates(subset=['id'], inplace=True, keep='last')
bad_values = ((data['bedrooms'] > 15))
data = data[~bad_values]
data['waterfront'].replace(0, "No", inplace=True)
data['waterfront'].replace(1, "Yes", inplace=True)


data = data.tail(2000)


##### Filter Params

price_min = int(data['price'].min())  
price_max = int(data['price'].max())

bedrooms_min = int(data['bedrooms'].min())  
bedrooms_max = int(data['bedrooms'].max())

floors_min = int(data['floors'].min())  
floors_max = int(data['floors'].max())

condition_min = int(data['condition'].min())  
condition_max = int(data['condition'].max())  

sqft_living_min = int(data['sqft_living'].min())
sqft_living_max = int(data['sqft_living'].max())  

data['date'] = pd.to_datetime( data['date'] ).dt.strftime( '%Y-%m-%d' )
min_date = datetime.strptime( data['date'].min(), '%Y-%m-%d' )
max_date = datetime.strptime( data['date'].max(), '%Y-%m-%d' )



st.sidebar.header('Filters:')


#f_attributes = st.sidebar.multiselect( 'Enter Columns', data.columns) 
#f_zipcode = st.sidebar.multiselect( 'Zipcodes', options=data['zipcode'].unique(), default=data['zipcode'].unique()) 

f_price = st.sidebar.slider('Price Range', min_value=0, max_value=price_max, value=(0,price_max), step=10000)
f_sqft_living =  st.sidebar.slider('Sqft Living Range', min_value=0, max_value=sqft_living_max, value=(0,sqft_living_max), step=100)
f_cal = st.sidebar.date_input('Date Range', value=(min_date, max_date)) 
#f_bedrooms= st.sidebar.slider('Bedroom Range', min_value=bedrooms_min, max_value=bedrooms_max, value=(bedrooms_min,bedrooms_max+1)) 
f_bedrooms= st.sidebar.select_slider('Bedroom Range', options=sorted(set(data['bedrooms'].unique())),value=(bedrooms_min,bedrooms_max) ) 
f_floors= st.sidebar.slider('Floors Range', min_value=floors_min, max_value=floors_max, value=(floors_min,floors_max)) 
f_condition= st.sidebar.slider('Condition Range', min_value=condition_min, max_value=condition_max, value=(condition_min,condition_max)) 
#= st.sidebar.select_slider('Bedroom Range', options=['1','2','4','5'],value=(bedrooms_min,bedrooms_max) ) 


dataselection = data.query(" price <= @f_price[1] & price >= @f_price[0] \
                    & sqft_living >= @f_sqft_living[0] & sqft_living <= @f_sqft_living[1] \
                    & bedrooms <= @f_bedrooms[1] & bedrooms >= @f_bedrooms[0] \
                    & floors <= @f_floors[1] & floors >= @f_floors[0] \
                    & condition <= @f_condition[1] & condition >= @f_condition[0]")

# Average metrics
df1 = dataselection[['id', 'zipcode']].groupby('zipcode').count().reset_index()
df2 = dataselection[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df3 = dataselection[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
df4 = dataselection[['price_sqft', 'zipcode']].groupby('zipcode').mean().reset_index()

# Merge dataframes by zipcode
meg1 = pd.merge(df1, df2, on='zipcode', how='inner')
meg2 = pd.merge(meg1, df3, on='zipcode', how='inner')
df = pd.merge(meg2, df4, on='zipcode', how='inner')

    # Rename columns
df.columns = ['zipcode', 'total houses', 'price', 'sqrt living, ', 'price/living']

st.title( 'House Rocket Company' )
st.caption( 'Welcome to House Rocket Data Analysis')


data2 = dataselection.copy()


tables_expander = st.expander(label='Tables')
with tables_expander:
    st.subheader('Tabela Descritiva')
    st.write(dataselection.shape)
    st.write(dataselection)
    st.subheader('Averages by Zip Code')    
    st.write(df.shape)
    st.dataframe(df, height=300)
    st.subheader('Tabela Estatistica')
    st.write(dataselection.shape)
    st.dataframe(dataselection.describe().T, height=300) 

charts_expander = st.expander(label='Charts')
with charts_expander:
    input_dropdown = alt.binding_select(
        options=['',1,2,3,4,5], 
        name='condition'
    )

    selection = alt.selection_single(
        fields=['condition'], 
        bind=input_dropdown
    )

    color = alt.condition(selection,
            alt.Color('condition:O'),
            alt.value('darkgray'))

    fig1= alt.Chart(data2).mark_point().encode(
            x='sqft_living:Q',
            y='price:Q',
            color=color,
            tooltip='zipcode:N'
    ).properties(
            width=680,
            height=500
    ).add_selection(
            selection
    ).interactive()


    fig2=alt.Chart(data2).mark_bar().encode(
            x='zipcode:N',
            y='mean(price)',
            tooltip='count(zipcode):N'
    #text='count()' 
    ).properties(
         width=680,
         height=500
    ).interactive()


    line = alt.Chart(data2).mark_line(point=True).encode(
            x='yearmonth(date):T',
            y='mean(price):Q'
        #tooltip='count()'
    ).properties(
            width=680,
            height=500
    ).interactive()


    band = alt.Chart(data2).mark_errorband(extent='ci').encode(
            x='yearmonth(date):T',
            y=alt.Y('mean(price):Q') #title='Miles/Gallon'
    )

    fig3 = band + line

    choose_chart = st.radio("", options=('Price by Sqft Living','Price by Zipcode', 'Prize by Month'), horizontal=True)

    if choose_chart == 'Price by Sqft Living':
        st.altair_chart(fig1)
    elif choose_chart == 'Price by Zipcode':
        st.altair_chart(fig2)
    else:
        st.altair_chart(fig3)    
    
    


### MAPAS

df2 = dataselection.copy()
geofile = f"seattle.geojson"

# MAPA 1

m1 = folium.Map(location=[df2['lat'].mean(),df2['long'].mean()],
                #tiles='cartodbpositron',
                tiles='OpenStreetMap',
                min_zoom=8.5,
                zoom_start=9.2              
                )


#marker_cluster = MarkerCluster().add_to(m1)
                        
for i, v in df2.iterrows():
        
        value = float(v['price'])
        popup = """
        Price: <b>%s</b><br>
        Sqft Living: <b>%s</b><br>
        Zipcode: <b>%s</b><br>
        Date: <b>%s</b><br>
        """ % (v['price'], v['sqft_living'], v['zipcode'], v['date'])  
        
          
        folium.CircleMarker(location = [v['lat'],v['long']],
                            radius = np.log(value) * 0.4,
                            weight = 0,
                            tooltip = popup,
                            color = 'red',
                            fill_color = 'red',
                            fill_opacity = 0.7,
                            fill = True).add_to(m1)




### MAPA 2
dgeo = df2[['price_sqft','price','zipcode']].groupby( 'zipcode' ).mean().reset_index()
dgeo['price_sqft'] = round(dgeo['price_sqft'],2)
dgeo['price'] = round(dgeo['price'],0)
df_indexed = dgeo.set_index('zipcode')

m2 = folium.Map(location=[df2['lat'].mean(),df2['long'].mean()],
                tiles='cartodbpositron',             
                min_zoom=8.5,
                max_zoom=12,  
                zoom_start=9.2 
                )

threshold_scale=[100, 150, 200, 250, 300, 350,400,650]

choropleth = folium.Choropleth( data = dgeo,
                    geo_data = geofile,
                    columns=['zipcode','price_sqft','price'],
                    key_on='feature.properties.ZIP',
                    fill_color='YlOrRd',
                    fill_opacity=1,
                    line_opacity=0.2,
                    threshold_scale=threshold_scale,
                    name="price_sqft",            
                    #smooth_factor=0,
                    highlight= True,
                    line_color = "black",
                    legend_name = "Avarage Price per Sqft Living",
                    show=True,
                    overlay=True,
                    reset=True,   
                    nan_fill_color = "gray"
                    #popup=folium.features.GeoJsonPopup(fields=["ZIP"])
                    ).add_to(m2)

choropleth.geojson.add_to(m2)

for feature in choropleth.geojson.data['features']:
        zipcode= feature['properties']['ZIP']
        feature['properties']['price_sqft'] = "$"+str(df_indexed.loc[zipcode, 'price_sqft']) if zipcode in list(df_indexed.index) else ''
        feature['properties']['price'] = "$"+str(df_indexed.loc[zipcode, 'price']) if zipcode in list(df_indexed.index) else ''   
        
        
        choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['ZIP','price_sqft','price'],label=True))    
   


m3 = folium.Map(location=[df2['lat'].mean(),df2['long'].mean()],
              tiles='cartodbpositron',
              #tiles='OpenStreetMap',
              min_zoom=8.5,
              zoom_start=9.2  
              )

cor=[]
for lat,lon in zip (df2.lat.values,df2.long.values):
    cor.append([lat,lon])    
    
m3.add_child(plugins.HeatMap(cor, radius=12))       


maps_expander = st.expander(label='Maps')

with maps_expander:

    choose_map = st.radio("", options=('Agrupado por ID','Agrupado por Região', 'Densidade'), horizontal=True)

    if choose_map == 'Agrupado por ID':
        st_map1 = folium_static(m1, width=680, height=450)
    elif choose_map == 'Agrupado por Região':
        st_map2 = folium_static(m2, width=680, height=450)
    else:
        st_map3 = folium_static(m3, width=680, height=450)
    #st.caption('A base de dados reduzida para 2000 observações para manter o desempenho da plataforma, já que o objetivo desse app é apenas expositivo e didático.')   
    
    #st.markdown( 'Localização de cada casa agrupado por preço' )
    


### RECONMENDAÇÕES ###


 

recomendations_expander = st.expander(label='Recomendations')

with recomendations_expander:

    st.subheader( 'Critérios:' )
    st.markdown( '''
        Imoveis considerados bons para compra de acordo com os critérios CEO da House Rocket. 
        * Imoveis com o preço inferior a 20% da mediana da região de acordo com a sazonalidade
        * Imoveis com estado de conservação baixo (condition < 3)
    ''')

    c1,c2,c3 = st.columns(3)
    with c1:
        header=('Mean')
        st.metric(label='Mean', value=dataselection['price'].mean().round(2), delta=None)

    with c2:
        header=('Count')
        st.metric(label='Count', value=dataselection['price'].count(), delta=None)

    with c3:
        header=('sum')
        st.metric(label='Count', value=dataselection['price'].sum().round(2), delta=None)