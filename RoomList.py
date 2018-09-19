import json
from sqlwrapper import gensql,dbfetch,dbget

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
    res = request.json
    a = { k : v for k,v in res.items() if v != '' if k  not in ('business_id','room_type')}
    e = { k : v for k,v in res.items() if v != '' if k   in ('business_id','room_type')}
    gensql('update','extranet_room_list',a,e)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
