from utils import Bme680_manager, air_quality_index
from sql.sqlManager import SQL_Manager
import time



if __name__ == '__main__':
        
    
    sensor_manager = Bme680_manager()
    
    sql_manager = SQL_Manager()
    
    
    while True:
        
        time.sleep(2)
    
        sensor_data = sensor_manager.get_sensor_data()

	temp = sensor_data['temperature']
	hum = sensor_data['humidity']
	gas_resist = sensor_data['gas_resistance']

        air_quality = air_quality_index(temp, hum, gas_resist)
        
        sql_manager.insert_row(temp,
                               hum,
                               gas_resist)
    


    