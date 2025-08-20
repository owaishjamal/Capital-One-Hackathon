from django.test import TestCase
from twilio.rest import Client

# Create your tests here.
def send_report_via_sms():
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
            body = f'''नमस्ते, आर्यन
                    उत्पाद का नाम: मक्का
                    समाप्ति तिथि: कल, 26-02-2024

                    उत्पाद का नाम: ज्वार
                    समाप्ति तिथि: कल, 26-02-2024

                    उत्पाद का नाम: गेहूं
                    समाप्ति तिथि: कल, 26-02-2024

                    उत्पाद का नाम: चावल
                    समाप्ति तिथि: कल, 26-02-2024

                    कृपया इन्हें जल्द से जल्द उपयोग करें या बाजार में बेचने के लिए विचार करें। धन्यवाद!''',
  to='whatsapp:+918879519771'
    )

    print(message.sid)

send_report_via_sms()