from sqlwrapper import dbget,dbput,gensql
import json


def config(request):
    
    res = request.json
    print(res)
    gensql('insert','configration',res)
    return(json.dumps({"Return":"Record Inserted Successfully","ReturnCode":"RIS","ReturnMessage":"Success"},indent=2))

def select_config(request):
    
    res = json.loads(dbget("select room_id, room_name, max_adults, max_child, room_size.*, bedding_options.* ,max_extra_bed.*,\
                            bed_size.*, upload_photos, room_amenitie.*, smoking, rate_plan_id, advance_booking_window,\
                            prepayment_policy, cancellation_policy, inclusions.*, important_information \
                            from configration \
                            join room_size on configration.room_size_id = room_size.room_size_id\
                            join bedding_options on configration.bedding_options_id = bedding_options.bedding_option_id\
                            join max_extra_bed on configration.maximum_extrabed_id = max_extra_bed.extrabed_id\
                            join bed_size on configration.bed_size_id = bed_size.bed_size_id\
                            join inclusions on configration.inculsions_id = inclusions.inclusion_id\
                            join room_amenitie on configration.room_amenities_id = room_amenitie.amenitie_id"))
    return(json.dumps({"Result":res,"ReturnCode":"RRS","ReturnMessage":"Success"},indent=2))

def update_config(request):
    res = request.json
    a = { k : v for k,v in res.items()  if k not in ('room_id')}
    e = { k : v for k,v in res.items()  if k  in ('room_id')}
    gensql('update','configration',a,e)
    return(json.dumps({"ReturnCode":"RUS","ReturnMessage":"Success"},indent=2))
