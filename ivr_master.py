'''
This is the master file for all the Web services
related to IVR application
'''
import json
from flask import Flask,request, jsonify
from flask_cors import CORS
from QueryANITEST import queryanitest
from QueryANI import queryani
from UpdateCustomerLangSelected import updatecustomerlangselected
from FetchExistingBookings import fetchexistingbookings
from CancelCurrentbooking import cancelcurrentbooking
from FetchRoomsAvailabilityandPrice import fetchroomsavailabilityandprice
from FetchRoomsAvailabilityandPrice import fetchpromotionalmessage
from CalculateTotalChargesAndRetrieveConfirmationNumber import calculatetotalcharges
from UpdatedCustomerProfile import updatedcustomerprofile
from SendSMS import sendsms
from SendEmailIVR import sendemailivr
##extranet
from SignupExtranet import signup
from LoginExtranet import login
from AvailableRoomCount import availableroomcount
from RoomList import roomlist
from RatesandAvailability import ratesandavailability
from InsertRatesandAvailability import insertratesandavailability
from UpdateRatesandAvailability import updateratesandavailability
from AddDiscount import adddiscount
from QueryDiscount import querydiscount
#add
from CheckDate import validationivr
from SendEmail import sendemail
from SendEmailANI import callexternalapi
from RatesInsertAndUpdate import ratesinsertandupdate
from UpdateExistingBooking import updateexistingbooking
from PromotionalCancelMessage import promotionalcancelmessage
from InsertCustomerRoomBooking import insertcustomerroombooking
from ValidateConfirmationNumber import validateconfirmationnumber
from FetchBooking import fetchbooking
#
from phonenumber import phonenumbers_country
from PromotionalCancelMessage import insertcancelmessage
from FetchRoomsAvailabilityandPrice import insertpromotionalmessage
from RoomList import insertroomlist
from InsertCancelPolicy import insertcancelpolicy
from InsertCancelPolicy import QueryStatistics
from Insert_Ivr_Reservation import Insert_Ivr_Reservation
from Getreservationcancelmodification import Getreservationcancelmodification
from Getchannelcount import Getchannelcounts
from Getreservationcancelmodification import GetBookingConfirmation
from SendSMS import UpdateSMSmessage
from SendSMS import Updateivrsmsmessage
from Getreservationcancelmodification import Getsmscount
from Getreservationcancelmodification import GetLanguagecount
from Getreservationcancelmodification import GetRoomOccupancy
from Getreservationcancelmodification import GetYearbyyeareservationcount
from Getreservationcancelmodification import GetCountryreservation
# add changes
from RatesandAvailability import daterange
from RoomList import restriction
from configuration import config
from configuration import select_config
from configuration import update_config
from Insert_Ivr_Reservation import Query_Reservation


#configuration
from ExtranetConfiguration import RoomsizeConfiguration
from ExtranetConfiguration import BeddingoptionsConfiguration
from ExtranetConfiguration import BedsizeConfiguration
from ExtranetConfiguration import RoomamenitieConfiguration
from ExtranetConfiguration import InclusionsConfiguration
from ExtranetConfiguration import DeleteRoomsizeConfiguration
from ExtranetConfiguration import DeleteBeddingoptionsConfiguration
from ExtranetConfiguration import DeleteBedSizeConfiguration
from ExtranetConfiguration import DeleteInclusionsConfiguration
from ExtranetConfiguration import DeleteRoomamenitieConfiguration

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
   return "Welcome to IVR!"
@app.route('/QueryANI/test',methods=['GET'])
def QueryANITest():
   return queryanitest(request)

@app.route('/QueryANI',methods=['GET','POST'])
def QueryANIinfo():
   return queryani(request)
@app.route('/UpdateCustomerLangSelected',methods=['GET'])
def LangSelected():
   return updatecustomerlangselected(request)
@app.route('/FetchExistingBookings',methods=['GET','POST'])
def ExistingBookings():
   return fetchexistingbookings(request)
@app.route('/CancelCurrentbooking',methods=['GET'])
def Cancelbooking():
   return cancelcurrentbooking(request)
@app.route('/FetchRoomsAvailabilityandPrice',methods=['GET','POST'])
def FetchRooms():
   return fetchroomsavailabilityandprice(request)
@app.route('/FetchPromotionalMessage',methods=['GET','POST'])
def FetchPromotionalMessage():
   return fetchpromotionalmessage(request)
@app.route('/CalculateTotalCharges',methods=['POST'])
def CalculateTotalCharges():
   return calculatetotalcharges(request)
@app.route('/UpdatedCustomerProfile',methods=['POST'])
def UpdatedProfile():
   return updatedcustomerprofile(request)
@app.route('/SendSMS',methods=['POST'])
def SMS():
   return sendsms(request)
@app.route('/SendEmailIVR',methods=['POST'])
def Email():
   return sendemailivr(request)
##extranet
@app.route('/SignupExtranet',methods=['POST'])
def ExSignup():
   return signup(request)
@app.route('/LoginExtranet',methods=['POST'])
def ExLogin():
   return login(request)
@app.route('/AvailableRoomCount',methods=['POST'])
def ExAvailableRoomCount():
   return availableroomcount(request)
@app.route('/RoomList',methods=['POST'])
def ExRoomList():
   return roomlist(request)
@app.route('/RatesandAvailability',methods=['POST'])
def ExRatesandAvailability():
   return ratesandavailability(request)
@app.route('/InsertRatesandAvailability',methods=['POST'])
def ExInsertRatesandAvailability():
   return insertratesandavailability(request)
@app.route('/UpdateRatesandAvailability',methods=['POST'])
def ExUpdateRatesandAvailability():
   return updateratesandavailability(request)
@app.route('/AddDiscount',methods=['POST'])
def Discount():
   return adddiscount(request)
@app.route('/QueryDiscount',methods=['POST'])
def QueryDiscount():
   return querydiscount(request)
#add
@app.route('/ValidationIVR',methods=['POST'])
def CheckDate():
   return validationivr(request)
@app.route('/SendEmail',methods=['POST'])
def  sendemailmessage():
   return sendemail(request)
@app.route('/SendEmailANI',methods=['POST'])
def sendanimessage():
   return callexternalapi(request)
@app.route('/RatesInsertAndUpdate',methods=['POST'])
def RatesInsertAndUpdate():
   return ratesinsertandupdate(request)
@app.route('/UpdateExistingBooking',methods=['POST'])
def UpdateExistingBooking():
   return updateexistingbooking(request)
@app.route('/PromotionalCancelMessage',methods=['POST'])
def PromotionalCancelMessage():
   return promotionalcancelmessage(request)
@app.route('/InsertCustomerRoomBooking',methods=['POST'])
def InsertCustomerRoomBooking():
   return insertcustomerroombooking(request)
@app.route('/ValidateConfirmationNumber',methods=['POST'])
def ValidateConfirmationNumber():
   return validateconfirmationnumber(request)
@app.route('/FetchBooking',methods=['POST'])
def FetchBooking():
   return fetchbooking(request)
#
@app.route('/Phonenumbers',methods=['POST'])
def Phonenumbers():
   return phonenumbers_country(request)
@app.route('/InsertCancelMessage',methods=['POST'])
def InsertCancelMessage():
   return insertcancelmessage(request)
@app.route('/InsertPromotionalMessage',methods=['POST'])
def InsertPromotionalMessage():
   return insertpromotionalmessage(request)
@app.route('/InsertRoomList',methods=['POST'])
def InsertRoomList():
   return insertroomlist(request)
@app.route('/InsertCancelPolicy',methods=['POST'])
def InsertCancelPolicy():
   return insertcancelpolicy(request)
@app.route('/QueryStatistics',methods=['POST'])
def QueryStatisticsRecord():
   return QueryStatistics(request)
@app.route('/Insert_Ivr_Reservations',methods=['POST'])
def Insert_Ivr_Reservationswer():
   return Insert_Ivr_Reservation(request)
@app.route('/Getreservationcancelmodification',methods=['POST'])
def dashboarddetails():
   return Getreservationcancelmodification(request)
@app.route('/Getchannelcounts',methods=['POST'])
def Getchannelcounts_all():
   return Getchannelcounts(request)
@app.route('/GetBookingConfirmation',methods=['POST'])
def GetBookingConfirmation_all():
   return GetBookingConfirmation(request)

@app.route('/UpdateSMSmessage',methods=['POST'])
def UpdateSMSmessage_all():
   return UpdateSMSmessage(request)

@app.route('/Updateivrsmsmessage',methods=['POST'])
def Updateivrsmsmessage_all():
   return Updateivrsmsmessage(request)
@app.route('/Getsmscount',methods=['POST'])
def Getsmscount_all():
   return Getsmscount(request)
@app.route('/GetLanguagecount',methods=['POST'])
def GetLanguagecount_all():
   return GetLanguagecount(request)
@app.route('/GetRoomOccupancyall',methods=['POST'])
def GetRoomOccupancy_all():
   return GetRoomOccupancy(request)

@app.route('/GetYearbyyeareservationcount',methods=['POST'])
def GetYearbyyeareservationcount_all():
   return GetYearbyyeareservationcount(request)

@app.route('/GetCountryreservation',methods=['POST'])
def GetCountryreservation_all():
   return GetCountryreservation(request)

# add changes

@app.route('/daterange',methods=['POST'])
def daterangeforrates():
   return daterange(request)

@app.route('/restriction',methods=['POST'])
def restriction_rates():
   return restriction(request)

@app.route('/insert_configuration',methods=['POST'])
def insert_configuration():
   return config(request)

@app.route('/select_configuration',methods=['POST'])
def select_configuration():
   return select_config(request)

@app.route('/update_configuration',methods=['POST'])
def update_configuration():
   return update_config(request)

@app.route('/Query_Reservation',methods=['POST','GET'])
def Query_Reservation_Data():
   return Query_Reservation(request)


#configuration
@app.route('/RoomsizeConfiguration',methods=['POST'])
def RoomsizeConfiguration_all():
   return RoomsizeConfiguration(request)
@app.route('/BeddingoptionsConfiguration',methods=['POST'])
def BeddingoptionsConfiguration_all():
   return BeddingoptionsConfiguration(request)
@app.route('/BedsizeConfiguration',methods=['POST'])
def BedsizeConfiguration_all():
   return BedsizeConfiguration(request)
@app.route('/RoomamenitieConfiguration',methods=['POST'])
def RoomamenitieConfiguration_all():
   return RoomamenitieConfiguration(request)
@app.route('/InclusionsConfiguration',methods=['POST'])
def InclusionsConfiguration_all():
   return InclusionsConfiguration(request)
@app.route('/DeleteRoomsizeConfiguration',methods=['POST'])
def DeleteRoomsizeConfiguration_all():
   return DeleteRoomsizeConfiguration(request)
@app.route('/DeleteBeddingoptionsConfiguration',methods=['POST'])
def DeleteBeddingoptionsConfiguration_all():
   return DeleteBeddingoptionsConfiguration(request)
@app.route('/DeleteBedSizeConfiguration',methods=['POST'])
def DeleteBedSizeConfiguration_all():
   return DeleteBedSizeConfiguration(request)
@app.route('/DeleteInclusionsConfiguration',methods=['POST'])
def DeleteInclusionsConfiguration_all():
   return DeleteInclusionsConfiguration(request)
@app.route('/DeleteRoomamenitieConfiguration',methods=['POST'])
def DeleteRoomamenitieConfiguration_all():
   return DeleteRoomamenitieConfiguration(request)
if __name__ == "__main__":
  app.run(debug=True)
  #app.run(host="192.168.1.10",port=5000)
   
