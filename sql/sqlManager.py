import datetime as dt
from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bigQueryKeys.json"

class SQL_Manager:
    
    def __init__(self):
        self.project_id = "unilbigscaleanalytics"
        self.__client = bigquery.Client(project=self.project_id)
        
        dataset_ref = self.get_client().dataset("IoT_Project", project=self.project_id)
        
        self.__dataset = self.get_client().get_dataset(dataset_ref)
        
        # Create a reference to the "movies" table
        bme680_table_ref = dataset_ref.table("bme680")

        # Fetch the table (API request)
        self.__bme680_table = self.get_client().get_table(bme680_table_ref)
                
    
    
    def insert_row(self,
                   temperature: float,
                   humidity: float,
                   gas_resistance: float):
        
        rows_to_insert = [{'timestamp': dt.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                 'humidity': humidity, 
                 'gas_resistance': gas_resistance, 
                 'temperature': temperature}]
        
        insert_errors = self.get_client().insert_rows_json(
                                        self.get_bme680_table(),
                                        rows_to_insert)
        if len(insert_errors) > 0:
            print(f"Error while inserting a row : {rows_to_insert[0]}")
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
        
    
    
    
    
    