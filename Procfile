web: gunicorn ivr_master:app

worker: gunicorn sqlwrapper.py
worker: gunicorn QueryANI.py
worker: gunicorn FetchExistingBookings.py
worker: gunicorn FetchRoomsAvailabilityandPrice.py
worker: gunicorn UpdateCustomerLangSelected.py
worker: gunicorn FetchPromotionalMessage.py
worker: gunicorn CalculateTotalChargesAndRetrieveConfirmationNumber.py
worker: gunicorn UpdatedCustomerProfile.py
worker: gunicorn CancelCurrentbooking.py
worker: gunicorn SendSMS.py
worker: gunicorn SendEmailIVR.py
worker: gunicorn SendEmailIVRTEST.py
worker: gunicorn SignupExtranet.py
worker: gunicorn LoginExtranet.py
worker: gunicorn AvailableRoomCount.py
worker: gunicorn RoomList.py
worker: gunicorn RatesandAvailability.py
worker: gunicorn InsertRatesandAvailability.py
worker: gunicorn UpdateRatesandAvailability.py
worker: gunicorn AddDiscount.py
worker: gunicorn QueryDiscount.py
worker: gunicorn CheckDate.py

