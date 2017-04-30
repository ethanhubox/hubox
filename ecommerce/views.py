from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from .models import Vendor, Course, Catagory, Ordering, IndexEdit, AvailableTime
from .forms import OrderingForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from datetime import datetime
from itertools import chain
import os
# Create your views here.

def index(request):
    vendor = Vendor.objects.all().order_by('?')
    course = Course.objects.all().order_by('?')
    catagory = Catagory.objects.all().order_by('?')[:3]
    # index = IndexEdit.objects.get(pk="1")
    try:
        index = IndexEdit.objects.get(pk="1")
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


    context = {
    'vendor':vendor,
    'vendor_medias':vendor_medias,
    'courses':courses,

    }

    return render(request, 'vendor_detail.html', context)

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


    gte_date = course.availabletime_set.filter(date__gte=datetime.now())[:5]



    form = OrderingForm()
    form.fields['material'].queryset = materials
    form.fields['available_time'].queryset = gte_date

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
            form.fields['material'].queryset = materials
            form.fields['available_time'].queryset = gte_date

    context = {
    'course':course,
    'course_media':course_media,
    'gte_date':gte_date,
    'materials':materials,
    'form':form,
    'googlemap_api_key': googlemap_api_key,
    }

    return render(request, 'course_detail.html', context)

def datepicker_ajax(request):
    if request.is_ajax() and request.method == "GET":
        pk = request.GET.get('pk', '')
        data = request.GET.get('date', '')
        course = get_object_or_404(Course, pk=pk)
        available_time = list(course.availabletime_set.filter(format_date=data))
        print(available_time)

    return JsonResponse({"d": 'df'})

def ordering_detail(request, pk):
    ordering = get_object_or_404(Ordering, pk=pk)


    context = {
    'ordering': ordering,
    }

    return render(request, 'ordering_detail.html', context)
