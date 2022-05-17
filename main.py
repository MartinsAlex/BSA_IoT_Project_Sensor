from utils import Bme680_manager, air_quality_index, OpenWeatherMap_manager, compute_gas_baseline
from sql.sqlManager import SQL_Manager
import time



if __name__ == '__main__':
    
    
    sensor_manager = Bme680_manager()
    



    sql_manager = SQL_Manager("/home/pi/Desktop/bigQueryKeys.json",
                              "unilbigscaleanalytics",
                              "IoT_Project",
                              "bme680")

    openWeather_manager = OpenWeatherMap_manager("/home/pi/Desktop/openWeatherMapKeys.txt")
    
    gas_baseline = compute_gas_baseline(sensor_manager)

    
    while True:
        
        time.sleep(60)
    
        sensor_data = sensor_manager.get_sensor_data()

        indoor_temp = sensor_data['temperature']
        indoor_hum = sensor_data['humidity']
        indoor_gas_resist = sensor_data['gas_resistance']


        indoor_air_quality = air_quality_index(indoor_temp, 
                                        indoor_hum, 
                                        indoor_gas_resist,
                                        gas_baseline)
        
        try:
            outdoor_temp_hum = openWeather_manager.get_outside_humidity_and_temperature()


            sql_manager.insert_row(indoor_temp,
                                   indoor_hum,
                                   indoor_gas_resist,
                                   indoor_air_quality,
                                   outdoor_temp_hum['outside_temperature'],
                                   outdoor_temp_hum['outside_humidity'],
                                   openWeather_manager.get_outdoor_air_quality())
        
        except Exception as e:
            print('An exception occurred: {}'.format(e))

    


    
