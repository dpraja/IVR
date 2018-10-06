import json
import datetime
from sqlwrapper import gensql,dbfetch,dbget

def ratesandavailability(request):
    req = request.json
    for k,v in req.items():
        if k == 'date_range':
           from_date = datetime.datetime.now().date()
           to_date = from_date +datetime.timedelta(days=v)
           
        if k == 'from_date':
           from_date = request.json['from_date']
           to_date = request.json['to_date']
           from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d').date()
           to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d').date()
               
    business_id = request.json['business_id']
    room_type = request.json['room_type']
    #room_name = request.json['room_name']
    date_list = []
    str_date = ''
    while from_date <= to_date:
        if len(str_date) != 0:
           str_date += ','+"'"+str(from_date)+"'"
        else:   
           str_date += "'"+str(from_date)+"'"   
        date_list.append(from_date)
        from_date += datetime.timedelta(days=1)
    print(str_date)    
    day,days,a = [],{},{"business_id":business_id}
    res = json.loads(dbget("select room_date,available_count,room_rate,room_open from extranet_availableroom where room_date in ("+str_date+") and id in (select id from extranet_room_list where business_id='"+business_id+"' and room_type='"+room_type+"')"))
    print(res,type(res),len(res))
    length = len(res)
    date = []
    for data in res:
        print(data['room_date'],type(data['room_date']))
        date.append(datetime.datetime.strptime(data['room_date'],'%Y-%m-%d').date())
    #print(date,type(list))    
    for i in date_list:
        #print(i,type(i))
        if i in date:
              n = date.index(i)
              #print(n)
              d = {"Month": i.strftime('%B'),"Date":i.strftime('%d'),"Day":i.strftime("%A")[0:3],
                "Price":res[n]["room_rate"],
                "Available_Room_Count":res[n]["available_count"],
                "Room_Status":"Declared","date":str(i),"room_open":res[n]['room_open']}
              #print(d)
        else:
             d = {"Month": i.strftime('%B'),"Date":i.strftime('%d'),"Day":i.strftime("%A")[0:3],
                "Price":"",
                "Available_Room_Count":"",
                "Room_Status":"NotDeclared","date":str(i),"room_open":res[n]['room_open']}
             #print(d) 
        day.append(d)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":day},indent=2))

def daterange(request):
    res = request.json
    print(res,type(res))
    a = { k : v for k,v in res.items() if k not in ('st_date','ed_date','days') }
    print("a",a)
    x = { k : v for k,v in a.items() if k not in ('business_id','room_id','rate_plan_id') }
    y = { k : v for k,v in a.items() if k  in ('business_id','room_id','rate_plan_id') }
    print("x",x)
    print("y",y)
    days = res['days']
    #day0 = [ k  for k,v in res.items() if v == 0 ]
    day1 = [ k  for k,v in days.items() if v != 0 ]
    print(a,days,day1)
    from_date = request.json['st_date']
    to_date = request.json['ed_date']
    from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d').date()
    
    while from_date <= to_date:
          print(from_date,from_date.strftime("%A")[0:3].lower())
          if from_date.strftime("%A")[0:3].lower() in day1:
             y1={} 
             y1 = y
             y1['room_date'] = from_date
             count = json.loads(gensql('select','extranet_availableroom','count(*)',y1) )
             print(count,type(count),count[0]['count'])
             if count[0]['count'] == 0:
               print("insert",from_date)  
               a['booked_count'] = 0
               a['room_date'] = from_date
               a['room_open'] = 1
               print("insert a",a)
               gensql('insert','extranet_availableroom',a)
             else:
               print("update",from_date)  
               gensql('update','extranet_availableroom',x,y)
          else:
              pass
          from_date+=datetime.timedelta(days=1)
          
          
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":""},indent=2))
    
    


