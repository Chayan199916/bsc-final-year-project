#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# from google.colab import drive
# drive.mount('/content/drive')


# In[1]:


import pandas as pd
import numpy as np
from sklearn.externals import joblib


# In[2]:


df = pd.read_csv('merged_new.csv')
df.head(1)


# In[3]:


col_list = ["PM10", "D-1 PM10", "Air Temperature", "Horizontal Visibility", "Dew Point Temperature", "Wind Speed", "Relative Humidity"]
target_y = ['PM10']


# In[4]:


X = df[col_list][:-1]
y = df[target_y][1:]


# In[5]:


calc_test_size = round(X.shape[0]*(1 - 0.2))
x_train = X.iloc[:calc_test_size, :]
x_test = X.iloc[calc_test_size:, :]
y_train = y.iloc[:calc_test_size, :]
y_test = y.iloc[calc_test_size:, :]
xx_train = np.array(x_train)
yy_train = np.array(y_train)
xx_test = np.array(x_test)
yy_test = np.array(y_test)


# In[6]:


pm10_svr_obj = joblib.load('saved_models/pm10/pm10_svr_predictor.joblib')
pm10_svr_xscaler = joblib.load('saved_scalers/pm10/pm10_svr_xscaler.save')
pm10_svr_yscaler = joblib.load('saved_scalers/pm10/pm10_svr_yscaler.save')


# In[ ]:


# # from sklearn.preprocessing import PolynomialFeatures
# # pf = PolynomialFeatures()
# # x_poly = pf.fit_transform(xx_test)
# predicted_result = so2_forest_obj.predict(xx_train) 

X = pm10_svr_xscaler.transform(xx_train)
prediction = pm10_svr_obj.predict(X)
predicted_result = pm10_svr_yscaler.inverse_transform(prediction)


# In[ ]:


import matplotlib.pyplot as plt
x = np.arange(len(yy_train))


# In[ ]:


plt.figure(figsize = (10, 10))
plt.style.use('dark_background')
plt.scatter(x, yy_train, label = "actual", c = "b", s = 100)
plt.scatter(x, predicted_result, label = "prediction", c = "skyblue", s = 100)
plt.xlabel("Days", fontsize = 13)
plt.ylabel("PM10", fontsize = 13)
plt.grid()
plt.xticks(size = 10)
plt.yticks(size = 10)
plt.tight_layout()
plt.title("Support Vector Regression : PM10 scatter plot", fontsize = 15)
plt.legend(fontsize = 12)
plt.show()


# In[ ]:




