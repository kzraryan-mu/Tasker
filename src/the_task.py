# libraries
import pyodbc
import pandas as pd

# Initializing variables
source_file = 'source.txt'
destination_file = 'destination.txt'
select_query_file = 'select.sql'
update_query_file = 'update.sql'
dsn = ''

# Connecting to data server
with pyodbc.connect('DSN={}'.format(dsn)) as connection:
    # step1
    # reading the data from server
    with open(select_query_file, 'r') as f:
        select_sql = f.read()
    output1 = pd.read_sql(select_sql, connection)

    #step2
    #compare output1 with source.txt
    source_df = pd.read_csv(source_file)


    #step3
    #write into the destination file from the output2


    #step4
    #update into the data server
    with open(update_query_file, 'r') as f:
        update_sql = f.read()
print(select_sql)
