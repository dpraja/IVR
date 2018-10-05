import json
from sqlwrapper import gensql,dbfetch,dbget,dbput

def roomlist(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select * from extranet_room_list where business_id='"+business_id+"' "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Room_List":res},indent=2))
def insertroomlist(request):
 try: 
    d = request.json
    for i in d:
        print(i)
    print(i)
    no = json.loads(dbget("select count(*) from extranet_room_list"))
    print(no[0]['count'])
    id1 = no[0]['count']+1
    print(id1)
    i['id']= id1
    print(gensql('insert','extranet_room_list',i))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
 except:
     return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2)) 

def restriction(request):
    d = request.json
    #gensql('insert','restriction',d)
    print(d)
    business_id = d['business_id']
    room_id = json.loads(dbget("select room_id from configration where business_id='"+str(business_id)+"' "))
    print(dbput("update extranet_availableroom set min_stay='"+d['min_stay']+"' where room_date='"+d['min_date']+"' \
           and room_id in (""select room_id from configration where business_id='"+str(business_id)+"'" ") "))

    print(dbput("update extranet_availableroom set max_stay='"+d['max_stay']+"' where room_date='"+d['max_date']+"' \
           and room_id in (""select room_id from configration where business_id='"+str(business_id)+"'" ") "))

    print(dbput("update extranet_availableroom set house_close='1' where room_date='"+d['house_close']+"' \
           and room_id in (""select room_id from configration where business_id='"+str(business_id)+"'" ") "))

    print(dbput("update extranet_availableroom set close_arrival='1' where room_date between '"+d['close_arrival_from']+"' and '"+d['close_arrival_to']+"' \
           and room_id in (""select room_id from configration where business_id='"+str(business_id)+"'" ") "))

    print(dbput("update extranet_availableroom set close_departure='1' where room_date between '"+d['close_departure_from']+"' and '"+d['close_departure_to']+"' \
           and room_id in (""select room_id from configration where business_id='"+str(business_id)+"'" ") "))

    print(room_id)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def select_restriction(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select * from restriction where business_id= '"+business_id+"' "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
