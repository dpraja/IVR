from sqlwrapper import dbget,dbput,gensql
import json

def Insert_Ivr_Reservation(request):
    d = request.json
    gensql('insert','ivr_resevation',d)
    return(json.dumps({"Return":"Record Inserted Successfully","ReturnCode":"RIS","ReturnMessage":"Success"},indent=2))
