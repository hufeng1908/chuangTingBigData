from impala.dbapi import connect
import pymysql
conn = connect(host='slave2', port=21050)
cursor = conn.cursor()
cursor.execute('SELECT count(*),avg(gprs_error),stddev(gprs_error) FROM test.ct_data')
#print cursor.description  # prints the result set's schema
results = cursor.fetchall()
(count, average,std)=results[0]
db = pymysql.connect("localhost", "root", "123456", "test", charset='utf8' )
cursor = db.cursor()
sql = "insert into ct_data_out(user_count ,gprs_error_average,gprs_error_std) values ('%f', '%f','%f')" % (count, average,std)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    
db.close()
print("Done")