from __future__ import absolute_import
import arrow
import dramatiq

from django.conf import settings
from twilio.rest import Client

#from comment.models import Appointment


from django.db import models
import os
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Appointment


#from  Appointment
#from comment.models import Appointment


# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
TWILIO_ACCOUNT_SID = 'AC46c019ea77dacf86ecea2d4bb44a3ca0'
TWILIO_AUTH_TOKEN = '62a1301a6bcaa6928f92fce0bdd679da'


print(TWILIO_ACCOUNT_SID)
print(TWILIO_AUTH_TOKEN)


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@dramatiq.actor
def send_sms_reminder(appointment_id):
    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    appointment_time = arrow.get(appointment.time, appointment.time_zone.zone)
    body = 'Hi {0}. You have an appointment coming up at {1}.'.format(
        appointment.name,
        appointment_time.format('h:mm a')
    )

    client.messages.create(
        body=body,
        to=appointment.phone_number,
        from_='+12393938910',
    )

    print(message.sid)




if __name__ == '__main__':
    app.run()