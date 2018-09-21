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
    d = json.loads(dbget("select customer_mobile, customer_arrival_date, customer_depature_date,\
                          customer_room_type, customer_room_rate,\
                          customer_pickup_drop,customer_booked_date,customer_cc,customer_expirydate,\
                          customer_amount,customer_booked_status,\
                          customer_booked_status,customer_adult,customer_child,customer_no_of_rooms,\
                          channel from ivr_room_customer_booked"))
    print(d)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","result":d},indent=2))
