import json
from sqlwrapper import gensql,dbfetch,dbget,dbput

def create_rate_plan(request):
    res = request.json
    gensql('insert','rate_plan',res)

    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def update_rate_plan(request):
    res = request.json
    a = { k : v for k,v in res.items() if v != '' if k  not in ('business_id','rate_plan_id')}
    e = { k : v for k,v in res.items() if v != '' if k   in ('business_id')}
    gensql('update','rate_plan',a,e)
    
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def delete_rate_plan(request):
    plan_id = request.json['rate_plan_id']
    dbput("delete from rate_plan where rate_plan_id="+str(plan_id)+" ")
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def select_rate_plan(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select rate_plan.rate_plan_id, rate_plan.rate_plan, cancellation_policy.*, room_id, room_name, packages.*, start_date, end_date, rate_plan.business_id\
                            from rate_plan join cancellation_policy on rate_plan.cancellation_policy_id = cancellation_policy.policy_id \
                            join configration on rate_plan.room_types_id = configration.room_id \
                            join packages on rate_plan.packages_id = packages.packages_id \
                            where rate_plan.business_id="+business_id+" "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
    
def select_room_types(request):
    res = json.loads(dbget("select room_id, room_name from configration"))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
    
def select_cancellation_policy(request):
    res = json.loads(dbget("select * from cancellation_policy"))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
 
def select_packages(request):
    res = json.loads(dbget("select * from packages"))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
 
def select_rateplanid(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select rate_plan_id, rate_plan from public.rate_plan where business_id='"+business_id+"' "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
    
