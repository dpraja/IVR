from sqlwrapper import gensql,dbget,dbput
import json
import datetime
import random
import urllib
from dateutil import parser
def Inserttwilioreservation(request):
    d = request.json
    
    roomtype = request.json['customer_room_type']
    arr = request.json['customer_arrival_date']
    name = request.json['customer_name']
    email = request.json['customer_email']
    dep = request.json['customer_depature_date']
    arr = parser.parse(arr).date().strftime('%d-%m-%Y')
    dep = parser.parse(dep).date().strftime('%d-%m-%Y')
    arr_date = datetime.datetime.strptime(arr, '%d-%m-%Y').date()
    dep_date = datetime.datetime.strptime(dep, '%d-%m-%Y').date()
    confir = (random.randint(100000,999999))
    print(arr_date,dep_date)
    arr = arr_date.strftime("%Y-%m-%d")
    dep = dep_date.strftime("%Y-%m-%d")
    d['customer_arrival_date'] = arr
    d['customer_depature_date'] = dep
    d['customer_confirmation_number'] = confir
    d['modification'] = "No"
    d['customer_booked_status'] = "booked"
    d['customer_room_type'] = roomtype.title()
    d['customer_name'] = name
    d['customer_email'] = email
    sql = gensql('insert','public.ivr_room_customer_booked',d)
    print(sql)
    confirmation= d.get("customer_confirmation_number")
    return(json.dumps([{"Return":"Record Inserted Succcessfully","Returncode":"RIS","Status":"Success","Statuscode":200,"confirmation_number":confirmation}],indent=2))

def InsertArrivalDeparture(request):
    
    d = request.json
    print(d)
    try:
        #e = { k : v for k,v in d.items() if v = '' }       
        #print(e)
        today_date = datetime.datetime.utcnow().date()
        print(today_date)
        '''
        arrival = e['arrival']
        depature = e['departure']
        print(arrival,depature,type(arrival))
        arr_date = datetime.datetime.strptime(arrival, '%Y-%m-%d').date()
        dep_date = datetime.datetime.strptime(depature, '%Y-%m-%d').date()
        print("str1", arr_date,dep_date,type(arr_date))
        '''
        data1 = d.get('customer_arrival_date')
        data2 = d.get('customer_depature_date')
        date1 = parser.parse(data1).date().strftime('%d-%m-%Y')
        date2 = parser.parse(data2).date().strftime('%d-%m-%Y')    
        arr_date = datetime.datetime.strptime(date1, '%d-%m-%Y').date()     #datetime format
        dep_date = datetime.datetime.strptime(date2, '%d-%m-%Y').date()
        arr_date = arr_date.strftime("%Y-%m-%d")                             #formatted string datetime
        dep_date = dep_date.strftime("%Y-%m-%d")
        arr_date = datetime.datetime.strptime(arr_date, '%Y-%m-%d').date()   #convert string to datetime format
        dep_date = datetime.datetime.strptime(dep_date, '%Y-%m-%d').date()
        print(arr_date,dep_date)
        restrict_days =  today_date + datetime.timedelta(days=90)
        print(restrict_days)
        #charges_end_date = datetime.datetime.strptime(data2, '%Y-%m-%d').date()
        #print("str2",charges_begin_date,charges_end_date,type(charges_end_date))
        d['arrival'] = arr_date
        d['departure'] = dep_date
        if arr_date >= today_date:
            if  dep_date >= arr_date :    
                if dep_date <= restrict_days:
                   #sql_value = gensql('insert','reservation',d)
                   return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Given dates are valid','ReturnCode':'Valid'}], sort_keys=True, indent=4))
                else:   
                   return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'departure date should not exceed 90 days than arrival','ReturnCode':'Invalid'}], sort_keys=True, indent=4))
            else:
                
               return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Departure date should not be in past date than arrival','ReturnCode':'Invalid'}], sort_keys=True, indent=4))
        else:
            
             return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'arrival date must be scheduled atleast one day in advance','ReturnCode':'Invalid'}], sort_keys=True, indent=4))
    except:
         return(json.dumps([{'Status': 'Success', 'StatusCode': '200','ReturnCode':'Invalid'}], sort_keys=True, indent=4))

        

def Modifytwilioreservation(request):
    d = request.json
           
    a = { k : v for k,v in d.items() if v != '' if k not in ('customer_confirmation_number','customer_arrival_date','customer_depature_date')}
    print(a)
    e = { k : v for k,v in d.items() if k != '' if k in ('customer_confirmation_number')}
    print(e)

    data1 = d.get('customer_arrival_date')
    data2 = d.get('customer_depature_date')
    date1 = parser.parse(data1).date().strftime('%d-%m-%Y')
    date2 = parser.parse(data2).date().strftime('%d-%m-%Y')    
    arr_date = datetime.datetime.strptime(date1, '%d-%m-%Y').date()     #datetime format
    dep_date = datetime.datetime.strptime(date2, '%d-%m-%Y').date()
    a['customer_arrival_date'] = arr_date.strftime("%Y-%m-%d")                             #formatted string datetime
    a['customer_depature_date'] = dep_date.strftime("%Y-%m-%d")
    #a['arrival'] = parser.parse(d['arrival']).date().strftime('%d-%m-%Y')
    #a['departure'] = parser.parse(d['departure']).date().strftime('%d-%m-%Y')

    
    sql_value = gensql('update','ivr_room_customer_booked',a,e)
    print(sql_value)
    conf = e.get('confirmation_number')
    sql = dbput("update ivr_room_customer_booked set modification = 'yes' where customer_confirmation_number = '"+str(conf)+"'")
    return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Record Updated Successfully','ReturnCode':'RUS'}], sort_keys=True, indent=4))

def Canceltwilioreservation(request):
    d  = request.json
    conf = d.get('confirmation_number')
    status = 'Canceled'

    sql = dbput("update ivr_room_customer_booked set customer_booked_status = '"+status+"' where customer_confirmation_number = '"+conf+"'")
    print(sql)
    
    return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Your booking has been cancelled','ReturnCode':'RCS'}], sort_keys=True, indent=4))

def Smstwilioservice(request):
     countrycode = request.json['countrycode']
     #print(countrycode)
     name = 'Customer'
     phone = request.json['phone']
     message = request.json['message']
     conf_no = request.json['conf_no']
     hotel_name = 'Konnect'
     arrival = request.json['arrival']
     depature = request.json['depature']
     room_type = request.json['room_type']
     all_message = ("Dear "+name+", "+message+".  Confirmation Number is "+conf_no+", Arrival Date: "+arrival+", Depature Date:"+depature+", Room Type:"+room_type+". by "+hotel_name+"")
     url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles="+phone+"&message="+all_message+"&sender=Infoit&route=4&country="+countrycode+""
     req = urllib.request.Request(url)
     with urllib.request.urlopen(req) as response:
         the_page = response.read()
         the_page = the_page[1:]
         print(the_page)
         the_page = str(the_page)
     sql = dbput("update ivr_room_customer_booked set send_sms = 'success' where customer_confirmation_number = '"+conf_no+"'")
     print(sql)
     return(json.dumps([{"Return":"SMS Sent Successfully","Return_Code":"SSS","Status": "Success","Status_Code": "200","Key":the_page}],indent =2))

def CheckConfirmation(request):
     
     conf_no = request.json['confirmation_number']
     sql = json.loads(dbget("select count(*) from ivr_room_customer_booked where customer_confirmation_number='"+conf_no+"'"))
     psql = json.loads(dbget("select count(*) from ivr_room_customer_booked where customer_confirmation_number='"+conf_no+"' and customer_booked_status in ('booked')"))
     print(psql)
     if sql[0]['count'] > 0 and psql[0]['count'] > 0 :
         return(json.dumps([{"Return":"Confirmation number already exist","Return_Code":"Valid","Status": "Success","Status_Code": "200"}],indent =2))
     else:
         return(json.dumps([{"Return":"Confirmation number does not exist","Return_Code":"Invalid","Status": "Success","Status_Code": "200"}],indent =2))
