import cStringIO
import time
from pandas.core.frame import DataFrame
from sqlalchemy import create_engine
from impala.dbapi import connect
import pandas as pd
start = time.time()
conn = connect(host='slave2', port=21050)
cursor1 = conn.cursor()
cursor1.execute('select * from test.ct_data where gprs_error>(select avg(gprs_error)+3*stddev(gprs_error) from test.ct_data) order by gprs_error')
result = cursor1.fetchall()
df_result = DataFrame(result)
df_result.columns = ['user_id','room_id','battery_1_v','battery_1','battery_2_v','bayyery_2','door','local','silence','voice','wifi','gprs','gprs_error','time','open_type']
db = create_engine('mysql+mysqldb://root:123456@localhost:3306/test')
pd.io.sql.to_sql(df_result,'result_out', db, schema='test', index=False,if_exists='replace')
print("Done")
end  = time.time()
print("Time:") , (end - start)