import json
import datetime
import calendar
from sqlwrapper import gensql,dbget,dbput
def insertcancelpolicy(request):
    d = request.json
    print(d)
    e = { k : v for k,v in d.items() if k in ('business_id')}
    f = { k : v for k,v in d.items() if k not in ('business_id')}
    sql = json.loads(dbget("select count(*) from cancel_policy where business_id='"+d['business_id']+"' "))
    print(sql[0]['count'])
    if sql[0]['count'] != 0:
        print(gensql('update','cancel_policy',f,e))
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    print(gensql('insert','cancel_policy',d))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    
def QueryStatistics(request):
    sql = json.loads(dbget("SELECT customer_arrival_date FROM public.ivr_room_customer_booked where \
                            customer_arrival_date < '2018-06-20' \
                            order by customer_arrival_date desc"))
    print(sql)
    today = datetime.datetime.utcnow().date()
    print(today,today.month)
    a,b,c = 0,0,0
    d={} 
    for i in sql:
        #print(i['customer_arrival_date'],type(i['customer_arrival_date']))
        i = datetime.datetime.strptime(i['customer_arrival_date'], "%Y-%m-%d").date()
        
        #print(i,type(i))
        if i.month == today.month:
            a += 1
            #print (calendar.month_name[today.month])    
            #print(calendar.i[today.month], "-", calendar.i[today.month])
        elif i.month == today.month-1:
            b += 1
        elif i.month == today.month-2:
            c += 1
    d[""+calendar.month_name[today.month]+""+"-"+""+str(i.year)+""] = a
    d[""+calendar.month_name[today.month-1]+""+"-"+""+str(i.year)+""] = b
    d[""+calendar.month_name[today.month-2]+""+"-"+""+str(i.year)+""] = c
    
    print(a,b,c,d)        
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":d},indent=2))
