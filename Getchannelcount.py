from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request, jsonify

def Getchannelcounts(request):
    
    
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']


    channelchatbot = json.loads(dbget("select count(*) from ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and channel in ('CHATBOT')"))
    print(channelchatbot)

    #channelivr = json.loads(dbget("select count(*) from ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and channel in ('IVR')"))
    #print(channelivr)

    ivrcount = json.loads(dbget("select count (*) from ivr_room_customer_booked where customer_arrival_date between  '"+date_from+"' and  '"+date_to+"' and channel in ('IVR')"))
    print(ivrcount)

    
    totalvalue = channelchatbot[0]['count'] + ivrcount[0]['count']
    chatperc = channelchatbot[0]['count'] * 100/totalvalue
    ivrperc = ivrcount[0]['count'] * 100/ totalvalue
    
    json_input = [{"title":"Chatbot","value":channelchatbot[0]['count'],"percentage":chatperc},
                  {"title":"Ivr","value":ivrcount[0]['count'],"percentage":ivrperc}
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success",
                      "Status_Code": "200","Returnvalue":json_input },indent=2))
    
    
    

    
