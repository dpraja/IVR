import requests
import json
import smtplib
from sqlwrapper import gensql,dbget
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendemailwhatsapp(request):
     #print(name,email,type(email),message,conf_no,arrival,depature, room_type)
     e = request.json
     print(e)
     tfn = request.json['TFN']
     con_no = request.json['customer_confirmation_number']
     print(con_no,type(con_no))
     b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
     #print(b_id)
     bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
     print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))

     rate_day = json.loads(dbget("select * from customer_rate_detail where \
                          business_id='"+str(bi_id[0]['business_id'])+"' and customer_confirmation_number='"+con_no+"' "))
     print("rate_day",rate_day)
     
     d = json.loads(dbget("SELECT ivr_room_customer_booked.*,ivr_hotel_list.* FROM public.ivr_room_customer_booked \
                           join ivr_hotel_list on \
                           ivr_room_customer_booked.business_id = ivr_hotel_list.business_id\
                           where ivr_room_customer_booked.business_id='"+str(bi_id[0]['business_id'])+"' \
                           and ivr_room_customer_booked.customer_confirmation_number='"+str(con_no)+"' "))
     print("d",d)
     email = []
     email.append(d[0]['email'])
     email.append(d[0]['customer_email'])
     print(email)
     
     sender = "infocuit.testing@gmail.com"
     
     for receiver in email:

          
          #print(sender,type(sender),receiver,type(receiver))
          subject = "Hotel Booking"
          msg = MIMEMultipart()
          msg['from'] = sender
          msg['to'] = receiver
          msg['subject'] = subject
          
          html = """\
          <!DOCTYPE html>
          <html>
          <head>
          <meta charset="utf-8">
          </head>
          <body>
                  
          </body>
          </html>
          """

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

