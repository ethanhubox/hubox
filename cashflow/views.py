from django.shortcuts import render, HttpResponse
import time, json, pprint, requests, binascii, base64, hashlib, os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from .forms import AddMerchantForm, PaymentForm
from ecommerce.forms import OrderingForm


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
    c = "HashKey=AWMW8kVE7ZSFPdkuijnRHIw3PGbcyRa8&Amt=1200&MerchantID=MS39344778&MerchantOrderNo=201406010002&TimeStamp=1493880738&Version=1.2&HashIV=NW5Wh1Ao0t4QHokZ"
    shavalue = hashlib.sha256()
    shavalue.update(c.encode('utf-8'))
    # print(shavalue.digest().decode('utf-8'))
    print("我要的",shavalue.hexdigest().upper())
    # print(str(shavalue.digest(),'utf-8'))

    return render(request, "add_merchant.html", context)


def payment(request):
    form = PaymentForm()
    available_time = ''
    material = ''
    material_price = ''
    course = ''
    vendor = ''
    total_amount = ''
    if request.method == "POST":
        order_form = OrderingForm(request.POST)
        if order_form.is_valid():
            material = order_form.cleaned_data['material']
            material_price = material.price
            available_time = order_form.cleaned_data['available_time']
            course = available_time.course
            vendor = course.vendor
            total_amount = course.price + material_price

            print(order_form.cleaned_data)
            # form = PaymentForm()

            form.fields['MerchantID'].initial = 'MS39344778'
            form.fields['RespondType'].initial = 'JSON'
            form.fields['TimeStamp'].initial = str(time.time())
            form.fields['Version'].initial = '1.2'
            form.fields['LangType'].initial = 'zh-tw'
            form.fields['MerchantOrderNo'].initial = available_time.pk
            form.fields['Amt'].initial = int(total_amount)
            form.fields['ItemDesc'].initial = course.name
            form.fields['TradeLimit'].initial = ''
            form.fields['ExpireDate'].initial = ''
            form.fields['ReturnURL'].initial = ''
            form.fields['NotifyURL'].initial = ''
            form.fields['CustomerURL'].initial = ''
            form.fields['ClientBackURL'].initial = ''
            form.fields['Email'].initial = request.user.email
            form.fields['EmailModify'].initial = 1
            form.fields['LoginType'].initial = 0
            form.fields['OrderComment'].initial = ''
            form.fields['CREDIT'].initial = ''
            form.fields['InstFlag'].initial = ''
            form.fields['UNIONPAY'].initial = ''
            form.fields['WEBATM'].initial = ''
            form.fields['VACC'].initial = ''
            form.fields['CVS'].initial = ''
            form.fields['BARCODE'].initial = ''
            form.fields['CUSTOM'].initial = ''


            check_value = "HashKey=" + os.environ['PAYMENT_HASHKEY'] + "&Amt=" + str(form.fields['Amt'].initial) + '&MerchantID=' + str(form.fields['MerchantID'].initial) + '&MerchantOrderNo=' + str(form.fields['MerchantOrderNo'].initial) + '&TimeStamp=' + form.fields['TimeStamp'].initial + '&Version=1.2&HashIV=' + os.environ['PAYMENT_HASHIV']
            shavalue = hashlib.sha256()
            shavalue.update(check_value.encode('utf-8'))


            form.fields['CheckValue'].initial = shavalue.hexdigest().upper()

    context = {
    "form": form,
    'vendor': vendor,
    'course': course,
    'material': material,
    'available_time': available_time,
    'total_amount': total_amount,
    }

    return render(request, "payment.html", context)

def get_payback(request):
    if request.method == "POST":
        print(request.method)

    return HttpResponse(request.method)
