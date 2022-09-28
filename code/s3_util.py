import boto3
import os
from datetime import datetime
from io import StringIO

class s3Handler:

    def __init__(self):
        
        self.s3_client = boto3.client('s3')
        self.input_bucket_name = os.environ['INPUT_BUCKET']
        self.output_bucket_name = os.environ['OUTPUT_BUCKET']

    def __sort_file_names(self,file_names):
        """
        private function to sort filenames
        """
        output = sorted(file_names, key=lambda file: datetime.strptime(' '.join(' '.join(file.split()[3:]).replace('_',' ').split()[:3]), '%B %d %Y'))

        return output

    def upload(self,dataframe,filename):
        buffer = StringIO()
        dataframe.to_csv(buffer, header=True, index=False)
        report_dir = filename
        self.s3_client.put_object(Bucket=self.output_bucket_name, Body=buffer.getvalue(), Key=report_dir)
        

    def list_object(self):
        filename = [i['Key'] for i in self.s3_client.list_objects(Bucket=self.input_bucket_name)['Contents'] if i['Key'].endswith('_Total_Analysis.csv')]
        sorted_names = self.__sort_file_names(filename)
        
        return sorted_names

    def get_object(self,file_name):
        """
        get a specfic file
        """
        
        csv_obj = self.s3_client.get_object(Bucket=self.input_bucket_name, Key=file_name)
        body = csv_obj['Body']
        
        return body