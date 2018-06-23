#from pyhive import hive
from pyspark import SparkConf, SparkContext 
from pyspark.sql import HiveContext 
import pymysql
import pandas as pd

conf = (SparkConf() 
         .setAppName("My app")) 
sc = SparkContext(conf = conf) 
sqlContext = HiveContext(sc) 
df = sqlContext.sql("Select count(*),avg(gprs_error),stddev(gprs_error) from test.ct_data") 
ddf=pd.DataFrame(df.collect())

count, average,std=ddf.loc[0,0],ddf.loc[0,1],ddf.loc[0,2]

db = pymysql.connect("localhost", "root", "123456", "test", charset='utf8' )
cursor = db.cursor()
sql = "insert into ct_data_out(user_count ,gprs_error_average, gprs_error_std) values ('%f', '%f','%f')" % (count, average,std+1)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    
db.close()
print("Done")