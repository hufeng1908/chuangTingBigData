# -*- coding: utf-8 -*-
import random
import datetime
import pymysql
import numpy as np
import re
import time





def excutesql(sqlprefix, valuess):
    if (len(valuess) == 0):
        return
    sql = sqlprefix
    for v in valuess:
        sql += v + ",\n"
    sql = sql.strip(",\n") + ";"


    conn = pymysql.connect(host='47.104.218.115', port=3306, user='root', passwd='123456', db='bi', charset='utf8')
    # print(sql)


    # 创建游标
    cursor = conn.cursor()

    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute(sql)

    # 执行SQL，并返回受影响行数
    # effect_row = cursor.execute("update tb7 set pass = '123' where nid = %s", (11,))

    # 执行SQL，并返回受影响行数,执行多次
    # effect_row = cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)", [("u1","u1pass","11111"),("u2","u2pass","22222")])

    # 提交，不然无法保存新建或者修改的数据
    conn.commit()

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

def nextuser():
    return str(random.randint(0,2800))

def nextArea():
    cities= ['济南',    '石家庄',    '西安',    '太原',    '上海',    '北京',    '广州',    '天津',    '重庆',    '拉萨',    '南京',    '沈阳',    '南宁',    '长春',    '哈尔滨',    '昆明',    '杭州',    '海口',    '成都',    '郑州',    '长沙',    '南昌',    '武汉',    '呼和浩特',    '合肥',    '贵阳',    '福州',    '兰州',    '银川',    '西宁',    '乌鲁木齐']
    return cities[random.randint(0,len(cities)-1)]

def nextprice():
    type =['CT-AT10','CT-BRFPDA-I4','CT-Q305/Q305Z','CT-C10F300','CT-H1-RFPDA-R9','CT-H2-RFPDA-Z','CT-AT10-plus','CT-BRFPDA-I4-plus','CT-Q305/Q305Z-plus','CT-C10F300-plus','CT-H1-RFPDA-R9-plus','CT-H2-RFPDA-Z-plus']
    name = ['标配版','旗舰版','豪华版','经典版','精英版','尊享版','标配增强版','旗舰增强版','豪华增强版','经典增强版','精英增强版','尊享增强版']
    price = [500,600,700,400,450,550,650,750,850,550,600,700]

    rid = random.randint(0,6)

    return type[rid], name[rid],price[rid]


## return a random time i  before current time
def nexttime(i):

    nowTime = datetime.datetime.now()+ datetime.timedelta(hours= -i,minutes=random.randint(0,60),seconds=random.randint(0,60))
    nowTimestr = nowTime.strftime('%Y-%m-%d %H:%M:%S')
    return nowTimestr

def nextprob(l,v):
    v = np.array(v)

    s = np.sum(v)
    v = v/s
    for i in range(1,len(v)):
        v[i]+=v[i-1]
    rr = random.random()
    for idx, vv in enumerate(v):
        if rr <= vv:
            return l[idx]
    return l[-1]

def nextnorm(u,s,maxv,minv):
    v = np.random.normal(u,s)
    v = max(v,minv)
    v = min(maxv,v)
    return int(v)

def nextsolve_state():
    l = [0,1,2]
    v = [2,3,5]
    return nextprob(l,v)

def nextservicetype():
    l = [0,1,2,3,4,5]
    v = [2,3,5,6,8,9]
    return nextprob(l,v)

def nextscore():
    return nextnorm(80,10,100,50)

def nextresponce_time():
    return nextnorm(15, 10, 60, 2)

def nextcomments():
    l = [0,1,2,3,4,5]
    v = [20,40,60,90,200,500]
    return nextprob(l, v)


def repair(flag):
    sqlprefix = " insert into bi.hwrepair (product_type,repair_status,comments,repair_time) values \n"



    valuess = []
    hours = 1
    if flag:
        hours = 1000 * 24
        sql = " truncate table bi.hwrepair"
        excutesql(sql)
    maxitem = 10
    if hours >1:
        base = np.log(maxitem) / np.log(hours)
    else:
        base = 0

    for i in range(hours):

        if hours >1:
            n = int(np.power(i, base)) + 1
        else:
            n = maxitem

        for j in range(random.randint(0, n)):
            values = ""
            l = [0, 1, 2, 3, 4]
            v = [1000, 500, 300, 200, 200]
            product_type = nextprob(l,v)
            repair_status = nextsolve_state()
            comments = nextcomments()
            repair_time = nexttime(i)

            values +=  str(product_type) + ","
            values += str(repair_status) + ","
            values += str(comments) + ","
            values += "'" + str(repair_time) + "'"
            values = "(" + values + ")"
            valuess.append(values)

            if (len(valuess) > 5000):
                excutesql(sqlprefix,valuess)
                valuess = []

    excutesql(sqlprefix, valuess)



def ct400(flag):
    sqlprefix = " insert into bi.cthotline (solve_state,score,responce_time,call_time,comments) values \n"

    valuess = []
    hours = 1
    if flag:
        hours = 1000 * 24
        sql = " truncate table bi.cthotline"
        excutesql(sql)
    maxitem = 50
    if hours >1:
        base = np.log(maxitem) / np.log(hours)
    else:
        base = 0

    for i in range(hours):

        if hours >1:
            n = int(np.power(i, base)) + 1
        else:
            n = maxitem

        for j in range(random.randint(0, n)):
            values = ""
            solve_state = nextsolve_state()
            score = nextscore()
            responce_time = nextresponce_time()
            call_time = nexttime(hours - i)
            comments = nextcomments()
            values += str(solve_state) + ","
            values += str(score) + ","
            values += str(responce_time) + ","
            values += "'" + str(call_time) + "',"
            values += str(comments)
            values = "(" + values + ")"
            valuess.append(values)

            if (len(valuess) > 5000):

                excutesql(sqlprefix,valuess)
                valuess = []



    excutesql(sqlprefix, valuess)


def nextaptname():
    l = re.split(",","蘑菇公寓,小米公寓,自如公寓,青年公寓,青稞公寓,魔方公寓,壹栈公寓,魔飞公寓")
    v = [200,100,400,200,140,20,100,50]
    return nextprob(l,v)


def ctservice(flag):
    sqlprefix = " insert into bi.ctservice (service_type,user_id,apt_name,room_id,price,paymethod,service_status,service_time) values \n"

    valuess = []
    hours = 1
    if flag:
        hours = 1000 * 24
        sql = " truncate table bi.ctservice"
        excutesql(sql)
    maxitem = 50

    if hours >1:
        base = np.log(maxitem) / np.log(hours)
    else:
        base = 0

    for i in range(hours):

        if hours >1:
            n = int(np.power(i, base)) + 1
        else:
            n = maxitem


        for j in range(random.randint(0, n)):
            values = ""
            service_type = nextservicetype()
            user_id = random.randint(0,2800)
            apt_name = nextaptname()
            room_id = random.randint(0,600)
            price = nextnorm(100,50,200,40)
            paymethod = nextprob([0,1,2,3],[10,80,90,2])
            service_status = nextprob([0,1],[10,90])
            service_time = nexttime(hours-i)

            values += str(service_type) + ","
            values += str(user_id) + ","
            values += "'" + str(apt_name) + "',"
            values += str(room_id) + ","
            values += str(price) + ","
            values += str(paymethod) + ","
            values += str(service_status) + ","
            values += "'" + str(service_time) + "'"

            values = "(" + values + ")"
            valuess.append(values)

            if (len(valuess) > 5000):
                sql = sqlprefix

                excutesql(sqlprefix,valuess)
                valuess = []



    excutesql(sqlprefix, valuess)







print(datetime.datetime.now())
# ctservice(True) # True表示清空表，倒推1000天，重新生成，False表示倒推1小时，不清空表
# repair(True)
# ct400(True)
# while(True):
#     print(datetime.datetime.now())
#     try:
#         repair(False)
#         ctservice(False)
#         ct400(False)
#     except:
#         time.sleep(10)
#     time.sleep(60*60)


ctservice(False) # True表示清空表，倒推1000天，重新生成，False表示倒推1小时，不清空表
repair(False)
ct400(False)

