import json
from sqlwrapper import gensql,dbfetch,dbget

def availableroomcount(request):
    d = request.json
    print(d)
    print(d['business_id'])
    res = json.loads(dbget("select available_count,booked_count,room_name from extranet_availableroom join configration on configration.room_id = extranet_availableroom.room_id where room_date = '"+d['available_date']+"'"))
    print(res,type(res))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Available_Rooms":res},indent=2))
