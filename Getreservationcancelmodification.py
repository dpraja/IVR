from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request, jsonify
def Getreservationcancelmodification(request):
    
    
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    sql_value = json.loads(dbget("select * from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"'"))
    print(sql_value)
    
    reservationcount = json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between '"+date_from+"' and '"+date_to+"'"))
    print(reservationcount)

    ivreservationcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked')"))
    print(ivreservationcount)

    cancelcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('canceled')"))
    print(cancelcount)

    #Totalreservationcount = json.loads(dbget("select count(*) from public.ivr_resevation "))
    #print(Totalreservationcount)
    
    Modificationcount = json.loads(dbget("select count(*) from ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and modification in ('yes')"))

    totalivrcount = json.loads(dbget("select count (*) from public.ivr_room_customer_booked"))
    print(totalivrcount)

    json_input = [
                   {"title":"reservationcount","value":reservationcount[0]['count'] + ivreservationcount[0]['count']},
                   {"title":"cancelcount","value":cancelcount[0]['count']},
                   #{"title":"Totalbookingcount","value":Totalreservationcount[0]['count'] + totalivrcount[0]['count']},
                   {"title":"Modificationcount","value":Modificationcount[0]['count']}
                   ]
  
   # json_input = {
      #          "title":["reservationcount","cancelcount","Totalbookingcount"],
       #         "value":[reservationcount[0]['count'] + ivreservationcount[0]['count'],cancelcount[0]['count'],Totalreservationcount[0]['count'] + totalivrcount[0]['count']]
                
       #         }
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
    
def GetBookingConfirmation(request):
    
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    sql_value = json.loads(dbget("SELECT count(customer_confirmation_number) FROM public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"'"))
    print(sql_value)

    ivreservationcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked')"))
    print(ivreservationcount)

    json_input = [
                   {"title":"Bookingcount","value":ivreservationcount[0]['count'] },
                   
                   {"title":"Confirmationcount","value":sql_value[0]['count']}
                   ]
  
   # json_input = {
      #          "title":["reservationcount","cancelcount","Totalbookingcount"],
       #         "value":[reservationcount[0]['count'] + ivreservationcount[0]['count'],cancelcount[0]['count'],Totalreservationcount[0]['count'] + totalivrcount[0]['count']]
                
       #         }
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
    
