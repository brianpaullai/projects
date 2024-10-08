#%% Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
#%% Importing the data
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
#%% Exploring the data
print(train.info())
print(train.isna().sum())
print(train.describe())
print(train['accident'].value_counts()) #appears to be a boolean value not sure about the missing
print(train['fuel_type'].value_counts()) 
print(train['transmission'].value_counts())
print(train['clean_title'].value_counts()) #appears to be a boolean value, missing seem to be no

plt.hist(train['price'], bins = 20)
plt.xlabel('Price')
plt.ylabel('Count')
plt.title('Histogram of Price')
plt.show()

plt.scatter(train['milage'], train['price'])
plt.xlabel('Milage')
plt.ylabel('Price')
plt.title('Milage vs Price')
plt.show()

plt.scatter(train['model_year'], train['price'])
plt.xlabel('Model Year')
plt.ylabel('Price')
plt.title('Model Year vs Price')
plt.show()

print('90th percentile', np.percentile(train['price'], 90))
print('95th percentile:', np.percentile(train['price'], 95))
print('97th percentile:', np.percentile(train['price'], 97))
print('99th percentile:', np.percentile(train['price'], 99))

brand_price = train[["brand","price"]].groupby("brand").mean().sort_values("price",ascending = False)
ax = brand_price.plot(kind="bar", figsize=(15, 5))
for container in ax.containers:
    ax.bar_label(container, rotation = 90)
plt.ylabel("Avg Price")
plt.xlabel("Brands")
plt.title("Brand vs Avg Price")
#%% Dealing with null values
nan_fuel = train[train['fuel_type'].isna()]
# Looking at the engine there are obvious connections to fuel type
e_mask = ((train['engine'].str.contains('electric fuel', case = False, regex = False)) | 
          (train['engine'].str.contains('battery', case = False, regex = False)) |
          (train['engine'] == 'Electric') |
          (train['engine'].str.contains('electric motor', case = False, regex = False)) |
          (train['engine'].str.contains('dual motor', case = False, regex = False)) |
          (train['engine'].str.contains('kW')))
train.loc[e_mask, 'fuel_type'] = train.loc[e_mask, 'fuel_type'].fillna('Electric')
h_mask = (train['engine'].str.contains('hybrid', case = False, regex = False))
train.loc[h_mask, 'fuel_type'] = train.loc[h_mask, 'fuel_type'].fillna('Hybrid')
g_mask = (train['engine'].str.contains('gasoline', case = False, regex = False))
train.loc[g_mask, 'fuel_type'] = train.loc[g_mask, 'fuel_type'].fillna('Gasoline')
d_mask = (train['engine'].str.contains('diesel', case = False, regex = False))
train.loc[d_mask, 'fuel_type'] = train.loc[d_mask, 'fuel_type'].fillna('Diesel')
f_mask = (train['engine'].str.contains('flex fuel', case = False, regex = False))
train.loc[f_mask, 'fuel_type'] = train.loc[f_mask, 'fuel_type'].fillna('E85 Flex Fuel')

# Changing the clean_title column to just be a boolean value
train['clean_title'] = train['clean_title'].where(train['clean_title'] == 'Yes', 0)
train['clean_title'] = train['clean_title'].where(train['clean_title'] == 0, 1)

# Filling in null values for accident
train['accident'] = train['accident'].fillna('Missing')
#%% Feature Creation
train['hp'] = train['engine'].str.extract(r'([0-9]*)\.([0-9]HP)')[0].astype(float)
train['hp'] = train['hp'].fillna(0)

train['disp'] = train['engine'].str.extract(r'([0-9]*)\.([0-9]L)')[0].astype(float)
train['disp'] = train['disp'].fillna(0)

t_a_mask = ((train['transmission'].str.contains('AT')) |
            (train['transmission'].str.contains('A\/T')) |
            (train['transmission'].str.contains('Automatic')))
t_m_mask = ((train['transmission'].str.contains('MT')) |
            (train['transmission'].str.contains('M\/T')) |
            (train['transmission'].str.contains('Manual')))
train.loc[t_a_mask, 'automatic'] = 1
train.loc[~t_a_mask, 'automatic'] = 0
train.loc[t_m_mask,'manual'] = 1
train.loc[~t_m_mask,'manual'] = 0

train['age'] = 2024-train['model_year']

euro_brand = ['MINI', 'Mercedes-Benz', 'Audi', 'BMW', 'Land', 'Volvo', 'Volkswagen', 'Alfa', 
              'Porsche', 'McLaren', 'Jaguar', 'Rolls-Royce', 'Maserati', 'Bentley', 'Ferrari', 
              'Aston', 'Lamborghini','Lotus', 'smart', 'Karma', 'FIAT', 'Saab', 'Bugatti', 
              'Polestar', 'Maybach']
asian_brand = ['Genesis', 'Toyota', 'Hyundai', 'INFINITI', 'Honda', 'Lexus', 'Nissan', 'Acura',
               'Kia', 'Mitsubishi', 'Mazda', 'Subaru', 'Scion', 'Suzuki']
na_brand = ['Lincoln', 'Chevrolet', 'Ford', 'Tesla', 'Cadillac', 'GMC', 'Buick', 'Rivian', 'RAM',
            'Hummer', 'Jeep', 'Dodge', 'Pontiac', 'Saturn', 'Chrysler', 'Lucid', 'Plymouth', 'Mercury']
def brand_origin(x):
    if x in euro_brand:
        return 'euro'
    elif x in asian_brand:
        return 'asia'
    elif x in na_brand:
        return 'na'
train['brand_origin'] = train['brand'].apply(brand_origin)

brand_price_index = train[['brand','price']].groupby('brand').mean().sort_values('price',ascending = False).index
luxury_car_brand = brand_price_index[:7]
premium_car_brand = brand_price_index[7:24]
expensive_car_brand = brand_price_index[24:47]
cheap_car_brand = brand_price_index[47:]
def brand_category(x):
    if x in luxury_car_brand:
        return "luxury"
    elif x in premium_car_brand:
        return "premium"
    elif x in expensive_car_brand:
        return "expensive"
    elif x in cheap_car_brand:
        return "cheap"
    return "other"
train['brand_category'] = train['brand'].apply(brand_category)

#%% Applying previous steps to the test data
e_mask = ((test['engine'].str.contains('electric fuel', case = False, regex = False)) | 
          (test['engine'].str.contains('battery', case = False, regex = False)) |
          (test['engine'] == 'Electric') |
          (test['engine'].str.contains('electric motor', case = False, regex = False)) |
          (test['engine'].str.contains('dual motor', case = False, regex = False)) |
          (test['engine'].str.contains('kW')))
test.loc[e_mask, 'fuel_type'] = test.loc[e_mask, 'fuel_type'].fillna('Electric')
h_mask = (test['engine'].str.contains('hybrid', case = False, regex = False))
test.loc[h_mask, 'fuel_type'] = test.loc[h_mask, 'fuel_type'].fillna('Hybrid')
g_mask = (test['engine'].str.contains('gasoline', case = False, regex = False))
test.loc[g_mask, 'fuel_type'] = test.loc[g_mask, 'fuel_type'].fillna('Gasoline')
d_mask = (test['engine'].str.contains('diesel', case = False, regex = False))
test.loc[d_mask, 'fuel_type'] = test.loc[d_mask, 'fuel_type'].fillna('Diesel')
f_mask = (test['engine'].str.contains('flex fuel', case = False, regex = False))
test.loc[f_mask, 'fuel_type'] = test.loc[f_mask, 'fuel_type'].fillna('E85 Flex Fuel')

test['clean_title'] = test['clean_title'].where(test['clean_title'] == 'Yes', 0)
test['clean_title'] = test['clean_title'].where(test['clean_title'] == 0, 1)

test['accident'] = test['accident'].fillna('Missing')

test['hp'] = test['engine'].str.extract(r'([0-9]*)\.([0-9]HP)')[0].astype(float)
test['hp'] = test['hp'].fillna(0)

test['disp'] = test['engine'].str.extract(r'([0-9]*)\.([0-9]L)')[0].astype(float)
test['disp'] = test['disp'].fillna(0)

t_a_mask = ((test['transmission'].str.contains('AT')) |
            (test['transmission'].str.contains('A\/T')) |
            (test['transmission'].str.contains('Automatic')))
t_m_mask = ((test['transmission'].str.contains('MT')) |
            (test['transmission'].str.contains('M\/T')) |
            (test['transmission'].str.contains('Manual')))
test.loc[t_a_mask, 'automatic'] = 1
test.loc[~t_a_mask, 'automatic'] = 0
test.loc[t_m_mask,'manual'] = 1
test.loc[~t_m_mask,'manual'] = 0

test['age'] = 2024-test['model_year']

test['brand_origin'] = test['brand'].apply(brand_origin)

test['brand_category'] = test['brand'].apply(brand_category)

#%% OLS
train2 = pd.get_dummies(data = train, columns=['brand', 'fuel_type', 'accident', 'brand_origin', 'brand_category'], dtype = int)
train2 = train2[train2['price']< 500000]
train_x = train2.drop(columns = ['id', 'price', 'model', 'int_col', 'ext_col', 'engine', 'model_year', 'transmission', 'brand_Polestar', 'brand_smart'])
price = train2['price']
X_train, X_test, y_train, y_test = train_test_split(train_x, price, test_size=0.3, random_state = 10)
reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)
mean_squared_error(y_test, y_pred)
# 2 OLS with onehot variables and brand origin 865240576.8960277 
# 3 dropping id 865232332.7858169
# 4 changed cutoff from 300,000 to 1,000,000 and adding the brand categories 1670387061.9324086
# 6 tried removing brands to see if the variables derived from brand would replace it 1692846139.194646
# 7 changed the cutoff to 500,000 1324356511.4024823
#%% Predicting with OLS
test2 = pd.get_dummies(data = test, columns=['brand', 'fuel_type', 'accident', 'brand_origin', 'brand_category'], dtype = int)
test2 = test2.drop(columns = ['id', 'model', 'int_col', 'ext_col', 'engine', 'model_year', 'transmission'])
test_pred = reg.predict(test2)

#%% Random Forest
train3 = pd.get_dummies(data = train, columns=['brand', 'fuel_type', 'accident', 'brand_origin', 'brand_category'], dtype = int)
train3 = train3[train3['price']< 1000000]
train_x = train3.drop(columns = ['id', 'price', 'model', 'int_col', 'ext_col', 'engine', 'model_year', 'transmission', 'brand_Polestar', 'brand_smart'])
price = train3['price']
X_train, X_test, y_train, y_test = train_test_split(train_x, price, test_size=0.3, random_state = 10)
regr = RandomForestRegressor(random_state=10)
regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
mean_squared_error(y_test, y_pred)
# 5 1833249703.702538

#%% Predicting with Random Forests
test3 = pd.get_dummies(data = test, columns=['brand', 'fuel_type', 'accident', 'brand_origin', 'brand_category'], dtype = int)
test3 = test3.drop(columns = ['id','model', 'int_col', 'ext_col', 'engine', 'model_year', 'transmission'])
test_pred = regr.predict(test2)

#%% Clening up the brand
train4 = train
train4['model'] = train4['model'].str.split().str[0]
#train4['engine_words'] = train['engine'].str.split().apply(len)

#%% OLS with model as dummy variable, dropping brand
train4 = pd.get_dummies(data = train4, columns=['model', 'fuel_type', 'accident', 'brand_origin', 'brand_category'], dtype = int)
train4 = train4[train4['price']< 500000]
train_x = train4.drop(columns = ['id', 'price', 'brand', 'int_col', 'ext_col', 'engine', 'model_year', 'transmission'])
price = train4['price']
X_train, X_test, y_train, y_test = train_test_split(train_x, price, test_size=0.3, random_state = 10)
reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)
mean_squared_error(y_test, y_pred)
# 8 1276803548.3981671
# 9 created engine word count 1276697088.261095
# 10 raised the price limit from 500,000 to 1,000,000 didn't use engine word count 35344237335773.31
#%% Predicting with OLS, dropping brand
test4 = test
test4['model'] = test4['model'].str.split().str[0]
#test4['engine_words'] = test4['engine'].str.split().apply(len)
test4 = pd.get_dummies(data = test4, columns=['model', 'fuel_type', 'accident', 'brand_origin', 'brand_category'], dtype = int)
test4 = test4.drop(columns = ['id', 'brand', 'int_col', 'ext_col', 'engine', 'model_year', 'transmission'])
test_pred = reg.predict(test4)

#%% Creating a submission
sample = pd.read_csv('sample_submission.csv')
sample['price'] = test_pred
sample.to_csv('submission10.csv', index = False)

