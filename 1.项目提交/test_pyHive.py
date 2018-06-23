from pyhive import hive  
import pymysql
conn = hive.Connection(host='localhost', port=10000, username='root', database='test')  
cursor = conn.cursor()  
cursor.execute('select count(*),avg(gprs_error),stddev(gprs_error) from ct_data')  
results = cursor.fetchall()
(count, average,std)=results[0]
db = pymysql.connect("localhost", "root", "123456", "test", charset='utf8' )
cursor = db.cursor()
sql = "insert into ct_data_out(user_count ,gprs_error_average) values ('%f', '%f')" % (count, average)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    
db.close()
print("Done")