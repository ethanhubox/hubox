from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from .models import Vendor, Course, Catagory, Ordering, IndexEdit, AvailableTime, UserSubscribe, UserProfile, VendorMedia, CourseMedia
from index.models import CatagoryPage
from .forms import UserProfileForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from itertools import chain
import os, time, json, datetime, hashlib
from django.contrib.auth.decorators import login_required
from cart.forms import CartItemForm
from cashflow.forms import PaymentForm
from Crypto.Hash import SHA256
from django.conf import settings
from PIL import Image

from hubox.settings import BASE_DIR
from django.core.mail import send_mail


from courseorder.forms import CoursePreOrderForm
# Create your views here.

def index(request):
    vendor = Vendor.objects.all().order_by('?')
    course = Course.objects.all().order_by('?')
    catagory = Catagory.objects.all().order_by('?')[:3]


    try:
        index = IndexEdit.objects.all()[0]
    except IndexEdit.DoesNotExist:
        index = None

    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        if name and email and phone and message:
            with open(os.path.join(BASE_DIR, 'ecommerce', 'templates') + '/contact_us.txt', 'w') as content:
                content.write("聯絡人姓名：{}\n信箱：{}\n電話：{}\n要說的話：\n{}".format(name, email, phone, message))
            file = open(os.path.join(BASE_DIR, 'ecommerce', 'templates') + '/contact_us.txt', 'r')
            content = file.read()

            to_mail = ['ethan@hubox.life', 'frank@hubox.life']
            send_mail(
                '聯絡我們',
                content,
                'Hubox哈盒子',
                to_mail,
                fail_silently=False,
            )

    context = {
    'vendor':vendor,
    'course':course,
    'catagory':catagory,
    'index':index,
    }

    return render(request, 'index.html', context)

def vendor_list(request):
    vendors = Vendor.objects.all()
    context = {'vendors':vendors}

    return render(request, 'vendor_list.html', context)

def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor_medias = vendor.vendormedia_set.all()
    courses = vendor.course_set.all()

    if request.user.is_authenticated():
        try:
            subscribe = UserSubscribe.objects.get(user=request.user, vendor=vendor)
        except:
            subscribe = False
        # except UserSubscribe.DoesNotExist:
        #     subscribe = False
        # except RelatedObjectDoesNotExist:
        #     pass
    else:
        subscribe = False


    context = {
    'vendor':vendor,
    'vendor_medias':vendor_medias,
    'courses':courses,
    'subscribe': subscribe,

    }

    return render(request, 'vendor_detail.html', context)

def course_list(request):
    catagory = Catagory.objects.all()
    try:
        catagory_element = CatagoryPage.objects.all()[0]
    except:
        catagory_element = ''

    context = {
    'catagory':catagory,
    'catagory_element':catagory_element,
    }

    return render(request, 'course_list.html', context)

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    all_available_time = course.availabletime_set.all()
    course_media = course.coursemedia_set.all()
    materials = course.material_set.all()
    googlemap_api_key = os.environ["GOOGLE_API_KEY"]

    gte_date = course.availabletime_set.filter(date__gte=datetime.datetime.now())[:3]

    form = CoursePreOrderForm()
    # form.fields['material'].queryset = materials
    form.fields['available_time'].queryset = all_available_time

    context = {
    'course':course,
    'course_media':course_media,
    'all_available_time': all_available_time,
    'gte_date':gte_date,
    'materials':materials,
    'form':form,
    'googlemap_api_key': googlemap_api_key,
    }

    return render(request, 'course_detail.html', context)

@login_required
def ordering_detail(request, pk):
    ordering = get_object_or_404(Ordering, pk=pk)
    total_amount = ordering.total_amount
    form = PaymentForm()

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


    context = {
    'ordering': ordering,
    'form': form,
    }

    return render(request, 'ordering_detail.html', context)


def catagory_detail(request, pk):
    catagory = get_object_or_404(Catagory, pk=pk)

    context = {
        'catagory': catagory,
    }

    return render(request, 'catagory_detail.html', context)

# @login_required
# def certificate(request, pk):
#     ordering = get_object_or_404(Ordering, pk=pk)
#     if request.user != ordering.user:
#         messages.add_message(request, messages.INFO, '你並沒有購買這個課程的憑證')


def media_compress(request):
    course_media = CourseMedia.objects.all()
    vendor_media = VendorMedia.objects.all()
    vendor = Vendor.objects.all()

    for c in course_media:
        image = Image.open(c.file.path)
        image.save(c.file.path, quality=85, optimize=True)

    for v in vendor_media:
        image = Image.open(v.file.path)
        image.save(v.file.path, quality=85, optimize=True)

    for v in vendor:
        image = Image.open(v.logo.path)
        image.save(v.logo.path, quality=85, optimize=True)

        image = Image.open(v.banner.path)
        image.save(v.banner.path, quality=85, optimize=True)


    return HttpResponse('success')
