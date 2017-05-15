from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
import time, json, pprint, requests, binascii, base64, hashlib, os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from hubox.settings import BASE_DIR
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import PaymentForm

from ecommerce.models import Ordering
from cart.models import Cart
from hubox.custom_exceptions import OverfulfilException, OurOfDateException


# Create your views here.

@login_required
def payment(request):
    try:
        profile = request.user.userprofile
    except:
        return HttpResponseRedirect(reverse("create_user_profile") + "?next=" +  request.path )
    form = PaymentForm()

    cart_pk = request.session.get("cart_pk")
    if cart_pk == None:
        return HttpResponseRedirect(reverse('cart'))
    cart = Cart.objects.get(pk=cart_pk)
    if request.user.is_authenticated():
        cart.user = request.user
        cart.save()
    total_amount = cart.total

    for item in cart.cartitem_set.all():
        if item.available_time.quota < item.participants_number:
            messages.error(request, '{}課程已額滿'.format(item.available_time.course.name))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    ordering = Ordering.objects.create(cart=cart, user=request.user, total_amount=total_amount)


    form.fields['MerchantID'].initial = 'MS39344778'
    form.fields['RespondType'].initial = 'JSON'
    form.fields['TimeStamp'].initial = str(time.time())
    form.fields['Version'].initial = '1.2'
    form.fields['LangType'].initial = 'zh-tw'
    form.fields['MerchantOrderNo'].initial = 'HBX{}_{}'.format(str(ordering.pk), request.user.pk)
    form.fields['Amt'].initial = int(total_amount)
    form.fields['ItemDesc'].initial = str(request.user)
    form.fields['TradeLimit'].initial = ''
    form.fields['ExpireDate'].initial = ''
    form.fields['ReturnURL'].initial = request.build_absolute_uri(reverse('finish_order'))
    form.fields['NotifyURL'].initial = ''
    form.fields['CustomerURL'].initial = request.build_absolute_uri(reverse('finish_order'))
    form.fields['ClientBackURL'].initial = ''
    form.fields['Email'].initial = request.user.email
    form.fields['EmailModify'].initial = 1
    form.fields['LoginType'].initial = 0
    form.fields['OrderComment'].initial = ''
    form.fields['CREDIT'].initial = 1
    form.fields['InstFlag'].initial = 0
    form.fields['UNIONPAY'].initial = 0
    form.fields['WEBATM'].initial = 0
    form.fields['VACC'].initial = 0
    form.fields['CVS'].initial = 1
    form.fields['BARCODE'].initial = 0
    form.fields['CUSTOM'].initial = 0


    check_value = "HashKey=" + os.environ['PAYMENT_HASHKEY'] + "&Amt=" + str(form.fields['Amt'].initial) + '&MerchantID=' + str(form.fields['MerchantID'].initial) + '&MerchantOrderNo=' + str(form.fields['MerchantOrderNo'].initial) + '&TimeStamp=' + form.fields['TimeStamp'].initial + '&Version=1.2&HashIV=' + os.environ['PAYMENT_HASHIV']
    shavalue = hashlib.sha256()
    shavalue.update(check_value.encode('utf-8'))


    form.fields['CheckValue'].initial = shavalue.hexdigest().upper()

    ordering.order_number = form.fields['MerchantOrderNo'].initial
    ordering.save()

    del request.session['cart_pk']

    context = {
    "form": form,
    'total_amount': total_amount,
    'ordering': ordering,
    }

    return render(request, "payment.html", context)

@csrf_exempt
def finish_order(request):
    ordering = ''
    if request.method == "POST":
        data = request.POST.get('JSONData','')
        new_data = json.loads(data)
        result = new_data['Result'].replace('\"','"')
        new_result = json.loads(result)


        check_value = 'HashIV=' + os.environ['PAYMENT_HASHIV'] + "&Amt=" + str(new_result['Amt']) + '&MerchantID=' + str(new_result['MerchantID']) + '&MerchantOrderNo=' + str(new_result['MerchantOrderNo']) + '&TradeNo=' + str(new_result['TradeNo']) + "&HashKey=" + os.environ['PAYMENT_HASHKEY']
        shavalue = hashlib.sha256()
        shavalue.update(check_value.encode('utf-8'))

        check_value = shavalue.hexdigest().upper()


        if new_data['Status'] == "SUCCESS":
            if check_value == new_result['CheckCode']:
                ordering = Ordering.objects.filter(user=request.user, pk=int(new_result["MerchantOrderNo"].replace('HBX', '').split('_')[0]))[0]
                if ordering:
                    if new_result['PaymentType'] == 'CREDIT':
                        ordering.payment_choice = '信用卡'
                        ordering.payment = True
                    elif new_result['PaymentType'] == 'CVS':
                        ordering.payment_choice = '超商繳款'

                    ordering.save()

                    cart_item = ordering.cart.cartitem_set.all()
                    for item in cart_item:
                        item_string = ''
                        item_string += "\n" + item.available_time.course.name + " " + item.available_time.date.strftime("%Y-%m-%d %H:%M") + " " + item.available_time.start_time.strftime("%H:%M") + "～" + item.available_time.end_time.strftime("%H:%M") + " " + str(item.participants_number) + "人"

                    with open(os.path.join(BASE_DIR, 'cashflow', 'templates') + '/order_mail.txt', 'w') as content:
                        content.write("訂單資訊：" + "\n訂單編號：" + ordering.order_number + "\n會員：" + str(ordering.user) + "\n聯絡電話：" + ordering.user.userprofile.phone + "\n聯絡地址：" + ordering.user.userprofile.address + "\n訂單內容：" + item_string)
                    if ordering.payment == True:
                        with open(os.path.join(BASE_DIR, 'cashflow', 'templates') + '/order_mail.txt', "a") as append_content:
                            append_content.write("\n繳費狀態：已繳費")
                    file = open(os.path.join(BASE_DIR, 'cashflow', 'templates') + '/order_mail.txt', 'r')
                    content = file.read()

                    to_mail = ['miwooro@hotmail.com']
                    # to_mail = ['ethan@hubox.life', 'frank@hubox.life']
                    to_mail.append(ordering.user.email)
                    send_mail(
                        '訂單成立',
                        content,
                        'Hubox哈盒子',
                        to_mail,
                        fail_silently=False,
                )



                return HttpResponseRedirect(reverse('ordering_detail', kwargs={'pk': ordering.pk}))


    context = {
        'ordering': ordering
    }

    return render(request, "finish_order.html", context)

@login_required
def cancel_ordering(request):
    ordering = ''
    if request.method == "POST":
        if request.POST.get("username", '') == request.user.username:
            ordering = get_object_or_404(Ordering, user=request.user, pk=int(request.POST.get("ordering", '')))
            ordering.delete()
            return HttpResponseRedirect(reverse('user_profile'))

    context = {
        "ordering": ordering,
    }

    return render(request, "cancel_ordering.html", context)

@login_required
def refund(request):
    ordering = ''
    if request.method == "POST":
        ordering = get_object_or_404(Ordering, order_number=request.POST.get('order_number'))
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(request.POST)


        with open(os.path.join(BASE_DIR, 'cashflow', 'templates') + '/refund.txt', 'w') as content:
            content.write("訂單資訊：" + "\n訂單編號：" + ordering.order_number + "\n會員：" + str(ordering.user) + "\n聯絡電話：" + ordering.user.userprofile.phone + "\n聯絡信箱：" + email + "\n退款原因：\n" + message)
        if ordering.payment == True:
            with open(os.path.join(BASE_DIR, 'cashflow', 'templates') + '/refund.txt', "a") as append_content:
                append_content.write("\n繳費狀態：已繳費")
        file = open(os.path.join(BASE_DIR, 'cashflow', 'templates') + '/refund.txt', 'r')
        content = file.read()

        to_mail = ['miwooro@hotmail.com']
        # to_mail = ['ethan@hubox.life', 'frank@hubox.life']
        to_mail.append(ordering.user.email)
        send_mail(
            '訂單退款',
            content,
            'Hubox哈盒子',
            to_mail,
            fail_silently=False,
        )

    context = {
        'ordering': ordering,
        'phone': phone,
        'email': email,
        'message': message,
    }
    return render(request, "refund.html", context)
