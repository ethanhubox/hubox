from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from .models import Vendor, Course, Catagory, Ordering, IndexEdit, AvailableTime, UserSubscribe, UserProfile
from .forms import OrderingForm, UserProfileForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from datetime import datetime
from itertools import chain
import os, time, json
from django.contrib.auth.decorators import login_required

from hubox.settings import BASE_DIR
from django.core.mail import send_mail

# Create your views here.

def index(request):

    vendor = Vendor.objects.all().order_by('?')
    course = Course.objects.all().order_by('?')
    catagory = Catagory.objects.all().order_by('?')[:3]

    try:
        index = IndexEdit.objects.all()[0]
    except IndexEdit.DoesNotExist:
        index = None

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

def subscribe_ajax(request):
    vendor = get_object_or_404(Vendor, pk=request.POST.get("vendor", ''))
    if request.user.is_authenticated():
        user = request.user
        if request.method == "POST" and request.is_ajax():
            subscribe, created = UserSubscribe.objects.get_or_create(user=user, vendor=vendor)
            if created == False:
                subscribe.delete()
                subscribe = "加入追蹤"
                vendor.subscribe_number -= 1
                vendor.save()
            else:
                subscribe = "已追蹤"
                vendor.subscribe_number += 20
                vendor.save()
    else:
        subscribe = "尚未登入"
    return JsonResponse({'subscribe': subscribe})

def course_list(request):
    catagory = Catagory.objects.all()

    context = {
    'catagory':catagory,
    }

    return render(request, 'course_list.html', context)

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    all_available_time = course.availabletime_set.all()
    course_media = course.coursemedia_set.all()
    materials = course.material_set.all()
    googlemap_api_key = os.environ["GOOGLE_API_KEY"]

    gte_date = course.availabletime_set.filter(date__gte=datetime.now())[:3]

    form = OrderingForm()
    # form.fields['material'].queryset = materials
    form.fields['available_time'].queryset = all_available_time

    if request.method == "GET" and request.is_ajax():
        material_data = request.GET.get('material', '').split(" ")[0]
        material_price = materials.filter(name=material_data)[0].price

        price = request.GET.get('price', '')
        total = int(price) + int(material_price)

        return JsonResponse({'total':total})

    if request.method == "POST":
        form = OrderingForm(request.POST)
        if form.is_valid():
            material_price = form.cleaned_data['material'].price
            instance = form.save(commit=False)
            instance.user = request.user
            instance.vendor = course.vendor
            instance.course = course
            instance.total_amount = course.price + material_price
            instance.save()

            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            form = OrderingForm(request.POST)
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


    context = {
    'ordering': ordering,
    }

    return render(request, 'ordering_detail.html', context)

@login_required
def create_user_profile(request):
    form = UserProfileForm()
    if request.user.userprofile:
        if request.GET.get('next',''):
            return HttpResponseRedirect(request.GET.get('next',''))
        else:
            return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            if request.GET.get('next',''):
                return HttpResponseRedirect(request.GET.get('next',''))
            else:
                return HttpResponseRedirect(reverse('user_profile'))
    context = {
        'form': form,
    }

    return render(request, 'create_user_profile.html', context)

@login_required
def edit_user_profile(request):
    form = UserProfileForm(instance=UserProfile.objects.get(user=request.user))
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect(request.GET.get('next',''))
    context = {
        'form': form,
    }

    return render(request, 'edit_user_profile.html', context)

@login_required
def user_profile(request):
    user = request.user
    ordering = user.ordering_set.all()
    subscribe = user.usersubscribe_set.all()

    if not UserProfile.objects.filter(user=user):
        return HttpResponseRedirect(reverse('create_user_profile'))


    context = {
        'user': user,
        'ordering': ordering,
        'subscribe': subscribe,
    }

    return render(request, 'user_profile.html', context)
