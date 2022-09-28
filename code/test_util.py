import boto3
import os
from moto import mock_s3
from s3_util import s3Handler
import unittest
import pandas as pd


class MyTest(unittest.TestCase):
    mock_s3 = mock_s3()

    os.environ['INPUT_BUCKET'] = 'test'
    os.environ['OUTPUT_BUCKET'] = 'test'
    def setUp(self):
        self.mock_s3.start()
        self.s3_client = boto3.client('s3')
        self.s3_client.create_bucket(Bucket='test')
        self.s3_handler = s3Handler()

    def tearDown(self):
        self.mock_s3.stop()

    def test_upload(self):    
        df = pd.DataFrame()
        self.s3_handler.upload(df,'test.csv')

        assert 'test.csv' in [i['Key'] for i in self.s3_client.list_objects(Bucket='test')['Contents']]
    
    def test_list_object(self):
        df = pd.DataFrame()
        self.s3_handler.upload(df,'test a d August 25 2019_Total_Analysis.csv')
        self.s3_handler.upload(df,'test a d August 22 2019_Total_Analysis.csv')
        s3_obj =self.s3_handler.list_object()
        
        assert s3_obj[0] == 'test a d August 22 2019_Total_Analysis.csv'

    def test_get_object(self):
        df = pd.DataFrame()
        self.s3_handler.upload(df,'test a d August 25 2019_Total_Analysis.csv')
        obj = self.s3_handler.get_object('test a d August 25 2019_Total_Analysis.csv')
        
        

if '__main__' == __name__:
    unittest.main()