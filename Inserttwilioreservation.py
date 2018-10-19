from sqlwrapper import gensql,dbget,dbput
import json
import datetime
import random
import urllib
from dateutil import parser
from decimal import Decimal
import math
def Inserttwilioreservation(request):
    d = request.json
    #amount = d['amount']
    d= {k:v for k,v in d.items() if k not in ('TFN')}
    tfn = request.json['TFN']
    b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
    print(b_id)
    bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
    print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
    roomtype = request.json['customer_room_type']
    arr = request.json['customer_arrival_date']
    dep = request.json['customer_depature_date']
    
    customer_arrival_date = parser.parse(arr).date().strftime('%Y-%m-%d')
    customer_depature_date = parser.parse(dep).date().strftime('%Y-%m-%d')
    customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
    customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

    today_date = datetime.datetime.utcnow().date()
    if customer_arrival_date < today_date:
            customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
    if customer_depature_date < today_date:
            customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
    print("arr",customer_arrival_date)
    print("dep",customer_depature_date)
    
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
    d['business_id'] = str(bi_id[0]['business_id'])
    
    sql = gensql('insert','public.ivr_room_customer_booked',d)
    print(sql)
    '''
    res = json.loads(gensql('select','public.ivr_room_customer_booked','cus_id',d))
    print(res,type(res))
    e = {}
    e['cus_id'] = res[0]['cus_id']
    for i in amount:
        e['rate_date'] = i['day']
        e['amount'] = i['total']
        gensql('insert','customer_rate_detail',e)
    '''    
    return(json.dumps([{"Return":"Record Inserted Succcessfully","Returncode":"RIS","Status":"Success","Statuscode":200,"confirmation_number":confir}],indent=2))

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
        
        today_date = datetime.datetime.utcnow().date()
        if arr_date < today_date:
            arr_date = arr_date+datetime.timedelta(days=365)
        if dep_date < today_date:
            dep_date = dep_date+datetime.timedelta(days=365)
            
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
    d = {}
    conf = request.json['confirmation_number']
    d['customer_confirmation_number'] = request.json['confirmation_number']
    #conf = d.get('confirmation_number')
    #d['customer_confirmation_number'] = conf
   

    res = (gensql('select','ivr_room_customer_booked','*',d))
    print(res)
    #NO_OF_room = res[0]['customer_no_of_rooms']
    if len(res) == 2 :
        return(json.dumps([{"Return":"Invalid Confirmation Number","Return_Code":"ICN","Status": "Success",
                      "Status_Code": "200"}],indent=2))  
    result  = json.loads(res)
    data = result[0]
    date = data['customer_arrival_date']
    date1 = data['customer_depature_date']
    arrival_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    depature_date = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    str_date = "'"+str(arrival_date)+"'"
    while arrival_date < depature_date:
          arrival_date = arrival_date+datetime.timedelta(days=1)
          str_date += ","+"'"+str(arrival_date)+"'"
    #print(str_date)    
    room_type = data['customer_room_type']
    #print(room_type)
    no_of_room = data['customer_no_of_rooms']
    b_id = data['id']
    #print(no_of_room,b_id)
    
    today_date = datetime.datetime.utcnow().date()
    if arrival_date < today_date:
       return(json.dumps([{"Return":"Can't Cancel Reservation","Return_Code":"CCR","Status": "Success",
                      "Status_Code": "200"}],indent=2))
    s = {}
    s['customer_booked_status'] = "canceled"    
    print(gensql('update','ivr_room_customer_booked',s,d))
    bu_id = json.loads(dbget("select business_id,customer_no_of_rooms,customer_arrival_date,customer_room_type,customer_depature_date from ivr_room_customer_booked where customer_confirmation_number = '"+str(conf)+"' "))
    #print(bu_id[0]['business_id'])
    arr = str(bu_id[0]['customer_arrival_date'])
    end = str(bu_id[0]['customer_depature_date'])
    print(bu_id[0]['customer_arrival_date'])
    rm_name = bu_id[0]['customer_room_type']
    print(arr,type(arr),rm_name)
    psql = json.loads(dbget("select room_id from configration where room_name = '"+str(rm_name)+"'"))
    print(psql)
    print(dbput("update room_to_sell set available_count=available_count+'"+str(bu_id[0]['customer_no_of_rooms'])+"', booked_count=booked_count-1 where\
          business_id='"+str(bu_id[0]['business_id'])+"' and room_id='"+str(psql[0]['room_id'])+"' and room_date between '"+str(arr)+"' and '"+str(end)+"' "))
    
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
        
        
def twiliofetchroomsavailabilityandprice(request):
    #try:
        d = request.json
        print(d)
        tfn = request.json['TFN']
        adult = d['adult']
        child = d['child']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id)#,b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))

        #d['customer_arrival_date'] = datetime.date(2019, 1, 1)
        #d['customer_depature_date'] = datetime.date(2019, 1, 3)
        customer_arrival_date = d['arrival_date']
        customer_depature_date = d['depature_date']
        '''
        #print(customer_arrival_date,customer_depature_date)
        today_date = datetime.datetime.utcnow().date()
        year = str(today_date.year)
        if int(customer_arrival_date[0:2]) == today_date.month :
            if int(customer_arrival_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_arrival_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_arrival_date = year+'-'+customer_arrival_date[0:2]+'-'+customer_arrival_date[2:]
        d['customer_arrival_date'] = customer_arrival_date
        if int(customer_depature_date[0:2]) == today_date.month :
            if int(customer_depature_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))    
        elif int(customer_depature_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_depature_date = year+'-'+customer_depature_date[0:2]+'-'+customer_depature_date[2:]
        d['customer_depature_date'] = customer_depature_date
        print(customer_arrival_date,customer_depature_date)
        #print(d)  ,room_rate        
        print("date",d['customer_arrival_date'],d['customer_depature_date'])
        '''
        customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
        customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
        customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
        customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

        today_date = datetime.datetime.utcnow().date()
        if customer_arrival_date < today_date:
            #year = customer_arrival_date.year
            #print("year",year,type(year))
            customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
        if customer_depature_date < today_date:
            customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
        print("arr",customer_arrival_date)
        print("dep",customer_depature_date)
        
        nights = customer_depature_date.day - customer_arrival_date.day
        
        print("nights",customer_arrival_date,type(customer_arrival_date))

        depature_date1 = customer_depature_date-datetime.timedelta(days=1)

        print("depature_date1",depature_date1)

        
        room_to_sell = json.loads(dbget("select * from room_to_sell where room_date between '"+str(customer_arrival_date)+"'\
                                         and '"+str(depature_date1)+"' and business_id='"+bi_id[0]['business_id']+"' "))
        
        print("room_to_sell",room_to_sell,type(room_to_sell))
        
        count_o, count_l = [],[]
        
        for i in room_to_sell:
              if i['available_count'] == 0 or i['available_count'] == None:
                      count_o.append(i['room_id'])           
              else:
                 if i['room_id'] not in count_l:
                    count_l.append(i['room_id'])
        #print(count_o, count_l)

        for i in  count_o:
            count_l = [x for x in count_l if x != i]

        count_ll = list(map(str, count_l))        
        #print("idssss   ",count_l,count_ll)    

        rates = json.loads(dbget("select extranet_availableroom.room_id, configration.room_name, room_date,\
                                  room_rate,extranet_availableroom.extra_adult_rate,\
                                  room_open, extranet_availableroom.rate_plan_id from extranet_availableroom \
                                  join configration on extranet_availableroom.room_id = configration.room_id where\
                                  room_date between \
                                  '"+str(customer_arrival_date)+"' and '"+str(depature_date1)+"' and \
                                  extranet_availableroom.business_id = '"+bi_id[0]['business_id']+"' and \
                                  extranet_availableroom.room_id in (%s) order by room_id asc, room_date asc" % ",".join(map(str,count_ll))))
        print(rates)

        beds = json.loads(dbget("select configration.room_id,configration.room_name, bedding_options.total_bed , max_extra_bed.extrabed from configration join \
                                 bedding_options on configration.bedding_options_id = bedding_options.bedding_option_id\
                                 join max_extra_bed on configration.maximum_extrabed_id = max_extra_bed.extrabed_id \
                                 where  business_id='"+bi_id[0]['business_id']+"' and \
                                 configration.room_id in (%s)" % ",".join(map(str,count_ll))))
        #print("beds",beds)
        #print("adult",adult)
        plans, total =[],[]
        list1 =[]
        
        for room_id in count_l:
            list1 = []
            #plan_ids = []
            plans = []
            for rate in rates:
                if rate['room_id'] == room_id:                       
                       #print(rate,rates.index(rate))
                       r = {}
                       r['room_id'] = rate['room_id']
                       r['roo_name'] = rate['room_name']
                       r['rate_plan_id'] = rate['rate_plan_id']
                       r['room_date'] = rate['room_date']
                       r['room_rate'] = rate['room_rate']
                       r['extra_adult_rate'] = rate['extra_adult_rate']
                       plans.append(r)
            #print("plans",plans)
            plan_ids = []
            for plan in plans:
                
                if plan['room_date'] in plan_ids:
                   #print(len(list1),"len list....if")     
                   list1[len(list1)-1].append(plan)
                   
                else:
                   plan_ids.append(plan['room_date'])
                   list1.append([])
                   #print(len(list1),"len list....else")
                   list1[len(list1)-1].append(plan)
                
                
            #print("plans, list1",plan_ids, list1)

            r1 = {}
            r1['room_id'] = room_id
            r1['rate_plans'] = list1
            total.append(r1)
        add_amount,final = [], []
        amount = {}
        count = 0
        for bed in beds:    
            for tol in total:
                    
                if tol['room_id'] == bed['room_id']:    
                   #print(tol,"1111111111111111111111111111111")
                   total_bed = bed['total_bed']
                   extrabed = bed['extrabed']
                   rate_plan = tol['rate_plans']
                   for plan in rate_plan:
                        room_rate, extra_adult_rate =[],[] 
                        for p in plan:
                            room_rate.append(p['room_rate'])
                            extra_adult_rate.append(p['extra_adult_rate'])
                        r1 = min(room_rate)+min(extra_adult_rate)
                        #print(r1)
                        add_amount.append(r1)
                   amount['amount'+""+str(count)+""] = sum(add_amount)     
                   amount['room_id'+""+str(count)+""] = bed['room_id']
                   amount['room_name'+""+str(count)+""] = bed['room_name']
                   count += 1
            final.append(amount)
    
        #print(total)
        #print(add_amount)
        amount['count'] = count
        #print("final",final,amount)
        return(json.dumps([{"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                              "Status_Code": "200","total":amount}],indent=2))  
    
def twiliocalculatetotalcharges(request):
   #try:
        tfn = request.json['tfn_num']
        dividen_list = []
        last_list = []
        sumval = 0
        datelist_rate = []
        datelist_amount = {}
        rate_plan_list = []
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        customer_arrival_date = request.json["arrival_date"]
        customer_depature_date = request.json["depature_date"]
        customer_room_type = request.json["room_type"] # ROOM_ID
        
        print(customer_room_type,type(customer_room_type))

        roos_type_id = json.loads(dbget("select room_id from configration where room_name = '"+str(customer_room_type)+"'"))
       # customer_room_type = customer_room_type.title()
       # print("roomtype",customer_room_type)
        customer_adult = request.json["adult"]
        customer_child = request.json["child"]
        print("adults",customer_adult,type(customer_adult))
        d,e,d1,d2 = {},[],{},{}
        
        customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
        customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
        customer_arrival_date = datetime.datetime.strptime(customer_arrival_date,'%Y-%m-%d').date()
        customer_depature_date = datetime.datetime.strptime(customer_depature_date,'%Y-%m-%d').date()

        today_date = datetime.datetime.utcnow().date()
        if customer_arrival_date < today_date:
            customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
        if customer_depature_date < today_date:
            customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
        print("arr",customer_arrival_date)
        print("dep",customer_depature_date)
        '''
        print(customer_arrival_date,customer_depature_date)
        today_date = datetime.datetime.utcnow().date()
        year = str(today_date.year)
        if int(customer_arrival_date[0:2]) == today_date.month :
            if int(customer_arrival_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_arrival_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_arrival_date = year+'-'+customer_arrival_date[0:2]+'-'+customer_arrival_date[2:]
        
        if int(customer_depature_date[0:2]) == today_date.month :
            if int(customer_depature_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_depature_date[0:2]) < today_date.month :
            year = str(today_date.year+1)

        customer_depature_date = year+'-'+customer_depature_date[0:2]+'-'+customer_depature_date[2:]
        '''
        #print("arrival",customer_arrival_date,"depature",customer_depature_date,"roomid",customer_room_type,"businessid",bi_id[0]['business_id'])    # CONFIGRATION
        sql = json.loads(dbget("select max_extra_bed.extrabed,extranet_availableroom.extra_adult_rate,extranet_availableroom.rate_plan_id,extranet_availableroom.room_date,extranet_availableroom.room_rate,configration.max_adults \
                                    from configration \
                                   join extranet_availableroom on extranet_availableroom.room_id = configration.room_id \
                                   join max_extra_bed on max_extra_bed.extrabed_id = configration.maximum_extrabed_id \
                                   where configration.room_id  = '"+str(roos_type_id[0]['room_id'])+"' and configration.business_id='"+bi_id[0]['business_id']+"'and extranet_availableroom.room_date between '"+str(customer_arrival_date)+"' and '"+str(customer_depature_date)+"'"))
        print("sql",sql)
     
        #available_rate = json.loads(dbget("select room_id,room_rate,room_date,rate_plan_id from extranet_availableroom where room_date between '"+str(customer_arrival_date)+"' and '"+str(customer_depature_date)+"' and room_id='"+str(customer_room_type)+"'"))
        #print(available_rate)
        s = 0
        total_adult = int(customer_adult)
        max_adult = int(sql[0]['max_adults'])
        extra_bed = int(sql[0]['extrabed'])
        extra_adult_rate = sql[0]['extra_adult_rate']
        rooms_rate =  int(sql[0]['room_rate'])
        
        plan_rate = int(sql[0]['rate_plan_id'])

        #print("plan_rate",plan_rate)
        total_beds = max_adult + extra_bed
        total_rooms = total_adult / total_beds
        total_rooms_count = math.ceil(total_rooms)
        print("no of rooms",total_rooms_count)
        
    
        sumva = 0
        for i in sql:
                arrival_date = customer_arrival_date
                depature_date = customer_depature_date
                conf_date = datetime.datetime.strptime(i['room_date'], '%Y-%m-%d')
                print("conf_date",conf_date)
                deltadates = depature_date - arrival_date
                for x in range(deltadates.days + 1):
                   
                   datebetween = arrival_date + datetime.timedelta(x)
                   if datebetween == conf_date or plan_rate == int(i['rate_plan_id']) :
                      
                      print("hiiiiiiiiiiii",i["extra_adult_rate"],i['room_rate'],i['room_rate'])
                      r1 = max_adult * total_rooms_count
                      extra_price = (int(customer_adult) - r1) * int(i["extra_adult_rate"])
                      price = total_rooms_count * int(i['room_rate'])
                      total = price + extra_price                        
                      sumva += total
                      datelist_rate.append({"day":datebetween.strftime('%Y-%m-%d'),"total":total})
                      
        print("datelist_rate",datelist_rate)
        print("sumva",sumva)
       
        
        
        def myconverter(o):
                    if isinstance(o, datetime.datetime):
                         return o.__str__()  
 
        return(json.dumps([{"ServiceMessage":"Success","Total_Amount":sumva,"date_amount":datelist_rate,
                            "no_of_rooms":total_rooms_count}],indent=2,default=myconverter))
        
        #return(json.dumps({"ServiceMessage":"Success","Total_Amount":total_amout,"date_month_amount":last_list},indent=2))
        
    #except:
       # return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))
        
def CheckRoomtype(request):
    d = request.json
    print(d)
    tfn = d['TFN']

    customer_arrival_date = d['customer_arrival_date']
    customer_depature_date = d['customer_depature_date']
    #d = {k:v for k,v in d.items() if k not in ('TFN')}
    b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
    print(b_id)#,b_id[0]['id'])
    bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
    print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))

    customer_room_type = d['customer_room_type']
    
    sql = json.loads(dbget("select count(*) from configration where room_name = '"+str(customer_room_type)+"'"))
    print(sql,sql[0]['count'],type(sql[0]['count']))

    if sql[0]['count'] == 0:
        
        return(json.dumps([{'Retuen':'Success','Returncode':'InValid'}]))
    
    room_type_id = json.loads(dbget("select room_id from configration where room_name = '"+str(customer_room_type)+"'"))

    print(room_type_id[0]['room_id'],type(room_type_id[0]['room_id']))

    customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
    customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
    customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
    customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

    today_date = datetime.datetime.utcnow().date()
    if customer_arrival_date < today_date:
        customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
    if customer_depature_date < today_date:
        customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
    print("arr",customer_arrival_date)
    print("dep",customer_depature_date)
    
    nights = customer_depature_date.day - customer_arrival_date.day
        
    print("nights",nights,type(nights))

    depature_date1 = customer_depature_date-datetime.timedelta(days=1)

    print("depature_date1",depature_date1)

        
    count = json.loads(dbget("select count(*) from room_to_sell where room_id='"+str(room_type_id[0]['room_id'])+"' and \
                              room_date between '"+str(customer_arrival_date)+"' \
                              and '"+str(depature_date1)+"' and business_id='"+bi_id[0]['business_id']+"' "))

    print("count",count[0]['count'],type(count[0]['count']))


    if int(count[0]['count']) == int(nights):
        return(json.dumps([{'Retuen':'Success','Returncode':'Valid'}]))
    else:
        return(json.dumps([{'Retuen':'Success','Returncode':'InValid'}]))
    
