# libraries
import pyodbc
import pandas as pd

# Initializing variables
source_file = '/Users/mrkfw/Documents/GitHub/Tasker/src/source.txt'
destination_file = '/Users/mrkfw/Documents/GitHub/Tasker/src/destination.txt'
select_query_file = '/Users/mrkfw/Documents/GitHub/Tasker/src/select.sql'
update_query_file = '/Users/mrkfw/Documents/GitHub/Tasker/src/update.sql'
dsn = ''
cols = ['ACAD_GROUP', 'TERM', 'STRM', 'SESSION_CODE', 'CLASS_NBR', 'CRSE_ID', 'SUBJECT', 'CATALOG_NBR', 'CLASS_SECTION',
        'DESCR', 'INSTRUCTOR_ID', 'GRADE', 'EMPLID', 'LAST_NAME', 'FIRST_NAME', 'GRD_RSTR_TYPE_SEQ', 'ACAD_CAREER']

# Connecting to data server
with pyodbc.connect('DSN={}'.format(dsn)) as connection:
    # step1
    # reading the data from server
    with open(select_query_file, 'r') as f:
        select_sql = f.read()
    output1 = pd.read_sql(select_sql, connection)

    #step2
    #compare output1 with source.txt
    source_df = pd.read_csv(source_file, sep='\t', dtype=str)
    source_df.head()
    output2 = pd.merge(
        source_df
        , output1
        , how='inner'
        , on=['CLASS_NBR', 'EMPLID']
        , suffixes=('', '_y')
    )

    #step3
    #write into the destination file from the output2
    final_output = output2[cols]
    final_output['GRADE'] = output2['GRADE_y'].values
    final_output.to_csv(destination_file, sep='\t', index=False)

    #step4
    #update into the data server
    with open(update_query_file, 'r') as f:
        update_sql = f.read()
        cursor = connection.cursor()
        cursor.execute(update_sql)
        connection.commit()
        cursor.close()
print('Grade Roaster Completed!')
