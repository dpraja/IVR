from sqlwrapper import gensql,dbget
import json
import datetime
from decimal import Decimal

def calculatetotalcharges(request):
    try:
        tfn = request.json['TFN']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        customer_arrival_date = request.json["customer_arrival_date"]
        customer_depature_date = request.json["customer_depature_date"]
        customer_room_type = request.json["customer_room_type"]
        customer_room_type = customer_room_type.title()
        print("roomtype",customer_room_type)
        customer_adult = request.json["customer_adult"]
        customer_child = request.json["customer_child"]
        print("adults",customer_adult,type(customer_adult))
        d,e,d1,d2 = {},[],{},{}
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
        
        print("arrival",customer_arrival_date,"depature",customer_depature_date)    
        result = json.loads(dbget("select * from extranet_room_list where \
                                   room_type in ('"+customer_room_type+"') and business_id='"+bi_id[0]['business_id']+"' "))
        print("res",result)
        res = result[0]
        print("res",res)
        currency = res['standard_rate_currency']
        arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d')
        depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d')
        date_to = depature_date - datetime.timedelta(days=1)
        print(date_to)
        print(arrival_date,depature_date)
        night = (depature_date - arrival_date).days
        if night == 0:
            night = 1
        print("night",night,type(night))
        #Total_amt = night * room_rate
        #print(Total_amt,type(Total_amt))
        result = json.loads(dbget("select room_rate from extranet_availableroom where id in(select id from extranet_room_list where business_id = '"+str(bi_id[0]['business_id'])+"' \
                                   and room_type= '"+customer_room_type+"') and room_date between \
                                   '"+customer_arrival_date+"' and '"+str(date_to)+"' "))
        print("result",result)
        Total_amt = 0
        for rate in result:
             print("rate",rate)
             Total_amt += rate['room_rate']
        print("total",Total_amt)
        no_of_rooms = 1
        customer_adult = int(customer_adult)
        customer_child = int(customer_child)
        total_pers = customer_adult+customer_child
        if total_pers>4:
            no_of_rooms = total_pers/4
            str_count = str(no_of_rooms)
            print("first",no_of_rooms)
            a = str_count.split('.')
            print("aaaa",a[1],type(a[1]))
            if int(a[1]) != 0:  
              no_of_rooms += 1
              no_of_rooms = int(no_of_rooms)
            #Decimal(no_of_rooms)
              print("second",no_of_rooms)
            
        '''
        if customer_adult > 2:
           if customer_adult%2 > 0:
              customer_adult += 1
              no_of_rooms = customer_adult/2
           else:
              no_of_rooms = customer_adult/2
        '''      
        Total_amt = Total_amt * no_of_rooms
        print(Total_amt)
        return(json.dumps({"ServiceMessage":"Success","Total_Amount":Total_amt,"currency":currency,"no_of_rooms":int(no_of_rooms)}))
    except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))
