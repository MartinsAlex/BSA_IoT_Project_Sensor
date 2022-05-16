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
         sensor = self.get_sensor()
         sensor.get_sensor_data() # function from original lib, to update sensor inputs
         return {'humidity': sensor.data.humidity,
                    'gas_resistance': sensor.data.gas_resistance,
                    'temperature': sensor.data.temperature}
    
        
    def get_sensor(self):
        return self.__sensor
    
    
def air_quality_index(temp, hum, gas):

    hum_baseline = 40
    hum_weighting = 0.25
    gas_baseline = 35347.80 # avg on previous collected data
    
    gas_offset = gas_baseline - gas

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
        gas_score = (gas / gas_baseline)
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
