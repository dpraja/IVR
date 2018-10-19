import json
import datetime
from sqlwrapper import gensql,dbfetch,dbget

def ratesandavailability(request):
    
    req = request.json
    #print(req)
    a = {k:v for k,v in req.items() if v == '' }
    #print(len(a))
    if len(a) != 0:
       from_date = datetime.datetime.now().date()
       to_date = from_date +datetime.timedelta(days=15)
    else:
       from_date = datetime.datetime.strptime(req['from_date'],'%Y-%m-%d').date()
       to_date = datetime.datetime.strptime(req['to_date'],'%Y-%m-%d').date()
       
    res = json.loads(dbget("SELECT extranet_availableroom.business_id,configration.room_id, configration.room_name ,room_date, \
                            room_rate, room_open, s_no,   rate_plan.rate_plan_id,rate_plan.rate_plan, \
                            min_stay, max_stay, close_arrival, close_departure, house_close \
	                    FROM public.extranet_availableroom join configration on extranet_availableroom.room_id = configration.room_id\
	                    join rate_plan on extranet_availableroom.rate_plan_id = rate_plan.rate_plan_id \
                            where configration.business_id='"+req['business_id']+"' and room_date \
	                    between '"+str(from_date)+"' and '"+str(to_date)+"'"))
    
    #print(res,type(res))
    
    room_name,colle_rooms,rate_plan = [],[],[]
    count_type, count_plan = 0,0
    
    for i in res:
      #print(type(i))  
      l={k:v for k,v in i.items() if k in('business_id','room_id','room_name','room_date','rate_plan','rate_plan_id','room_open','min_stay','max_stay','room_rate','extra_adult_rate','booked_count',
                                          'close_arrival','close_departure','house_close') }
      #print('lll',l)
      if i['room_name'] in  room_name :
          pass
      else:
          rate_plan = []
          count_plan = 0
          count_type = count_type+1
          room_name.append(i['room_name'])
      #print("room_name",room_name)    
      if i['rate_plan'] in rate_plan:
         pass
      else:
          count_plan = count_plan+1
          rate_plan.append(i['rate_plan'])
          
      k={}
      k['room_plan'+str(count_plan)] = l
      
      j={}
      j['room_type'+str(count_type)] = k
      colle_rooms.append(j)         
      
      #print(i)
    #print(room_name)
    #print(colle_rooms)

    sell = json.loads(dbget("select room_to_sell.*, configration.room_name as con_room_name from room_to_sell \
                             join configration on room_to_sell.room_id = configration.room_id where room_date between  \
                             '"+str(from_date)+"' and '"+str(to_date)+"' and  room_to_sell.business_id='"+req['business_id']+"' "))
    #print("sell",sell)
        
    r_key,p_key = [],[]
    total,room_total,plan_total,plan_total01 = [],[],[],[]
    room_to_sell = []
    for i in colle_rooms:
        #print(i)
        room_k = [k for k,v in i.items()]
        rooms = i[""+room_k[0]+""]
        #print("rooms  ",rooms)
        
        plan_k = [k for k,v in rooms.items()]
        plans = rooms[""+plan_k[0]+""]
        #print("plans  ",plans)
        
        if room_k[0] not in r_key:           
           r_key.append(room_k[0])
           plan_total = []
           #plan_total[]
           '''
           plan_k = [k for k,v in rooms.items()]
           plans = rooms[""+plan_k[0]+""]
           print("plans  ",plans)
           '''
           total.append({""+room_k[0]+"":{'room_name': plans['room_name'],'room_to_sell':room_to_sell,'plans':plan_total}})
        else:
           pass
        for j in sell:
            if plans['room_name'] == j['con_room_name']  and plans['room_date'] == j['room_date']:
               j1 ={k:v for k,v in j.items() if k in ('room_id','room_date','available_count','booked_count') }
               room_to_sell.append(j1)
        plan_total.append(rooms)
        
        '''
        plan_k = [k for k,v in rooms.items()]
        plans = rooms[""+plan_k[0]+""]
        print("plans  ",plans)        
    
        if plan_k[0] not in p_key:
             p_key.append(plan_k[0])
        else:
            pass
        '''
    #print(r_key,p_key)
    print(total)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":total},indent=2))   
   

def daterange(request):
    res = request.json
    print(res,type(res))
    a = { k : v for k,v in res.items() if k not in ('st_date','ed_date','days','available_count') }
    print("a",a)
    x = { k : v for k,v in a.items() if k not in ('business_id','room_id','rate_plan_id') }
    y = { k : v for k,v in a.items() if k  in ('business_id','room_id','rate_plan_id') }
    z = { k : v for k,v in a.items() if k  in ('business_id','room_id') }
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
               #a['booked_count'] = 0
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
     
    from_date = request.json['st_date']
    to_date = request.json['ed_date']
    from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d').date()
 
    sell_detail = z
    sell_detail['available_count'] = res['available_count']
    sell_detail['booked_count'] = 0
    u_x = {'available_count':res['available_count']}
    while from_date <= to_date:
            z['room_date'] = from_date
            count = json.loads(gensql('select','room_to_sell','count(*)',z) )
            if count[0]['count'] == 0:
                print("insert a",a)
                sell_detail['room_date'] = from_date
                gensql('insert','room_to_sell',sell_detail)
            else:
               print("update",from_date)
               z['room_date'] = from_date
               gensql('update','room_to_sell',u_x,z)
            from_date+=datetime.timedelta(days=1)   
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":""},indent=2))
    
    


#RatesandAvailability.py
#Displaying RatesandAvailability.py.
