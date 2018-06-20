import json
import datetime
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
    
