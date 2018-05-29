from sqlwrapper import dbget,gensql,dbput
import json
import datetime
def fetchroomsavailabilityandprice(request):
    try:
        d = request.json
        print(d)
        tfn = request.json['TFN']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        customer_arrival_date = d['arival_date']
        customer_depature_date = d['depature_date']
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
        d['customer_arrival_date'] = customer_arrival_date
        if int(customer_depature_date[0:2]) == today_date.month :
            if int(customer_depature_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_depature_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_depature_date = year+'-'+customer_depature_date[0:2]+'-'+customer_depature_date[2:]
        d['customer_depature_date'] = customer_depature_date
        #print(customer_arrival_date,customer_depature_date)
        #print(d)  ,room_rate 
        res = json.loads(dbget("select available_count,room_type from extranet_availableroom join \
                               extranet_room_list on extranet_room_list.id = extranet_availableroom.id \
                               where room_date between '"+d['customer_arrival_date']+"' and \
                               '"+d['customer_depature_date']+"' \
                               and business_id='"+bi_id[0]['business_id']+"' "))
        #print(res,type(res))
        list1,list2 = [],[]
        for i in res:
            if i['available_count'] == 0:
                 list2.append(list(i.values())[1:])
            if list(i.values())[1:] not in list1:  
                 list1.append(list(i.values())[1:])
        print(list1)
        print(list2)
        for i in list2:
            if i in list1:
                list1.remove(i)
        print(list1)
        dict1 = {"count":len(list1)}
        rate_str = ''
        for i in list1:
            #print(i,type(i))
            dict1["room_type"+""+str(list1.index(i))+""] = i[0]
            if len(rate_str) !=0:
               rate_str +=','+ "'"+i[0]+"'"
            else:
               rate_str += "'"+i[0]+"'"
        print(dict1)       
        print(rate_str)
        st_rate = json.loads(dbget("select standard_rate from extranet_room_list where \
                                    room_type in ("+rate_str+") and business_id='"+bi_id[0]['business_id']+"' "))
        #print(st_rate,type(st_rate))
        for data in st_rate:
            #print(data,type(data))
            dict1["room_rate"+""+str(st_rate.index(data))+""] = data['standard_rate']
        print(dict1)
        dict1['ServiceStatus'] = "Success"
        dict1['ServiceMessage'] = "Success"
        return(json.dumps(dict1))
        #return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure","count":"0"},indent=2))
    
def fetchpromotionalmessage(request):
    try: 
        today_date = datetime.datetime.utcnow().date()
        tfn = request.json['TFN']
        
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        id1 = json.loads(dbget("select id from ivr_hotel_list where business_id='"+bi_id[0]['business_id']+"' "))
        #print(id1[0]['id'])
        date = json.loads(dbget("select message_date_start,message_date_end from \
                                ivr_promotional_message where id="+str(id1[0]['id'])+" "))
        print(date)
        st_d = date[0]['message_date_start']
        ed_d = date[0]['message_date_end']
        st_d = datetime.datetime.strptime(st_d,'%Y-%m-%d').date()
        ed_d = datetime.datetime.strptime(ed_d,'%Y-%m-%d').date()
        print(st_d,ed_d,type(st_d))
        #today_date = '2018-05-01'
        #today_date = datetime.datetime.strptime(today_date,'%Y-%m-%d').date()
        print("today",today_date)
        if today_date <= ed_d  and today_date >= st_d:       
            result = json.loads(dbget("select message from ivr_promotional_message where id="+str(id1[0]['id'])+" "))
            #print(result)
            result = result[0]
            #return(json.dumps({"Return":"Record Retrieved Successfully","Return Code":"RRS", "Status": "Success",
             #                 "Status Code": "200", "Return Value":result},indent=2))
            dict1 = {"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                              "Status_Code": "200"}
            print(dict1,type(dict1))
            dict1.update(result)
            print(dict1)
            return(json.dumps(dict1))
        else:
            return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))
    except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))
def insertpromotionalmessage(request):
    #e = request.json
    bus_id = request.json['business_id']
    message = request.json['message']
    st = request.json['message_date_start']
    ed = request.json['message_date_end']
    b_id = json.loads(dbget("select id from ivr_hotel_list where business_id='"+bus_id+"' "))
    print(b_id[0]['id'])
    count = json.loads(dbget("select count(*) from ivr_promotional_message where \
                              id='"+str(b_id[0]['id'])+"' "))
    print(count)
    e = {}
    e['message'] = message
    #print(type(message))
    e['id'] = b_id[0]['id']
    e['message_date_start']= st
    e['message_date_end'] = ed
    if count[0]['count'] != 1:
        print(gensql('insert','ivr_promotional_message',e))
    else:
            print(dbput("update ivr_promotional_message set message = '"+str(message)+"' , message_date_start = '"+st+"', message_date_end='"+ed+"' where id='"+str(b_id[0]['id'])+"' "))
    a = {"ServiceStatus":"Success","ServiceMessage":"Success"}
    return(json.dumps(a))
     
