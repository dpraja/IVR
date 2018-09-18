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
