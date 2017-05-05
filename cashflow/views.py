from django.shortcuts import render, HttpResponse
import time, json, pprint, requests, binascii, base64, hashlib, os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from django.views.decorators.csrf import csrf_exempt

from .forms import AddMerchantForm, PaymentForm
from ecommerce.forms import OrderingForm
from ecommerce.models import Ordering


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
    # material = ''
    # material_price = ''
    course = ''
    vendor = ''
    total_amount = ''
    if request.method == "POST":
        order_form = OrderingForm(request.POST)
        if order_form.is_valid():
            # material = order_form.cleaned_data['material']
            available_time = order_form.cleaned_data['available_time']
            number = order_form.cleaned_data['participants_number']
            course = available_time.course
            vendor = course.vendor

            total_amount = int(course.price) * int(number)




            form.fields['MerchantID'].initial = 'MS39344778'
            form.fields['RespondType'].initial = 'JSON'
            form.fields['TimeStamp'].initial = str(time.time())
            form.fields['Version'].initial = '1.2'
            form.fields['LangType'].initial = 'zh-tw'
            form.fields['MerchantOrderNo'].initial = time.strftime("%y%m%d%H%M%S") + str(available_time.pk)
            form.fields['Amt'].initial = int(total_amount)
            form.fields['ItemDesc'].initial = course.name
            form.fields['TradeLimit'].initial = ''
            form.fields['ExpireDate'].initial = ''
            form.fields['ReturnURL'].initial = request.build_absolute_uri('comfirm_order') + "/"
            form.fields['NotifyURL'].initial = ''
            form.fields['CustomerURL'].initial = ''
            form.fields['ClientBackURL'].initial = ''
            form.fields['Email'].initial = request.user.email
            form.fields['EmailModify'].initial = 0
            form.fields['LoginType'].initial = 0
            form.fields['OrderComment'].initial = ''
            form.fields['CREDIT'].initial = 1
            form.fields['InstFlag'].initial = 0
            form.fields['UNIONPAY'].initial = 0
            form.fields['WEBATM'].initial = 0
            form.fields['VACC'].initial = 0
            form.fields['CVS'].initial = 1
            form.fields['BARCODE'].initial = 1
            form.fields['CUSTOM'].initial = 0


            check_value = "HashKey=" + os.environ['PAYMENT_HASHKEY'] + "&Amt=" + str(form.fields['Amt'].initial) + '&MerchantID=' + str(form.fields['MerchantID'].initial) + '&MerchantOrderNo=' + str(form.fields['MerchantOrderNo'].initial) + '&TimeStamp=' + form.fields['TimeStamp'].initial + '&Version=1.2&HashIV=' + os.environ['PAYMENT_HASHIV']
            shavalue = hashlib.sha256()
            shavalue.update(check_value.encode('utf-8'))


            form.fields['CheckValue'].initial = shavalue.hexdigest().upper()

            Ordering.objects.create(user=request.user, vendor=vendor, course=course, available_time=available_time, participants_number=int(number), total_amount=total_amount, check_value=form.fields['CheckValue'].initial, payment=False)


        else:
            context = {}
            return render(request, "payment_error.html", context)

    context = {
    "form": form,
    'vendor': vendor,
    'course': course,
    'available_time': available_time,
    'total_amount': total_amount,
    }

    return render(request, "payment.html", context)

@csrf_exempt
def comfirm_order(request):
    if request.method == "POST":
        data = request.POST.get('JSONData','')
        new_data = json.loads(data)
        result = new_data['Result'].replace('\"','"')
        new_result = json.loads(result)
        print(new_result["MerchantOrderNo"][12:])
        ordering = Ordering.objects.filter(user=request.user, available_time__pk=int(new_result["MerchantOrderNo"][12:]))[0]
        print(ordering)
        if ordering:
            ordering.payment = True
            ordering.save()

    context = {
    "data": data,
    "new_result": new_result
    }

    return render(request, "comfirm_order.html", context)
