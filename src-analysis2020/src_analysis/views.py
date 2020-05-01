from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
from sklearn.externals import joblib
import pandas as pd
import json
from sklearn.preprocessing import PolynomialFeatures
from tensorflow import keras
from datetime import datetime
import sys, os
# sys.path.append(os.path.abspath('../'))
from src_analysis.pm10_predictor import pm10_predictor
from src_analysis.no2_predictor import no2_predictor
from src_analysis.so2_predictor import so2_predictor
from data_fetcher import data_fetcher
from src_analysis.aqi_calc.AQI import AQI

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def docs(request):
    return render(request, 'docs.html')

def plots(request):
    return render(request, 'plots.html')

def prediction(request):
    return render(request, 'prediction.html')

def about(request):
    return render(request, 'about.html')


def result1(request):
    date = request.GET.get('date', 'default')
    fetcher = data_fetcher.fetcher()
    fetched_data = fetcher.get(date)
    #print(fetched_data)
    pm10_object = pm10_predictor()
    no2_object = no2_predictor()
    so2_object = so2_predictor()
    mlr_is_checked = request.GET.get('check1', 'off')
    svr_is_checked = request.GET.get('check2', 'off')
    rf_is_checked = request.GET.get('check3', 'off')
    pr_is_checked = request.GET.get('check4', 'off')
    mlp_is_checked = request.GET.get('check5', 'off')
    lstm_is_checked = request.GET.get('check6', 'off')
    gru_is_checked = request.GET.get('check7', 'off')
    wide_is_checked = request.GET.get('check8', 'off')
    sum_pm10 = 0.0
    sum_no2 = 0.0
    sum_so2 = 0.0
    avg_pm10 = 0.0
    avg_no2 = 0.0
    avg_so2 = 0.0
    flag = 0

    if mlr_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_multi_lin_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_multi_lin_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_multi_lin_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Multivariable regression model', 'level': level, 'advisory': advisory}

    if svr_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_svr_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_svr_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_svr_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Support vector regression model', 'level': level, 'advisory': advisory}

    if rf_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_random_forest_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_random_forest_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_random_forest_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Random forest model', 'level': level, 'advisory': advisory}

    if pr_is_checked == 'on':
        flag = flag + 1        
        pm10_result = round(pm10_object.get_poly_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_poly_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_poly_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Polynomial regression model', 'level': level, 'advisory': advisory}

    if mlp_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_mlp_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_mlp_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_mlp_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Multilayer perceptron model', 'level': level, 'advisory': advisory}

    if lstm_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_lstm_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_lstm_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_lstm_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Long short term memory(LSTM) model', 'level': level, 'advisory': advisory}

    if gru_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_gru_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_gru_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_gru_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Gated recurrent unit(GRU) model', 'level': level, 'advisory': advisory}

    if wide_is_checked == 'on':
        flag = flag + 1
        pm10_result = round(pm10_object.get_wide_deep_prediction(fetched_data), 3)
        no2_result = round(no2_object.get_wide_deep_prediction(fetched_data), 3)
        so2_result = round(so2_object.get_wide_deep_prediction(fetched_data), 3)
        aqi_object = AQI(pm10_result, no2_result, so2_result)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        sum_pm10 = sum_pm10 + pm10_result
        sum_no2 = sum_no2 + no2_result
        sum_so2 = sum_so2 + so2_result
        params = {'date': date, 'pm10': pm10_result, 'no2': no2_result, 'so2': so2_result, 'aqi': aqi_val, 'msg': msg, 'model': 'Wide deep neural network model', 'level': level, 'advisory': advisory}
    
    if flag == 1:
        return render(request, 'result1.html', params)
    elif flag == 0:
        return HttpResponse('<h1>You have not selected any model...</h1>')
    else:
        avg_pm10 = round((sum_pm10 / flag), 3)
        avg_no2 = round((sum_no2 / flag), 3)
        avg_so2 = round((sum_so2 / flag), 3)
        aqi_object = AQI(avg_pm10, avg_no2, avg_so2)
        aqi_val, msg, level, advisory = aqi_object.get_aqi()
        params = {'date': date, 'pm10': avg_pm10, 'no2': avg_no2, 'so2': avg_so2, 'aqi': aqi_val, 'msg': msg, 'model': 'Average(Contribution of more than one models)', 'level': level, 'advisory': advisory}
        return render(request, 'result1.html', params)

def result2(request):
    print(os.getcwd())
    date = request.GET.get('date', 'default')
    pm10_val = round(float(request.GET.get('pm10', 'default')))
    no2_val = round(float(request.GET.get('no2', 'default')))
    so2_val = round(float(request.GET.get('so2', 'default')))
    aqi_object = AQI(pm10_val, no2_val, so2_val)
    aqi_val, msg, level, advisory = aqi_object.get_aqi()
    params = {'date': date, 'pm10': pm10_val, 'no2': no2_val, 'so2': so2_val, 'aqi': aqi_val, 'msg': msg, 'level': level, 'advisory': advisory}
    return render(request, 'result2.html', params)

def result3(request):
    date = request.GET.get('date', 'default')
    cur_obj = datetime.strptime(date, '%d.%m.%Y')
    first_obj = datetime(cur_obj.year, 1, 1, 0, 0)
    day_no = cur_obj - first_obj
    lis_air_temp = []
    lis_year = []
    lis_day_no = []
    lis_pressure_lev = []
    lis_relat_humidity = []
    lis_hor_visible = []
    lis_dew_temp = []
    lis_wind_speed = []
    lis_prev_pm10 = []
    lis_prev_no2 = []
    lis_prev_so2 = []
    lis_last_prev_pm10 = []
    lis_last_prev_no2 = []
    lis_last_prev_so2 = []
    lis_year.append(cur_obj.year)
    lis_day_no.append(day_no.days + 1)
    lis_air_temp.append(float((request.GET.get('atemp', 'default'))))
    lis_pressure_lev.append(float((request.GET.get('pslev', 'default'))))
    lis_relat_humidity.append(float((request.GET.get('rhum', 'default'))))
    lis_hor_visible.append(float((request.GET.get('hvis', 'default'))))
    lis_dew_temp.append(float((request.GET.get('dtemp', 'default'))))
    lis_wind_speed.append(float((request.GET.get('wspeed', 'default'))))
    lis_prev_pm10.append(float((request.GET.get('pmlast', 'default'))))
    lis_prev_no2.append(float((request.GET.get('nolast', 'default'))))
    lis_prev_so2.append(float((request.GET.get('solast', 'default'))))
    lis_last_prev_pm10.append(float((request.GET.get('pmprevlast', 'default'))))
    lis_last_prev_no2.append(float((request.GET.get('noprevlast', 'default'))))
    lis_last_prev_so2.append(float((request.GET.get('soprevlast', 'default'))))
    fetched_data = {'Air Temperature': lis_air_temp,'Pressure Station Level': lis_pressure_lev,'Wind Speed': lis_wind_speed,'Relative Humidity': lis_relat_humidity,'Horizontal Visibility': lis_hor_visible,'Dew Point Temperature': lis_dew_temp,'Day No.': lis_day_no,'Year': lis_year,'PM10': lis_prev_pm10,'NO2': lis_prev_no2,'SO2': lis_prev_so2,'D-1 PM10': lis_last_prev_pm10,'D-1 NO2': lis_last_prev_no2,'D-1 SO2': lis_last_prev_so2}
    #print(fetched_data)
    pm10_object = pm10_predictor()
    no2_object = no2_predictor()
    so2_object = so2_predictor()
    sum_pm10 = 0.0
    sum_no2 = 0.0
    sum_so2 = 0.0
    avg_pm10 = 0.0
    avg_no2 = 0.0
    avg_so2 = 0.0
    sum_pm10 = sum_pm10 + pm10_object.get_poly_prediction(fetched_data)+pm10_object.get_mlp_prediction(fetched_data)
    sum_no2 = sum_no2 + no2_object.get_mlp_prediction(fetched_data)+no2_object.get_lstm_prediction(fetched_data)
    sum_so2 = sum_so2 + so2_object.get_svr_prediction(fetched_data)+so2_object.get_mlp_prediction(fetched_data)
        #print(sum_pm10, sum_no2, sum_so2)
    avg_pm10 = round(sum_pm10 / 8)
    avg_no2 = round(sum_no2 / 8)
    avg_so2 = round(sum_so2 / 8)
    aqi_object = AQI(avg_pm10, avg_no2, avg_so2)
    aqi_val, msg, level, advisory = aqi_object.get_aqi()
    params = {'date': date, 'pm10': avg_pm10, 'no2': avg_no2, 'so2': avg_so2, 'aqi': aqi_val, 'msg': msg, 'model': 'Average', 'level': level, 'advisory': advisory}
    return render(request, 'result3.html', params)
