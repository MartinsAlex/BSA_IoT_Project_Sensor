import bme680


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
        
        return {'humidity': self.get_sensor().data.humidity,
                'gas_resistance': self.get_sensor().data.gas_resistance,
                'temperature': self.get_sensor().data.temperature}
    
        
    def get_sensor(self):
        return self.__sensor
    
    
    