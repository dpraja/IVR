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

    
    channel_count = json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"'"))
    print(channel_count)

    channel_bookingcount = json.loads(dbget("select count(confirmation_number) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"'"))
    print(channel_bookingcount)
    
    json_input = [
                   {"title":"Bookingcount","value":ivreservationcount[0]['count'] + channel_count[0]['count'] },
                   
                   {"title":"Confirmationcount","value":sql_value[0]['count'] + channel_bookingcount[0]['count']}
                   ]
  
   # json_input = {
      #          "title":["reservationcount","cancelcount","Totalbookingcount"],
       #         "value":[reservationcount[0]['count'] + ivreservationcount[0]['count'],cancelcount[0]['count'],Totalreservationcount[0]['count'] + totalivrcount[0]['count']]
                
       #         }
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
def Getsmscount(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    ivreservationcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked')"))
    print(ivreservationcount)

    
    channel_count = json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"'"))
    print(channel_count)
    ivrsmscount = json.loads(dbget("select count(*) from ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and send_sms in ('success')"))
    print(ivrsmscount)
    channelsmscount = json.loads(dbget("select count(*) from ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and sms in ('success')"))
    json_input = [
                   {"title":"Bookingcount","value":ivreservationcount[0]['count'] + channel_count[0]['count'] },
                   
                   {"title":"smscount","value":ivrsmscount[0]['count'] + channelsmscount[0]['count']}
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))

def GetLanguagecount(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    arabic_count = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and ivr_language in ('1')"))
    print(arabic_count)
    ivr_englishcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and ivr_language in ('2')"))
    print(ivr_englishcount)
    
    english_count = json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"'"))
    print(english_count)
    json_input = [
                   {"title":"Arabic","value":arabic_count[0]['count']  },
                   
                   {"title":"English","value":english_count[0]['count'] +  ivr_englishcount[0]['count'] }
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
def GetRoomOccupancy(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']

    IVR_Standard_room = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_room_type in ('Standard Room')"))
    print(IVR_Standard_room)
    
    IVR_deluxroom = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_room_type in ('Delux Room')"))
    print(IVR_deluxroom)

    IVR_superiorroom = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_room_type in ('Superior Room')"))
    print(IVR_superiorroom)

    IVR_deluxesuite = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_room_type in ('Deluxe Suite')"))
    print(IVR_deluxesuite) 

    channel_standard = json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and roomtype in ('Standard')"))
    print(channel_standard)
    channel_delux= json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and roomtype in ('Delux')"))
    print(channel_delux)
    channel_superior= json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and roomtype in ('Superior')"))
    print(channel_superior)
    channel_deluxe= json.loads(dbget("select count(*) from public.ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and roomtype in ('Deluxe')"))
    print(channel_deluxe)
    json_input = [
                   {"title":"StandardRoom","value":IVR_Standard_room[0]['count'] +channel_standard[0]['count'] },
                   {"title":"DeluxRoom","value":IVR_deluxroom[0]['count'] + channel_delux[0]['count'] },
                   {"title":"SuperiorRoom","value":IVR_superiorroom[0]['count'] + channel_superior[0]['count'] },
                   {"title":"DeluxSuite","value":IVR_deluxesuite[0]['count'] + channel_deluxe[0]['count']}
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
def GetYearbyyeareservationcount(request):
    yearlist = []
    dividendlist,dividendlist_add,fin_list  = [],[],[]
    count_of_year = {}
    Year1 = json.loads(dbget("select customer_arrival_date from public.ivr_room_customer_booked  order by customer_arrival_date"))
    Year2 = json.loads(dbget("select arrival_date as customer_arrival_date from public.ivr_resevation  order by arrival_date"))
    Year1 = Year1 + Year2
    for dividend_dict in Year1:
     for key, value in dividend_dict.items():
        #yearlist.append(key)
        dividendlist.append(value)
    
    year_count = 0
    for i in dividendlist:
        year_count = year_count+1
        j = datetime.datetime.strptime(i,'%Y-%m-%d').date()
        year_j = j.year
        sample = "'{}'".format(year_j)
        if sample in dividendlist_add:
            pass
        else: 
           dividendlist_add.append(sample)
           year_count = 1
        count_of_year[""+str(year_j)+""] = year_count

        
    print(count_of_year)
    #for key,value in count_of_year.items():
    for k,v in count_of_year.items():
        fin_list.append({'title':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)   
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":fin_list},indent=2))



def GetCountryreservation(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    
    dividendlist,a,a_add,total_count,fin_list,cn_reservation  = [],[],[],{},[],[]

    ivr_country_count = json.loads(dbget("SELECT ivr_room_customer_booked.cntry_code, country_list.country \
                                         from ivr_room_customer_booked \
                                         left join country_list on country_list.country_code = ivr_room_customer_booked.cntry_code where ivr_room_customer_booked.customer_arrival_date between '"+date_from+"' and '"+date_to+"'" ))
    
    channel_country_count = json.loads(dbget("SELECT ivr_resevation.countrycode as cntry_code, country_list.country \
                                         from ivr_resevation \
                                         left join country_list on country_list.country_code = ivr_resevation.countrycode where ivr_resevation.arrival_date between '"+date_from+"' and '"+date_to+"'"))
    
    #print("ivr",ivr_country_count)
    #print("channel",channel_country_count)
    ivr_country_count = ivr_country_count+channel_country_count
    #print("final_ivr",ivr_country_count)
    
    for res in ivr_country_count:
        for k,v in res.items():
            if k == 'country':
                a.append(v)            
    print(a)
    country_count=0
    for i in a:
        country_count = country_count+1
        if i in a_add:
            pass
        else:
            a_add.append(i)
            country_count = 1
        total_count[""+str(i)+""] = country_count
    print(total_count)
    for k,v in total_count.items():
        fin_list.append({'title':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)    
    
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":fin_list},indent=2))

