from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('')
        params = {
            'sender': '10008663 ',
            'receptor': phone_number,
            'message': f'{code}کد تایید شما',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

# 545034334477372B394336692F714C7156506F3447746D727546552B55635271637252737867314B7632673D

