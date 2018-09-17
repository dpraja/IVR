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
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success",
                      "Status_Code": "200","chatbotcount":channelchatbot[0]['count'],
                       "ivrchannelcount":channelivr[0]['count'] },indent=2))
    
    
