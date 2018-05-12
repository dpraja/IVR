import requests
import json
import smtplib
from sqlwrapper import gensql
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def sendemailani(name,email,message,conf_no,hotel_name,arrival,depature,room_type):
     print(name,email,message,conf_no,hotel_name,arrival,depature, room_type)
     sender = "infocuit.testing@gmail.com"
     receiver = email
     print(sender,type(sender),receiver,type(receiver))
     #message = request.json['message']
     #data = message.split("|")
     #print(data)
     subject = "Hotel Booking"
     msg = MIMEMultipart()
     msg['from'] = sender
     msg['to'] = receiver
     msg['subject'] = subject
     # Create the body of the message (a plain-text and an HTML version)
     html = """\
     <html>
      <head></head>
      <body>
        <dl>
        <dt>
        <p><font size="2" color="black">hi,"""+name+"""</font></p>
        <p><font size="4" color="blue">"""+message+"""</font></p>
  
        <p><font size="2" color="black">Confirmation Number:"""+ conf_no+"""</font></p>
        <p><font size="2" color="black">Arrival Date:"""+ arrival+"""</font></p>
        <p><font size="2" color="black">Depature Date0:"""+ depature+"""</font></p>
        <p><font size="2" color="black">Room Type:"""+ room_type+"""</font></p>
        <p><font size="4" color="blue">Hotel Name:"""+hotel_name+"""</font></p>
        
        </dl>

      </body>
     </html>
     """
     
     #msg.attach(MIMEText(msg['subject'],'plain'))
     msg.attach(MIMEText(html,'html'))
     
     gmailuser = 'infocuit.testing@gmail.com'
     password = 'infocuit@123'
     server = smtplib.SMTP('smtp.gmail.com',587)
     server.starttls()
     server.login(gmailuser,password)
     text = msg.as_string()
     server.sendmail(sender,receiver,text)
     print ("the message has been sent successfully")
     server.quit()
     return(json.dumps({'Return': 'Message Send Successfully',"Return_Code":"MSS","Status": "Success","Status_Code": "200"}, sort_keys=True, indent=4))



def callexternalapi(request):
     #conf_no = request.json['conf_no']
     #conf_no = request.json['conf_no']
     #print(conf_no)
     phone = request.json['mobile']
     d = {}
     d['customer_mobile'] = phone
     result = json.loads(gensql('select','ivr_room_customer_booked','*',d))
     #result = json.loads(result)
     re = result[0]
     print(re)
     #car1={"mobile":phone}
     #car1 = {"conf_no":conf_no}
     #print(car1)
     #r = requests.post('https://ivrinfocuit.herokuapp.com/FetchExistingBookings', json=car1)
     #re = r.json()
     
     print(type(re))
     name = re['customer_name']
     email = "infocuit.banupriya@gmail.com"
     message = "Booking Confirmed"
     conf_no = re['customer_confirmation_number']
     hotel_name = "SMARTMO"
     arrival = re['customer_arrival_date']
     depature = re['customer_depature_date']
     room_type = re['customer_room_type']
     
     return sendemailani(name,email,message,conf_no,hotel_name,arrival,depature,room_type)
