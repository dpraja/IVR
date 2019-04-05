import requests
from sqlwrapper import gensql,dbget,dbput
import json
import datetime
import time
from flask import Flask,request,jsonify
#app = Flask(__name__)
#@app.route('/reminder',methods=['GET'])

def reminder():
    print('wait')
    date = (datetime.datetime.now()).strftime("%Y-%m-%d")
    sql = json.loads(dbget("select customer_mobile from public.ivr_room_customer_booked where customer_arrival_date = '"+str(date)+"'"))

    if len(sql) != 0:
        for sqls in sql:
           
            
            mobile = '91'+str(sqls['customer_mobile'])
            print(mobile,type(mobile))
            message = 'Today is your arrival date of QulaityInn'
            headers = {
                'accept': '*/*',
                'apikey': '94b7389d4e074935c974eef4dd08ad6c',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
            }

            data = {
              'routing-rule': 'whatsapp',
              'src.phone': '919899066047',
              'dest.phone': mobile,
              'message.payload': message,
              'bypass': 'false'
            }

            response = requests.post('https://api.gupshup.io/sm/api/v1/msg', headers=headers, data=data)

            print('sucess')
        return 'sucess'
    else:
        print('no recored')


#if __name__ == "__main__":
    #app.run(host="192.168.1.3",port=5000)



