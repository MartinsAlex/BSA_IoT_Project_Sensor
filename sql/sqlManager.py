import datetime as dt
from google.cloud import bigquery
import os


class SQL_Manager:
    
    def __init__(self, secret_key_file):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secret_key_file
        
        self.project_id = "unilbigscaleanalytics"
        self.__client = bigquery.Client(project=self.project_id)
        
        dataset_ref = self.get_client().dataset("IoT_Project", project=self.project_id)
        
        self.__dataset = self.get_client().get_dataset(dataset_ref)
        
        # Create a reference to the "movies" table
        bme680_table_ref = dataset_ref.table("bme680")

        # Fetch the table (API request)
        self.__bme680_table = self.get_client().get_table(bme680_table_ref)
    
    
    def insert_row(self,
                   indoor_temperature: float,
                   indoor_humidity: float,
                   indoor_gas_resistance: float,
                   indoor_air_quality: float,
                   outdoor_temperature: float,
                   outdoor_humidity: float,
                   outdoor_air_quality: float):
        
        rows_to_insert = [{'timestamp': dt.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                 'indoor_humidity': indoor_humidity, 
                 'indoor_gas_resistance': indoor_gas_resistance, 
                 'indoor_temperature': indoor_temperature,
                'indoor_air_quality': indoor_air_quality,
                'outdoor_temperature': outdoor_temperature,
                'outdoor_humidity': outdoor_humidity,
                'outdoor_air_quality': outdoor_air_quality}]
        
        insert_errors = self.get_client().insert_rows_json(
                                        self.get_bme680_table(),
                                        rows_to_insert)
        if len(insert_errors) > 0:
            print(f"Error while inserting a row : {insert_errors}")
        else:
            print(f"Successfully inserted a row: {rows_to_insert[0]}")
        
        
        
    def get_client(self):
        return self.__client
        
        
    def get_dataset(self):
        return self.__dataset
    
    
    def get_bme680_table(self):
        return self.__bme680_table


        

if __name__ == '__main__':
    pass
        
    
    
    
    
    
