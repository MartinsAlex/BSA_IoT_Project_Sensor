import bme680
import requests
import time

LAUSANNE_LATITUDE = 46.52751093142267
LAUSANNE_LONGITUDE = 6.626519003698495



class Bme680_manager:
    
    def __init__(self):
        
        try:
            self.__sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.__sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        
        
        self.__sensor.set_humidity_oversample(bme680.OS_2X)
        self.__sensor.set_pressure_oversample(bme680.OS_4X)
        self.__sensor.set_temperature_oversample(bme680.OS_8X)
        self.__sensor.set_filter(bme680.FILTER_SIZE_3)
        self.__sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        self.__sensor.set_gas_heater_temperature(320)
        self.__sensor.set_gas_heater_duration(150)
        self.__sensor.select_gas_heater_profile(0)
                


    
    def get_sensor_data(self):
         sensor = self.get_sensor()
         sensor.get_sensor_data() # function from original lib, to update sensor inputs
         return {'humidity': sensor.data.humidity,
                    'gas_resistance': sensor.data.gas_resistance,
                    'temperature': sensor.data.temperature}
    
        
    def get_sensor(self):
        return self.__sensor
    


class OpenWeatherMap_manager:
    
    def __init__(self, private_key_file):
        with open(f"{private_key_file}") as f:
            lines = f.readlines()
            self.private_key = lines[0]

    def get_outdoor_air_quality(self):
        r = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={self.private_key}').json()
        pm10 = r['list'][0]['components']['pm10']
        no2 = r['list'][0]['components']['no2']
        o3 = r['list'][0]['components']['o3']
        pm2_5 = r['list'][0]['components']['pm2_5']

        pm10_max = 180
        no2_max = 400
        o3_max = 240
        pm2_5_max = 110

        # Air quality index calculation, according to:
        # https://en.wikipedia.org/wiki/Air_quality_index#CAQI

        outdoor_air_quality_index = ((1 - pm10 / pm10_max) + (1 - no2 / no2_max) + (1 - o3 / o3_max) + (1 - pm2_5 / pm2_5_max)) / 4

        return outdoor_air_quality_index*100

    def get_outside_humidity_and_temperature(self):
        
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={self.private_key}&units=metric").json()
        
        return {'outside_temperature': r['main']['temp'],
                'outside_humidity': r['main']['humidity']}



def air_quality_index(temp, hum, gas, baseline):

    hum_baseline = 40
    hum_weighting = 0.25
    
    gas_offset = baseline - gas

    hum_offset = hum - hum_baseline

    # Calculate hum_score as the distance from the hum_baseline.
    if hum_offset > 0:
        hum_score = (100 - hum_baseline - hum_offset)
        hum_score /= (100 - hum_baseline)
        hum_score *= (hum_weighting * 100)

    else:
        hum_score = (hum_baseline + hum_offset)
        hum_score /= hum_baseline
        hum_score *= (hum_weighting * 100)

    # Calculate gas_score as the distance from the gas_baseline.
    if gas_offset > 0:
        gas_score = (gas / baseline)
        gas_score *= (100 - (hum_weighting * 100))

    else:
        gas_score = 100 - (hum_weighting * 100)

    # Calculate air_quality_score.
    air_quality_score = hum_score + gas_score


    print('Gas: {0:.2f} Ohms,humidity: {1:.2f} %RH,air quality: {2:.2f}'.format(
        gas,
        hum,
        air_quality_score))
    
    
    return air_quality_score

   
def compute_gas_baseline(sensor):

    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
    start_time = time.time()
    curr_time = time.time()
    burn_in_time = 180
    burn_in_data = []
    print('Collecting gas resistance burn-in data for 3 mins\n')
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data():
            gas = sensor.get_sensor_data()['gas_resistance']
            burn_in_data.append(gas)
            print('Gas: {0} Ohms'.format(gas))
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0

    return gas_baseline



if __name__ == '__main__':
    pass