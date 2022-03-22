from util.sensorManager import Bme680_manager
from sql.sqlManager import SQL_Manager
import time



if __name__ == '__main__':
        
    
    sensor_manager = Bme680_manager()
    
    sql_manager = SQL_Manager()
    
    
    while True:
        
        time.sleep(2)
    
        sensor_data = sensor_manager.get_sensor_data()
        
        
        sql_manager.insert_row(sensor_data['temperature'],
                               sensor_data['humidity'],
                               sensor_data['gas_resistance'])
    


    