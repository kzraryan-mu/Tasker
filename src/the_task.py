# libraries
import pandas as pd
import pyodbc

# Initializing variables
source_file = r'\\msits-srv-pdsql\ApplicationTeamNetworkShare\GradeRoster\GradeRosterEmpty.txt'
destination_file = r'\\msits-srv-pdsql\ApplicationTeamNetworkShare\GradeRoster\GradeRosterFilled.txt'
select_query_file = r'\\msits-srv-pdsql\ApplicationTeamNetworkShare\GradeRoster\GradeTransmission.sql'
update_query_file = r'\\msits-srv-pdsql\ApplicationTeamNetworkShare\GradeRoster\UpdateGradeStatus.sql'
updated_file = r'\\msits-srv-pdsql\ApplicationTeamNetworkShare\GradeRoster\updated.txt'
dsn = 'RIME PROD'
cols = ['ACAD_GROUP', 'TERM', 'STRM', 'SESSION_CODE', 'CLASS_NBR', 'CRSE_ID', 'SUBJECT', 'CATALOG_NBR', 'CLASS_SECTION',
        'DESCR', 'INSTRUCTOR_ID', 'GRADE', 'EMPLID', 'LAST_NAME', 'FIRST_NAME', 'GRD_RSTR_TYPE_SEQ', 'ACAD_CAREER']

# Connecting to data server
with pyodbc.connect('DSN={}'.format(dsn)) as connection:
    # step0
    # updating database by comparing source and destination file
    source_df = pd.read_csv(source_file, sep='\t', dtype=str)
    source_df.head()
    destination_df = pd.read_csv(destination_file, sep='\t', dtype=str, names=cols)
    output0 = pd.merge(
        destination_df
        , source_df
        , how='left'
        , on=['CLASS_NBR', 'EMPLID']
        , suffixes=('', '_y')
        , indicator=True
    ).dropna(subset=['CLASS_NBR', 'EMPLID'])
    destination_df_2 = output0[output0['_merge'] == 'left_only']
    destination_df_2[cols].to_csv(updated_file, sep='\t', index=False, header=False)
    if destination_df_2.size > 0:
        class_nbr_emplid = []
        for index, row in destination_df_2.iterrows():
            class_nbr_emplid.append(row['CLASS_NBR'] + '_' + row['EMPLID'])
        str_class_nbr_emplid = "','".join(class_nbr_emplid)
        with open(update_query_file, 'r') as f:
            update_sql = f.read()
            update_sql.replace('CLASS_NBR_EMPLID', str_class_nbr_emplid)
            cursor = connection.cursor()
            cursor.execute(update_sql)
            connection.commit()
            cursor.close()
    # step1
    # reading the data from server
    with open(select_query_file, 'r') as f:
        select_sql = f.read()
    output1 = pd.read_sql(select_sql, connection)

    # step2
    # compare output1 with source.txt
    output2 = pd.merge(
        source_df
        , output1
        , how='inner'
        , on=['CLASS_NBR', 'EMPLID']
        , suffixes=('', '_y')
    )

    # step3
    # write into the destination file from the output2
    final_output = output2[cols]
    final_output['GRADE'] = output2['GRADE_y'].values
    final_output.to_csv(destination_file, sep='\t', index=False, header=False)

    # step4
    # update into the data server
    # with open(update_query_file, 'r') as f:
    #    update_sql = f.read()
    #    cursor = connection.cursor()
    #    cursor.execute(update_sql)
    #    connection.commit()
    #    cursor.close()
print('Grade Roaster Completed!')
