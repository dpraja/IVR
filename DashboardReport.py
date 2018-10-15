import datetime
import json
from sqlwrapper import dbget,dbput,gensql
def Lastreportrecord():
     
   RES_Log_Date = datetime.datetime.utcnow().date()
   print(RES_Log_Date)
   RES_Log_Time = datetime.datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)
   sql = json.loads(dbget("select customer_mobile, customer_confirmation_number,booked_date from ivr_room_customer_booked\
                            where DATE(customer_arrival_date) = DATE(NOW()) and customer_booked_status in('booked')   order by booked_date  limit 4 "))
   print(sql)
   
   return(json.dumps({"Return_value":sql,"Return_code":"Success"},indent=2))

def lastreservationcount():
   RES_Log_Date = datetime.datetime.utcnow().date()
   print(RES_Log_Date)
   psql = json.loads(dbget("select count(send_sms) from ivr_room_customer_booked \
                            where send_sms in ('success') and customer_booked_status in('booked')  and DATE(booked_date) = '"+str(RES_Log_Date)+"' order by booked_date  limit 4"))
   print(psql)
   psql1 = json.loads(dbget("select count(*) from ivr_room_customer_booked \
                            where customer_booked_status in('booked')  and DATE(booked_date) = '"+str(RES_Log_Date)+"' order by booked_date  limit 4"))
   print(psql1)
   car1 = {
       "Sms_count":psql[0]['count'],
       "reservation":psql1[0]['count']
       }
   print(car1)
   return(json.dumps({"Return_value":car1,"Return_code":"Success"},indent=2))
#lastreservationcount()

def lastchannelrecord():

   RES_Log_Date = datetime.datetime.utcnow().date()
   print(RES_Log_Date)
   sql = json.loads(dbget("select customer_mobile,channel,booked_date from ivr_room_customer_booked \
                     where customer_booked_status in('booked') and channel in ('whatsapp') and  DATE(booked_date) = '"+str(RES_Log_Date)+"' order by booked_date  limit 2 "))
  
   psql = json.loads(dbget("select customer_mobile,channel,booked_date from ivr_room_customer_booked \
                     where customer_booked_status in('booked') and channel in ('IVR') and  DATE(booked_date) = '"+str(RES_Log_Date)+"' order by booked_date  limit 2 "))
   print(psql)
   sql = sql + psql
   print(sql)
   return(json.dumps({"Return_value":sql,"Return_code":"Success"},indent=2))
#lastchannelrecord() 
