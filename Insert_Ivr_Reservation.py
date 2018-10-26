from sqlwrapper import dbget,dbput,gensql
import json
import random

def Insert_Ivr_Reservation(request):
    d = request.json
    confirmation = (random.randint(1000,9999))
    d['confirmation_number'] = confirmation
    gensql('insert','ivr_resevation',d)
    confirmation = d.get('confirmation_number')
    a = {"Return":"Record Inserted Successfully","ReturnCode":"RIS","ReturnMessage":"Success","Confirmation_Number":confirmation}
    return(json.dumps(a,indent=2))

def Query_Reservation(request):
    b_id = request.json
    d = json.loads(dbget("SELECT * FROM public.ivr_room_customer_booked where business_id='"+b_id['business_id']+"'"))
    '''
    e = json.loads(dbget("select customer_name, customer_room_rate, customer_booking_confirmed, customer_booked_date, customer_menu_navigation,\
                          customer_cc, customer_expirydate, customer_amount, customer_booked_status, id, customer_no_of_rooms, modification,\
                          ivr_language, phone_number as customer_mobile, arrival_date as customer_arrival_date, depature_date as customer_depature_date,\
                          adult as customer_adult, child as customer_child, roomtype as customer_room_type, pickup as customer_pickup_drop,\
                          channel, confirmation_number as customer_confirmation_number, sms as send_sms, countrycode as cntry_code,\
                          ivr_res_id as cus_id\
                          from public.ivr_resevation where  "))
    '''                          
    
    #print(d)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","result":d},indent=2))

