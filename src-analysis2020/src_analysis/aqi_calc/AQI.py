class AQI:
  def __init__(self, ele_no2, ele_pm10, ele_so2):
    self.ele_no2 = ele_no2
    self.ele_pm10 = ele_pm10
    self.ele_so2 = ele_so2
    self.max_aqi = 0
    self.msg = ''
    self.level = ''
    self.advisory = ''

  def get_aqi(self):
    aqi_pm10 = self.get_aqi_from_pm10(self.ele_pm10)
    aqi_no2 = self.get_aqi_from_no2(self.ele_no2)
    aqi_so2 = self.get_aqi_from_so2(self.ele_so2)
    if aqi_pm10 > self.max_aqi:
      self.max_aqi = aqi_pm10
    if aqi_no2 > self.max_aqi:
      self.max_aqi = aqi_no2
    if aqi_so2 > self.max_aqi:
      self.max_aqi = aqi_so2
    self.msg, self.level, self.advisory = self.get_message(round(self.max_aqi))
    return self.max_aqi, self.msg, self.level, self.advisory

  def get_message(self, ele_aqi):
      msg = ''
      level = ''
      advisory = ''
      if ele_aqi >= 0 and ele_aqi <= 50:
          msg = 'Good'
          level = 'success'
          advisory = 'Minimal impact.'
      if ele_aqi >= 51 and ele_aqi <= 100:
          msg = 'Moderate'
          level = 'secondary'
          advisory = 'Unusually sensitive individuals should consider limiting prolonged outdoor exertion.'
      if ele_aqi >= 101 and ele_aqi <= 150:
          msg = 'Unhealthy for sensitive groups'
          level = 'warning'
          advisory = 'Children, active adults and people with respiratory disease, such as asthma should limit prolonged outdoor exertion.'
      if ele_aqi >= 151 and ele_aqi <= 200:
          msg = 'Unhealthy'
          level = 'info'
          advisory = 'Children, active adults and people with respiratory disease, such as asthma should avoid prolonged outdoor exertion; everyone else should limit prolonged outdoor exertion.'
      if ele_aqi >= 201 and ele_aqi <= 300:
          msg = 'Very Unhealthy'
          level = 'danger'
          advisory = 'Children, active adults and people with respiratory disease, such as asthma should avoid prolonged outdoor exertion; everyone else should limit prolonged outdoor exertion.'
      if ele_aqi >= 301 and ele_aqi <= 500:
          msg = 'Hazardous'
          level = 'dark'
          advisory = 'Everyone should avoid all outdoor physical activities.'
      return msg, level, advisory
  
  def get_aqi_from_pm10(self, ele_pm10):
    if ele_pm10 <= 100:
      res_aqi = ele_pm10
    elif ele_pm10 >= 101 and ele_pm10 <= 250:
      res_aqi = ((200 - 101) / (250 - 101)) * (ele_pm10 - 101) + 101
    elif ele_pm10 >= 251 and ele_pm10 <= 350:
      res_aqi = ((300 - 201) / (350 - 251)) * (ele_pm10 - 251) + 201
    elif ele_pm10 >= 351 and ele_pm10 <= 430:
      res_aqi = ((400 - 301) / (430 - 351)) * (ele_pm10 - 351) + 301
    else:
      res_aqi = ((500 - 401) / (530 - 431)) * (ele_pm10 - 431) + 401
    return res_aqi
  
  def get_aqi_from_no2(self, ele_no2):
    if ele_no2 >= 0 and ele_no2 <= 40:
      res_aqi = ((50 - 0) / (40 - 0)) * (ele_no2 - 0) + 0
    elif ele_no2 >= 41 and ele_no2 <= 80:
      res_aqi = ((100 - 51) / (80 - 41)) * (ele_no2 - 41) + 51
    elif ele_no2 >= 81 and ele_no2 <= 180:
      res_aqi = ((200 - 101) / (180 - 81)) * (ele_no2 - 81) + 101
    elif ele_no2 >= 181 and ele_no2 <= 280:
      res_aqi = ((300 - 201) / (280 - 181)) * (ele_no2 - 181) + 201
    else:
      res_aqi = ((400 - 301) / (400 - 281)) * (ele_no2 - 281) + 301
    return res_aqi
    
  def get_aqi_from_so2(self, ele_so2):
    if ele_so2 >= 0 and ele_so2 <= 40:
      res_aqi = ((50 - 0) / (40 - 0)) * (ele_so2 - 0) + 0
    elif ele_so2 >= 41 and ele_so2 <= 80:
      res_aqi = ((100 - 51) / (80 - 41)) * (ele_so2 - 41) + 51
    else:
      res_aqi = ((200 - 101) / (380 - 81)) * (ele_so2 - 81) + 101
    return res_aqi