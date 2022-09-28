import pandas as pd
from report_generator import preprocess
import os

path = os.path.join(os.getcwd(),'test_data')
os.chdir(path)

def test_report_generator():
    #change directory to test data root
    test_data_one_name = 'Updated Week of January 21_ 2018_Total_Analysis.csv'
    test_data_two_name = 'Updated Week of January 28_ 2018_Total_Analysis.csv'
    needed_columns = ['Amazon Name', 'Resource Id', 'Service','Potential Savings']
    test_data_one_df = pd.read_csv(test_data_one_name)[needed_columns]
    test_data_two_df = pd.read_csv(test_data_two_name)[needed_columns]
    #read file one
    #read file two

    report_dir,result = preprocess(test_data_one_df ,test_data_two_df,[test_data_one_name,test_data_two_name])
    actual_result = pd.read_csv('answers.csv')
    columns = ['Week Of January 21 2018 Savings','Week Of January 28 2018 Savings','Total Savings']
    for i in columns:
        result[i] = result[i].apply(lambda x: int(100*x))
        actual_result[i] = actual_result[i].apply(lambda x: int(100*x))


    print(result.equals(actual_result))
    
    #compare the result

test_report_generator()
