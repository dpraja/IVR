from sqlwrapper import gensql,dbget,dbput
import json
import random
import datetime
def insertcustomerroombooking(request):
     try: 
        d = request.json
        print(d)
        e = { k : v for k,v in d.items() if k not in ('customer_room_type','customer_name','TFN','customer_arrival_date','customer_depature_date','customer_expirydate')}
        print(e)
        tfn = request.json['TFN']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        customer_name = request.json["customer_name"]
        if len(customer_name) == 0: 
            customer_name  = "Customer"
        e['customer_name'] = customer_name    
        #print(customer_name)
        customer_room_type = request.json['customer_room_type']
        customer_room_type = customer_room_type.title()
        print(customer_room_type)
        customer_arrival_date = request.json["customer_arrival_date"]
        customer_depature_date = request.json["customer_depature_date"]
        customer_expirydate = request.json["customer_expirydate"]
        language = request.json['ivr_language']
        cntry = request.json['cntry_code']
        customer_expirydate = customer_expirydate[0:2]+'/'+customer_expirydate[2:]
        e['customer_expirydate'] = customer_expirydate
        today_date = datetime.datetime.utcnow().date()
        year = str(today_date.year)
        if int(customer_arrival_date[0:2]) == today_date.month :
            if int(customer_arrival_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_arrival_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_arrival_date = year+'-'+customer_arrival_date[0:2]+'-'+customer_arrival_date[2:]
        e['customer_arrival_date'] = customer_arrival_date
        if int(customer_depature_date[0:2]) == today_date.month :
            if int(customer_depature_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_depature_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_depature_date = year+'-'+customer_depature_date[0:2]+'-'+customer_depature_date[2:]
        e['customer_depature_date'] = customer_depature_date
        #print(customer_arrival_date,customer_depature_date)
        arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
        depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()        
        str_date = "'"+str(arrival_date)+"'"
        while arrival_date < depature_date:
              arrival_date = arrival_date+datetime.timedelta(days=1)
              str_date += ","+"'"+str(arrival_date)+"'"
        #print(str_date)
        conf_no = (random.randint(1000000000,9999999999))
        e['customer_confirmation_number'] = conf_no
        e['customer_booked_status'] = 'booked'
        e['customer_booked_date'] = today_date
        e['id'] = b_id[0]['id']
        e['customer_room_type'] = customer_room_type
        e['ivr_language'] = language
        e['cntry_code'] = cntry
        print(gensql('insert','ivr_room_customer_booked',e))
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        #print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        id_bus = json.loads(dbget("select id from extranet_room_list where business_id ='"+bi_id[0]['business_id']+"' \
                                   and room_type= '"+customer_room_type+"' "))
        #print(id_bus[0]['id'])
        print(dbput("update extranet_availableroom set available_count = available_count-1 where \
                       id= "+str(id_bus[0]['id'])+" and room_date in ("+str_date+")"))
        
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","conf_no":conf_no}))
     except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))
