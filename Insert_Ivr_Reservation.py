from sqlwrapper import dbget,dbput,gensql
import json
import random

def Insert_Ivr_Reservation(request):
    d = request.json
    gensql('insert','ivr_resevation',d)
    confirmation = (random.randint(1000,9999))
    a = {"Return":"Record Inserted Successfully","ReturnCode":"RIS","ReturnMessage":"Success","Confirmation_Number":confirmation}
    return(a)
