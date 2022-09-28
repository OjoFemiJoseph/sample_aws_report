import pandas as pd
from s3_util import s3Handler
from report_generator import preprocess


def handler(event,context):
    s3_help = s3Handler()
    needed_columns = ['Amazon Name', 'Resource Id', 'Service','Potential Savings']
    last_two_weeks_file = s3_help.list_object()[-2:]
    last_week,current_week = last_two_weeks_file
    last_week_df = pd.read_csv(s3_help.get_object(last_week))[needed_columns]
    current_week_df = pd.read_csv(s3_help.get_object(current_week))[needed_columns ]
    report_dir, df = preprocess(last_week_df,current_week_df,last_two_weeks_file)
    s3_help.upload(df,report_dir)
    