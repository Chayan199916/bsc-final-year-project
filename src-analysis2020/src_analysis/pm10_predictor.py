import pandas as pd
import numpy as np
import json
from sklearn.externals import joblib
from sklearn.preprocessing import PolynomialFeatures
from tensorflow import keras
import sys, os

class pm10_predictor:
    
    def __init__(self):
        with open('parameters.txt') as file:
            self.param_json = json.loads(file.read())
            
    def __get_dataframe(self, data, model_type):

        df = pd.DataFrame(data)
        col_list = self.param_json['pm10'][model_type]
        X = np.array(df[col_list])
        return X
    
    def get_multi_lin_prediction(self, data):

        X = self.__get_dataframe(data, 'multi linear reg')        
        model = joblib.load('saved_models/pm10/pm10_multi_lin_predictor.joblib')
        prediction = model.predict(X)
        
        return prediction.ravel()[0]
    
    def get_poly_prediction(self, data):
        
        X = self.__get_dataframe(data, 'polynomial reg')
        pf = PolynomialFeatures()
        X_poly = pf.fit_transform(X)
        model = joblib.load('saved_models/pm10/pm10_poly_predictor.joblib')
        prediction = model.predict(X_poly)
        
        return prediction.ravel()[0]
    
    def get_random_forest_prediction(self, data):
        X = self.__get_dataframe(data, 'random forest')
        model = joblib.load('saved_models/pm10/pm10_forest_predictor.joblib')
        prediction = model.predict(X)
        
        return prediction.ravel()[0]        

    def get_svr_prediction(self, data):
        X = self.__get_dataframe(data, 'svr')
        x_scaler = joblib.load('saved_scalers/pm10/pm10_svr_xscaler.save')
        y_scaler = joblib.load('saved_scalers/pm10/pm10_svr_yscaler.save')
        X = x_scaler.transform(X)
        model = joblib.load('saved_models/pm10/pm10_svr_predictor.joblib')
        prediction = model.predict(X)
        
        return y_scaler.inverse_transform(prediction).ravel()[0]  
    
    def get_mlp_prediction(self, data):
        X = self.__get_dataframe(data, 'mlp')
        scaler = joblib.load('saved_scalers/pm10/pm10_mlp_scaler.save')
        X = scaler.transform(X)
        model = joblib.load('saved_models/pm10/pm10_MLP.joblib')
        prediction = model.predict(X)
        
        return prediction.ravel()[0]
    
    def get_wide_deep_prediction(self, data):
        X_deep = self.__get_dataframe(data, 'wide deep deep')
        X_wide = self.__get_dataframe(data, 'wide deep wide')
        deep_scaler = joblib.load('saved_scalers/pm10/pm10_wide_deep_deep_scaler.save')
        wide_scaler = joblib.load('saved_scalers/pm10/pm10_wide_deep_wide_scaler.save')
        
        X_deep = deep_scaler.transform(X_deep)
        X_wide = wide_scaler.transform(X_wide)
        
        model = keras.models.load_model('saved_models/pm10/pm10_wide_deep.h5')
        prediction = model.predict((X_deep, X_wide))
        
        return prediction.ravel()[0]
    
    def get_lstm_prediction(self, data):
        X = self.__get_dataframe(data, 'lstm')
        scaler = joblib.load('saved_scalers/pm10/pm10_lstm_scaler.save')
        X = scaler.transform(X)
        model = keras.models.load_model('saved_models/pm10/pm10_LSTM.h5')
        X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
        
        prediction = model.predict(X)
        
        return prediction.ravel()[0]
    
    def get_gru_prediction(self, data):
        X = self.__get_dataframe(data, 'gru')
        scaler = joblib.load('saved_scalers/pm10/pm10_gru_scaler.save')
        X = scaler.transform(X)
        model = keras.models.load_model('saved_models/pm10/pm10_GRU.h5')
        X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
        
        prediction = model.predict(X)
        
        return prediction.ravel()[0]

# import sys, os
# sys.path.append(os.path.abspath('../'))
# from data_fetcher import data_fetcher

# p = pm10_predictor()
# f = data_fetcher.fetcher()
# fetched_data = f.get('01.01.2020')
# print(p.get_multi_lin_prediction(fetched_data))
# print(p.get_poly_prediction(fetched_data))
# print(p.get_random_forest_prediction(fetched_data))
# print(p.get_svr_prediction(fetched_data))
# print(p.get_mlp_prediction(fetched_data))
# print(p.get_wide_deep_prediction(fetched_data))
# print(p.get_lstm_prediction(fetched_data))
# print(p.get_gru_prediction(fetched_data))
