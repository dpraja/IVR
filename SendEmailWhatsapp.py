import requests
import json
import smtplib
from sqlwrapper import gensql,dbget
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from dateutil import parser
import sys
def sendemailwhatsapp(request):
     #print(name,email,type(email),message,conf_no,arrival,depature, room_type)
     sys.stdout.flush()
     e = request.json
     print(e)
     Hotel_name = 'Kconnect24/7'
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
     #print(d[0]['customer_amount'],type(d[0]['customer_amount']))
     #email = ['infocuit.banupriya@gmail.com','infocuit.daisy@gmail.com']
     
     email.append(d[0]['email'])
     email.append(d[0]['customer_email'])
     print(email)
     on = d[0]['booked_date']
     print(on[:11], type(on[:11]))
     booked_on = parser.parse(on[:11]).date().strftime('%Y-%m-%d')
     sender = "infocuit.testing@gmail.com"
     
     t_body = """
                       <tr>
                         <th align="left">Date</th>
                         <th align="left">Rate</th>
                         <th align="left">Price Per Night in $</th>
                       </tr>

             """

     for rate in rate_day:
         print(rate)
         t_body += """
                       <tr style="border:1px solid gray">
                         <td>"""+rate['rate_date']+"""</td>
                         <td></td>
                         <td align="left">"""+str(rate['amount'])+"""</td>
                       </tr>
                   """
     t_body += """
                       <tr style="border:1px solid gray">
                         <td><b>Total</b></td>
                         <td></td>
                         <td align="left">"""+str(d[0]['customer_amount'])+"""</td>
                       </tr>
              """
     print("t_body-----------------------")
     print(t_body)
     
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
<meta charset="UTF-8">
<title>Title of the document</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

<body>
 <div class="panel panel-primary">
        <div class="panel-body">
          <div class="row" style="border:1px solid lightgrey;margin:10px ">
            <div class="col-md-4" style="padding:10px;">
              <p style="line-height:0.7"> <span>Arrival</span> <span style="padding-left:440px">Guest Name:</span></p> 
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_arrival_date'])+"""</span> <span style="padding-left:440px">"""+str(d[0]['customer_name'])+"""</span></p>
              <br>        
              <p style="line-height:0.7"><span>Departure</span> <span style="padding-left:440px">Preferred Language</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_depature_date'])+"""</span><span style="padding-left:440px">"""+str(d[0]['ivr_language'])+"""</span></p>
              <br>
              <p style="line-height:0.7"><span>Hotel Name:</span><span style="padding-left:440px">Channel</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['hotel_name'])+"""</span><span style="padding-left:440px">"""+d[0]['channel']+"""</span></p>
              <br>
              <p style="line-height:0.7"><span>Total</span> Adult <span style="padding-left:440px">Confirmation Number</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_adult'])+"""</span><span style="padding-left:440px">"""+d[0]['customer_confirmation_number']+"""</span></p>
              <br>
              <p style="line-height:0.7"><span>Total Child</span><span style="padding-left:440px"> Booked On</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_child'])+"""</span><span style="padding-left:440px">"""+booked_on+"""</span></p>   
              <b>
              <p style="line-height:0.7"><span>Total Price</span><span style="padding-left:440px"> No Of Rooms</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_amount'])+"""</span><span style="padding-left:440px">"""+str(d[0]['customer_no_of_rooms'])+"""</span></p>
            
                <hr>
                <p style="line-height:0.7">Room Type</p>
                <p style="line-height:0.7">"""+d[0]['customer_room_type']+"""</p> 
               <br>
                <p style="line-height:0.7">Guest Name</p>
                <p style="line-height:0.7">"""+str(d[0]['customer_name'])+""" </p>  
                <br>
                <p style="line-height:0.7">Max Guest</p>
                <p style="line-height:0.7">"""+str(d[0]['customer_adult']+d[0]['customer_child'])+"""</p>
                <br>
                <p>Room Options</p>
                <label>
               
          <table style="border:1px solid gray; width:700px;">
                     <tbody style="border:1px solid gray">
                     """+t_body+"""
                     </tbody>
                   </table>
               <label>
                   <br>

                   <img src="https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&h=350" alt="" width:1400px; height="250px">
              </div>
          
		    
            <br>
          </div>
        
        </div>
      </div>
            
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
        
     return(json.dumps([{'Return': 'Message Send Successfully',"Return_Code":"MSS","Status": "Success","Status_Code": "200"}], sort_keys=True, indent=4))

