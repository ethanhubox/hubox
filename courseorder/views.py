from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from Crypto.Cipher import AES
from django.views.decorators.csrf import csrf_exempt
from hubox.settings import BASE_DIR
from django.core.mail import send_mail


import time, os, hashlib, base64, binascii, json

from .models import CourseOrder
from .forms import CoursePreOrderForm, CheckOutForm, CourseOrderPaymentForm
from ecommerce.models import AvailableTime, Voucher, Ordering

@login_required
def course_check_out(request):
    available_time = ''
    course = ''
    vendor = ''
    if request.method == "GET":
        form = CoursePreOrderForm(request.GET)
        available_time = AvailableTime.objects.get(pk=request.GET.get('available_time'))
        participants_number = request.GET.get('participants_number')
        if form.is_valid():
            if available_time.quota - int(participants_number) < 0:
                messages.error(request, '課程已額滿')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            form = CheckOutForm()
            try:
                profile = request.user.profile
                form.fields['name'].initial = profile.name
                form.fields['phone'].initial = profile.phone
                form.fields['address'].initial = profile.address
            except:
                pass

            form.fields['available_time'].initial = int(request.GET.get('available_time'))
            form.fields['participants_number'].initial = int(request.GET.get('participants_number'))

            available_time = get_object_or_404(AvailableTime, pk=int(request.GET.get('available_time')))
            course = available_time.course
            vendor = course.vendor

        else:
            messages.error(request, '請確認所有欄位都有填寫')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'form': form,
        'available_time': available_time,
        'course': course,
        'vendor': vendor,
    }
    return render(request, 'course_check_out.html', context)


def create_order(request):
    form = CheckOutForm()
    if request.method == "POST":
        form = CheckOutForm(request.POST)
        if form.is_valid():
            print('valid')
            available_time = get_object_or_404(AvailableTime, pk=int(form.cleaned_data['available_time']))
            course_order = CourseOrder.objects.create(
            user=request.user,
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            address=form.cleaned_data['address'],
            vendor=available_time.course.vendor,
            course=available_time.course,
            available_time=available_time,
            participants_number=form.cleaned_data['participants_number'],
            )

            if form.cleaned_data['voucher']:
                voucher = Voucher.objects.get(serial_number=form.cleaned_data['voucher'])
                course_order.voucher = voucher
                course_order.total_amount = course_order.available_time.course.price - voucher.price
            else:
                course_order.total_amount = course_order.available_time.course.price

            course_order.order_number = 'HBX{}_{}'.format(str(course_order.pk), request.user.pk)
            if settings.DEBUG == True:
                course_order.order_number += '_0'
            else:
                course_order.order_number += '_1'
            course_order.order_number += '_C'
            course_order.save()

            return HttpResponseRedirect(reverse('course_order_detail', kwargs={"pk":course_order.pk}))


        else:
            messages.error(request, '錯誤，請重新購買')
            available_time = AvailableTime.objects.get(pk=request.POST.get('available_time'))
            course = available_time.course
            return HttpResponseRedirect(reverse('course_detail', kwargs={"pk":course.pk}))

    return HttpResponse(status=204)


def voucher_check(request):
    if request.is_ajax() and request.method == "POST":
        serial_number = request.POST.get('voucher', '')
        if serial_number:
            try:
               voucher = Voucher.objects.get(serial_number=serial_number)
               if voucher.aply == False:
                   return JsonResponse({"status":"ok", "voucher":voucher.serial_number, "price":voucher.price})
               else:
                   return JsonResponse({"status":"applied"})
            except Voucher.DoesNotExist:
               return JsonResponse({"status":"404"})
        else:
            return JsonResponse({"status":"no_serial"})
    return JsonResponse({"status":"error"})





@login_required
def course_order_detail(request, pk):
    course_order = get_object_or_404(CourseOrder, pk=pk)

    total_amount = course_order.total_amount
    form = CourseOrderPaymentForm()

    form.fields['MerchantID'].initial = 'MS39344778'
    form.fields['RespondType'].initial = 'JSON'
    form.fields['TimeStamp'].initial = str(time.time())
    form.fields['Version'].initial = '1.2'
    form.fields['LangType'].initial = 'zh-tw'
    form.fields['MerchantOrderNo'].initial = course_order.order_number
    form.fields['Amt'].initial = int(total_amount)
    form.fields['ItemDesc'].initial = str(request.user)
    form.fields['TradeLimit'].initial = ''
    form.fields['ExpireDate'].initial = ''
    form.fields['ReturnURL'].initial = request.build_absolute_uri(reverse('finish_course_order'))
    form.fields['NotifyURL'].initial = ''
    form.fields['CustomerURL'].initial = request.build_absolute_uri(reverse('finish_course_order'))
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

    check_value = "HashKey=" + os.environ['PAYMENT_HASHKEY'] + "&Amt=" + str(form.fields['Amt'].initial) + '&MerchantID=' + str(form.fields['MerchantID'].initial) + '&MerchantOrderNo=' + str(form.fields['MerchantOrderNo'].initial) + '&TimeStamp=' + form.fields['TimeStamp'].initial + '&Version=' + form.fields['Version'].initial + '&HashIV=' + os.environ['PAYMENT_HASHIV']
    shavalue = hashlib.sha256()
    shavalue.update(check_value.encode('utf-8'))

    form.fields['CheckValue'].initial = shavalue.hexdigest().upper()


    context = {
        'course_order':course_order,
        'form':form,
    }

    return render(request, "course_order_detail.html", context)


@login_required
def cancel_course_order(request):
    course_order = ''
    if request.method == "POST":
        if request.POST.get("username", '') == request.user.username:
            course_order = get_object_or_404(CourseOrder, user=request.user, pk=int(request.POST.get("course_order")))
            course_order.delete()
            return HttpResponseRedirect(reverse('profile'))

    context = {
        "course_order": course_order,
    }

    return HttpResponse(status=204)


@csrf_exempt
def finish_course_order(request):
    course_order = ''
    if request.method == "POST":
        data = request.POST.get('JSONData','')
        new_data = json.loads(data)
        result = new_data['Result'].replace('\"','"')
        new_result = json.loads(result)


        if new_data['Status'] == "SUCCESS":
            check_value = 'HashIV=' + os.environ['PAYMENT_HASHIV'] + "&Amt=" + str(new_result['Amt']) + '&MerchantID=' + str(new_result['MerchantID']) + '&MerchantOrderNo=' + str(new_result['MerchantOrderNo']) + '&TradeNo=' + str(new_result['TradeNo']) + "&HashKey=" + os.environ['PAYMENT_HASHKEY']
            shavalue = hashlib.sha256()
            shavalue.update(check_value.encode('utf-8'))

            check_value = shavalue.hexdigest().upper()

            if check_value == new_result['CheckCode']:
                course_order = CourseOrder.objects.filter(user=request.user, pk=int(new_result["MerchantOrderNo"].replace('HBX', '').split('_')[0]))[0]
                if course_order:
                    if new_result['PaymentType'] == 'CREDIT':
                        course_order.payment_choice = '信用卡'
                        course_order.pay_check = True

                    elif new_result['PaymentType'] == 'CVS':
                        course_order.payment_choice = '超商繳款'

                    course_order.save()

                    voucher = course_order.voucher
                    if voucher:
                        voucher.aply = True
                        voucher.save()

                    with open(os.path.join(BASE_DIR, 'courseorder', 'templates') + '/order_mail.txt', 'w') as content:
                        content.write("訂單資訊：\n訂單編號：{}\n會員：{}\n姓名：{}\n聯絡電話：{}\n聯絡地址：{}\n訂單內容：{} {} {}~{}\n參加人數：{}人\n訂單金額：{}".format(
                            course_order.order_number,
                            str(course_order.user),
                            course_order.name,
                            course_order.phone,
                            course_order.address,
                            course_order.available_time.course.name,
                            course_order.available_time.date.strftime("%Y-%m-%d"),
                            course_order.available_time.start_time.strftime("%H:%M"),
                            course_order.available_time.end_time.strftime("%H:%M"),
                            str(course_order.participants_number),
                            str(course_order.total_amount)
                        ))
                    if course_order.pay_check == True:
                        with open(os.path.join(BASE_DIR, 'courseorder', 'templates') + '/order_mail.txt', "a") as append_content:
                            append_content.write("\n繳費狀態：已繳費")
                    file = open(os.path.join(BASE_DIR, 'courseorder', 'templates') + '/order_mail.txt', 'r')
                    content = file.read()

                    if settings.DEBUG == True:
                        system_mail = ['miwooro@hotmail.com']
                    else:
                        system_mail = ['ethan@hubox.life', 'frank@hubox.life']


                    send_mail(
                        '訂單成立',
                        content,
                        'Hubox哈盒子',
                        system_mail,
                        fail_silently=False,
                    )

        else:
            course_order = CourseOrder.objects.filter(user=request.user, pk=int(new_result["MerchantOrderNo"].replace('HBX', '').split('_')[0]))[0]
            messages.error(request, '付款失敗，請重試一次或聯絡我們')



    context = {
        'course_order': course_order
    }

    return HttpResponseRedirect(reverse('course_order_detail', kwargs={'pk': course_order.pk}))

@login_required
def course_order_refund(request):
    course_order = ''
    if request.method == "POST":
        course_order = get_object_or_404(CourseOrder, order_number=request.POST.get('order_number'))
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')


        with open(os.path.join(BASE_DIR, 'courseorder', 'templates') + '/refund.txt', 'w') as content:
            content.write("訂單資訊：" + "\n訂單編號：" + course_order.order_number + "\n會員：" + str(course_order.user) + "\n聯絡電話：" + course_order.user.profile.phone + "\n聯絡信箱：" + email + "\n退款原因：\n" + message)
        if course_order.pay_check == True:
            with open(os.path.join(BASE_DIR, 'courseorder', 'templates') + '/refund.txt', "a") as append_content:
                append_content.write("\n繳費狀態：已繳費")
        file = open(os.path.join(BASE_DIR, 'courseorder', 'templates') + '/refund.txt', 'r')
        content = file.read()

        if settings.DEBUG == True:
            system_mail = ['miwooro@hotmail.com']
        else:
            system_mail = ['ethan@hubox.life', 'frank@hubox.life']

        send_mail(
            '訂單退款',
            content,
            'Hubox哈盒子',
            system_mail,
            fail_silently=False,
        )

    context = {
        'course_order': course_order,
        'phone': phone,
        'email': email,
        'message': message,
    }
    return render(request, "refund.html", context)

from django.template.loader import get_template
from hubox.utils import render_to_pdf

def eticket(request, pk):
    course_order = get_object_or_404(CourseOrder, pk=pk)

    context = {
        'course_order': course_order,
        'host_name': request.get_host()
    }

    return render(request, "eticket.html", context)
    # course_order = get_object_or_404(CourseOrder, pk=pk)
    # context = {
    #     'course_order': course_order,
    # }
    # template = get_template('eticket.html')
    # pdf = render_to_pdf('eticket.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')

def copy_order(request):
    orders = Ordering.objects.all()
    for order in orders:
        if order.cart.cartitem_set.all():
            new = CourseOrder.objects.create(
            order_number=order.order_number,
            user=order.user,
            name=order.user.userprofile.name,
            phone=order.user.userprofile.phone,
            address=order.user.userprofile.address,
            vendor=order.cart.cartitem_set.all()[0].available_time.course.vendor,
            course=order.cart.cartitem_set.all()[0].available_time.course,
            available_time=order.cart.cartitem_set.all()[0].available_time,
            participants_number=order.cart.cartitem_set.all()[0].participants_number,
            voucher=order.cart.voucher,
            total_amount=order.total_amount,
            payment_choice=order.payment_choice,
            pay_check=order.payment,
            timestamp=order.timestamp,
            )
        else:
            continue

    return HttpResponse('success')
