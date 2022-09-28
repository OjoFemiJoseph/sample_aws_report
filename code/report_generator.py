import pandas as pd
from datetime import datetime

def combine_service(column_one_service_name,column_two_service_name):
    """
    return the first service name if it is not nan
    nan has a data type of float
    """
    if isinstance(column_one_service_name,str):
        return column_one_service_name
    return column_two_service_name
    
def get_dates_from_filenames(lst):
    """
    Get dates from filenames
    """
    filename = '-'.join([' '.join(' '.join(i.split()[3:]).replace('_',' ').split()[:3]) for i in lst ])
    date_last_week,date_current_week = filename.split('-')
    last_week= f'Week Of {date_last_week} Savings'
    current_week= f'Week Of {date_current_week} Savings'
    return last_week,current_week
def generate_file_name():
    """
    Generate file name
    """
    todays_date = datetime.now()
    in_pd = pd.Timestamp(todays_date)
    name_of_file = f"Week of {in_pd.month_name()} {in_pd.day}, {in_pd.year}_Offside_report"
    return name_of_file

def preprocess(week1,week2,filenames):
    outer = pd.merge(week1,week2,on=['Amazon Name','Resource Id'],how='outer')
                

    #the two service column was passed to a user defined function that takes one of the service name in both columns (The chosen service name wont be nan)
    outer['Service'] = outer.apply(lambda service: combine_service(service['Service_x'], service['Service_y']), axis=1)

    
    outer.drop(['Service_x','Service_y'],axis=1,inplace=True)   

    last_week, current_week = get_dates_from_filenames(filenames)    
    col_dict = {'Potential Savings_x': last_week,'Potential Savings_y': current_week} 

    outer.rename(columns=col_dict,inplace=True)

    #fill nan/null fields with 0.0
    outer.fillna(0.00,inplace=True)

    outer['Total Savings'] = outer[col_dict['Potential Savings_x']] + outer[col_dict['Potential Savings_y']]

    #filename example: August 22 2022-August 29 2022 Report
    report_dir = generate_file_name()

    return report_dir, outer



if '__main__' == __name__:
    preprocess()