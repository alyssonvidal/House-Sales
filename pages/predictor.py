import numpy as np
import pandas as pd
import streamlit as st
import time
from datetime import datetime, time, date
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def get_data( path ):
    data = pd.read_csv( path )
    return data

data = get_data( 'dataset/kc_house_data.csv')




# Data Preparation
data.drop_duplicates(subset=['id'], inplace=True, keep='last')
data['date'] = pd.to_datetime( data['date'] )
data['week_of_year'] = data['date'].dt.isocalendar().week
data = data.astype({"week_of_year": int})
bad_values = ((data['bedrooms'] > 10))
data = data[~bad_values]


 # Data Transformation
data["house_age"] = data["date"].dt.year - data['yr_built']
data['renovated'] = data['yr_renovated'].apply(lambda yr: 0 if yr == 0 else 1)


#Data Bining
zipsorted = pd.DataFrame(data.groupby('zipcode')['price'].median().sort_values(ascending=True))
zipsorted['rank'] = np.divmod(np.arange(len(zipsorted)), 1)[0]+1


###

price_min = int(data['price'].min())  
price_max = int(data['price'].max())
price_mean = int(data['price'].median())

bedrooms_min = int(data['bedrooms'].min())  
bedrooms_max = int(data['bedrooms'].max())
bedrooms_mean = int(data['bedrooms'].median())

bathrooms_min = int(data['bathrooms'].min())  
bathrooms_max = int(data['bathrooms'].max())
bathrooms_mean = int(data['bathrooms'].median())

sqft_living_min = int(data['sqft_living'].min())
sqft_living_max = int(data['sqft_living'].max())
sqft_living_mean = int(data['sqft_living'].median()) 

sqft_lot_min = int(data['sqft_lot'].min())
sqft_lot_max = int(data['sqft_lot'].max())
sqft_lot_mean = int(data['sqft_lot'].median())   

floors_min = int(data['floors'].min())  
floors_max = int(data['floors'].max())
floors_mean = int(data['floors'].median())

condition_min = int(data['condition'].min())  
condition_max = int(data['condition'].max())
condition_mean = int(data['condition'].median())   

sqft_living_min = int(data['sqft_living'].min())
sqft_living_max = int(data['sqft_living'].max())
sqft_living_mean = int(data['sqft_living'].median())

sqft_basement_min = int(data['sqft_basement'].min())
sqft_basement_max = int(data['sqft_basement'].max())
sqft_basement_mean = int(data['sqft_basement'].median())   

grade_min = int(data['grade'].min())
grade_max = int(data['grade'].max())
grade_median = int(data['grade'].median()) 

yr_built_min = int(data['yr_built'].min())
yr_built_max = int(data['yr_built'].max())
yr_built_median = int(data['yr_built'].median()) 

yr_lat_min = float(data['lat'].min())
yr_lat_max = float(data['lat'].max())
yr_lat_median = float(data['lat'].median())

yr_long_min = float(data['long'].min())
yr_long_max = float(data['long'].max())
yr_long_median = float(data['long'].median()) 


modify_data = data.copy()
modify_data.drop(columns=['id','date','view','zipcode','waterfront','sqft_above','yr_renovated','sqft_living15','sqft_lot15'], inplace=True)


y = modify_data["price"]
X = modify_data.drop(["price"], axis=1)

def user_input_features():
    p_bedrooms =  st.slider('bedrooms', min_value=bedrooms_min, 
                                        max_value=bedrooms_max, 
                                        value=bedrooms_mean)

    p_bathrooms =  st.slider('bathrooms', min_value=bathrooms_min, 
                                        max_value=bathrooms_max, 
                                        value=bathrooms_mean)
    p_sqft_living =  st.slider('Sqft Living Range', min_value=sqft_living_min, max_value=sqft_living_max, value=sqft_living_mean)
    p_sqft_lot =  st.slider('sqft_lot', min_value=sqft_lot_min, max_value=sqft_lot_max, value=sqft_lot_mean)
    p_floors =  st.slider('Floors', min_value=floors_min, max_value=floors_max, value=floors_mean)
    p_condition =  st.slider('Condition', min_value=condition_min, max_value=condition_max, value=condition_mean)
    p_grade =  st.slider('Grade', min_value=grade_min, max_value=grade_max, value=grade_median)
    p_sqft_basement =  st.slider('Basement', min_value=sqft_basement_min, max_value=sqft_basement_max, value=sqft_basement_mean)
    
    p_yr_built =  st.slider('Year Built', min_value=yr_built_min, max_value=yr_built_max, value=yr_built_median)
    p_yr_lat =  st.slider('Latitude', min_value=yr_lat_min, max_value=yr_lat_max, value=yr_lat_median)
    p_yr_long =  st.slider('Longitude', min_value=yr_long_min, max_value=yr_long_max, value=yr_long_median)


    p_waterfront =  st.slider('Waterfront', min_value=0, max_value=1, value=0)
    p_zipsorted =  st.slider('Rank', min_value=1, max_value=70, value=20)
    p_house_age=  st.slider('House Age', min_value=0, max_value=100, value=40)
    p_renovated =  st.slider('Renovated', min_value=0, max_value=1, value=0)


    new_data = {'p_bedrooms': p_bedrooms,
                'p_bathrooms': p_bathrooms,
                'p_sqft_living': p_sqft_living,
                'p_sqft_lot': p_sqft_lot,
                'p_floors': p_floors,
                'p_condition': p_condition,
                'p_grade': p_grade,
                'p_sqft_basement': p_sqft_basement,                
                'p_yr_built': p_yr_built,
                'p_yr_lat': p_yr_lat,
                'p_waterfront': p_waterfront,
                'p_zipsorted': p_zipsorted, 
                'p_house_age': p_house_age,   
                'p_renovated': p_renovated,                         
                }

    features = pd.DataFrame(new_data, index=[0])
    return features


# Print specified input parameters
st.header('Specified Input parameters')
new_data = user_input_features()
st.write(new_data) 

def predict():
    model = RandomForestRegressor()

    model.fit(X, y)
    #Apply Model to Make Prediction
    prediction = model.predict(new_data)
    st.subheader('House Price Predicted:')

    st.success(f'${prediction}')
    st.write('---')

trigger = st.button('Predict', on_click=predict)