from sqlwrapper import gensql,dbget,dbput
import json
#import re
from flask import Flask,request,jsonify
def updategupshupreservation(request):
    #try:
        d=request.json
        #customer_email = json.loads(dbget("select count(*) customer_email from ivr_room_customer_booked where customer_email ='"+str(d['customer_email'])+"'"))
        dbput("update  ivr_room_customer_booked set id_proof='"+str(d['id_proof'])+"' where customer_mobile='"+str(d['customer_mobile'])+"'")
        print("mohan")
        return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success"},indent=4))
        
    #except:
        #return(json.dumps({"Message":"Recored Updated UnSuccessfully","Message_Code":"RUUS","Service":"Failure"},indent=4))
