import sys, os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests
import json

from datetime import datetime, timedelta
import time


class fetcher:
    def __init__(self, browser_path = 'undefined'):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('-headless')
            
            driver_path = 'data_fetcher\\' + 'chromedriver.exe'
            if browser_path != 'undefined':
                options.binary_location = browser_path
                self.driver = webdriver.Chrome(executable_path = driver_path, options=options)
            else:
                self.driver = webdriver.Chrome(executable_path = driver_path, options=options)
            return
        except WebDriverException:
            pass
        
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            
            driver_path = 'data_fetcher\\' + 'geckodriver.exe'
            if browser_path != 'undefined':
                options.binary_location = browser_path
                self.driver = webdriver.Firefox(executable_path = driver_path, options=options)
            else:
                self.driver = webdriver.Firefox(executable_path = driver_path, options=options)
            return
        except WebDriverException:
            pass
        print('Only Google Chrome and Mozilla Firefox is supported')

    def get(self, target_date):
        tdate = target_date
        driver = self.driver
        driver.get('https://rp5.ru/Weather_archive_in_Kolkata,_Dum_Dum_(airport),_METAR')
        driver.implicitly_wait(30)
        time.sleep(3)
        
        
        driver.find_element_by_xpath('//*[@id="tabMetarArchive"]').click()
        
        
        text_field = driver.find_element_by_xpath('//*[@id="calender_archive"]')
       	text_field.clear()
       	text_field.send_keys(tdate)
       
       	driver.find_element_by_xpath('//*[@id="toScreenMenu"]/form/table/tbody/tr/td[5]/div').click()
       	time.sleep(5)
        
        t1 = driver.find_elements_by_class_name('cl_rd')
        t2 = driver.find_elements_by_class_name('cl_rd_nt')
        
        temp = 0
        for e in t1 + t2:
            temp += float(e.text)
        temp = temp / (len(t1) + len(t2))
        
        p1 = t1 = driver.find_elements_by_class_name('cl')
        p2 = t1 = driver.find_elements_by_class_name('cl_nt')
        
        ph = []
        for e in p1 + p2:
            try:
                ph.append(float(e.text))
            except ValueError:
                pass

        pressure = 0
        hv = 0
        i = 0
        while i < len(ph):
            if(i % 2 == 0):
                pressure += float(ph[i])
            else:
                hv += float(ph[i])
            i += 1
        
        pressure /= (len(ph) / 2)
        hv /= (len(ph) / 2)
        
        rl1 = driver.find_elements_by_class_name('cl_bl')
        rl2 = driver.find_elements_by_class_name('cl_bl_nt')
        
        rl = rl1 + rl2
        
        hum = 0
        dt = 0
        
        i = 0
        while i < len(rl):
            if i % 2 == 0:
                hum += float(rl[i].text)
            else:
                dt += float(rl[i].text)
            i += 1
        hum /= (len(rl) / 2)
        dt /= (len(rl) / 2)
        
        data_dict = {}
        data_dict['Air Temperature'] = [temp]
        data_dict['Pressure Station Level'] = [pressure]
        data_dict['Relative Humidity'] = [hum]
        data_dict['Horizontal Visibility'] = [hv]
        data_dict['Dew Point Temperature'] = [dt]
        
        driver.find_element_by_xpath('//*[@id="tabMetarStatist"]').click()
        time.sleep(3)
        
        tf1 = driver.find_element_by_xpath('//*[@id="calender_stat"]')
        tf1.clear()
        tf1.send_keys(tdate)
        
        tf2 = driver.find_element_by_xpath('//*[@id="calender_stat2"]')
        tf2.clear()
        tf2.send_keys(tdate)
        # driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div[10]/div/form/table/tbody/tr[3]/td/div[2]').click()
        driver.find_element_by_xpath('//*[@id="t_statist_synop_wv"]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="statistMenu"]/form/table/tbody/tr[3]/td/div[2]/div').click()
        time.sleep(3)
        data_dict['Wind Speed'] = [driver.find_element_by_xpath('//*[@id="statist_synop_data_6"]/table/tbody/tr[2]/td[2]/div[1]').text]
                
        d_list = tdate.split('.')
        ob_date = datetime(int(d_list[2]), int(d_list[1]), int(d_list[0]))
        
        start_date = datetime(ob_date.year, 1, 1)
        one_day_delta = timedelta(days = 1)
        day_no = 0
        while start_date <= ob_date:
            day_no += 1
            start_date += one_day_delta
        data_dict['Day No.'] = [str(day_no)]
        data_dict['Year'] = [str(ob_date.year)]
        
        r = requests.get("http://emis.wbpcb.gov.in/airquality/JSP/aq/districtwiseReport.jsp")
        
        post_result = requests.post("http://emis.wbpcb.gov.in/airquality/JSP/aq/fetch_val_ajax.jsp?district=013&date={}&type=districtavg".format(ob_date.strftime('%d/%m/20%y')))
        post_json = json.loads(post_result.text)
        if(post_json['status'] != '0'):
            for val in post_json['list']:
                if(val['pname'] == 'PM10'):
                    data_dict['PM10'] = [val['value'].strip()]
                elif(val['pname'] == 'NO2'):
                    data_dict['NO2'] = [val['value'].strip()]
                elif(val['pname'] == 'SO2'):
                    data_dict['SO2'] = [val['value'].strip()]
                    
        d_prev = ob_date - one_day_delta
        post_result = requests.post("http://emis.wbpcb.gov.in/airquality/JSP/aq/fetch_val_ajax.jsp?district=013&date={}&type=districtavg".format(d_prev.strftime('%d/%m/20%y')))
        post_json = json.loads(post_result.text)
        if(post_json['status'] != '0'):
            for val in post_json['list']:
                if(val['pname'] == 'PM10'):
                    data_dict['D-1 PM10'] = [val['value'].strip()]
                elif(val['pname'] == 'NO2'):
                    data_dict['D-1 NO2'] = [val['value'].strip()]
                elif(val['pname'] == 'SO2'):
                    data_dict['D-1 SO2'] = [val['value'].strip()]       
        return data_dict
    
    def close(self):
        self.driver.close()

# {'Air Temperature': [16.979591836734695],
#  'Pressure Station Level': [763.0775510204081],
#  'Relative Humidity': [75.08163265306122],
#  'Horizontal Visibility': [2.8857142857142866],
#  'Dew Point Temperature': [12.244897959183673],
#  'Day No.': ['21'],
#  'Year': ['2020'],
#  'PM10': ['162.94'],
#  'NO2': ['42.81'],
#  'SO2': ['14.24'],
#  'D-1 PM10': ['180.89'],
#  'D-1 NO2': ['70.19'],
#  'D-1 SO2': ['19.14']}