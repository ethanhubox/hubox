from django.shortcuts import render
import time, json, pprint, requests, binascii, base64, hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from .forms import AddMerchantForm, PaymentForm


# Create your views here.

def add_merchant(request):
    form = AddMerchantForm()

    if request.method == "POST":
        form = AddMerchantForm(request.POST)
        if form.is_valid():
            # print(request.POST)
            form.cleaned_data['TimeStamp'] = int(time.time())
            data = {}
            for d in form.cleaned_data:
                data[d] = form.cleaned_data[d]

            data = json.dumps(data)


            BLOCK_SIZE = 32
            PADDING = '\0'
            pad = lambda data: data + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * PADDING

            encryption_suite = AES.new('key', AES.MODE_CBC, 'iv')
            cipher_text = encryption_suite.encrypt(pad(data))

            decryption_suite = AES.new('', AES.MODE_CBC, '')
            # plain_text = decryption_suite.decrypt(binascii.a2b_hex(cipher_text))


            print('cipher_text', cipher_text)
            # print('plain_text', plain_text)

            URL = 'https://ccore.spgateway.com/API/AddMerchant'

            headers = {
                'content-type': 'application/x-www-form-urlencoded',
            }

            last_data={
                "PartnerID_":"hubox01",
                "PostData_": '',
            }


            r = requests.post(URL, headers=headers, data=last_data)

            print(r.status_code)
            print(r.json())

            form = AddMerchantForm(request.POST)

        else:
            form = AddMerchantForm(request.POST)
            print('no')



    context = {
    "form": form,
    }

    return render(request, "add_merchant.html", context)


def payment(request):


    print(c)
    shavalue = hashlib.sha256()
    shavalue.update("c".encode('utf-8'))

    # print(shavalue.digest().decode('utf-8'))
    print("我要的",shavalue.hexdigest().upper())
    # print(str(shavalue.digest(),'utf-8'))


    form = PaymentForm()
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():

            form.cleaned_data['TimeStamp'] = int(time.time())
            form.cleaned_data['RespondType'] = "JSON"
            form.cleaned_data['LangType'] = "zh-tw"
            form.cleaned_data['TradeLimit'] = 60
            form.cleaned_data['ExpireDate'] = 60
            form.cleaned_data['ReturnURL'] = ""
            form.cleaned_data['NotifyURL'] = ""
            form.cleaned_data['CustomerURL'] = ""
            form.cleaned_data['ClientBackURL'] = ""
            form.cleaned_data['LoginType'] = 0
            form.cleaned_data['CREDIT'] = 0



            data = {}
            for d in form.cleaned_data:
                data[d] = form.cleaned_data[d]

            # print(json.dumps(data))


            URL = 'https://ccore.spgateway.com/MPG/mpg_gateway'

            headers = {
                'content-type': 'application/x-www-form-urlencoded',
            }

            last_data={
                "PartnerID_":"hubox01",
                "PostData_": cipher_text,
            }


            r = requests.post(URL, headers=headers, data=data)

            print(r.status_code)
            print(r.json())


            form = PaymentForm(request.POST)
        else:
            form = PaymentForm(request.POST)

    context = {
    "form": form,
    }

    return render(request, "payment.html", context)
