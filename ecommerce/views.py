from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Vendor, Course, Catagory, Ordering, IndexEdit
from .forms import OrderingForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
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
    print (settings.BASE_DIR)
    print (settings.STATIC_ROOT)

    course = get_object_or_404(Course, pk=pk)
    course_media = course.coursemedia_set.all()
    available_time = course.availabletime_set.all()
    materials = course.material_set.all()
    googlemap_api_key = os.environ["GOOGLE_API_KEY"]

    form = OrderingForm()
    form.fields['material'].queryset = materials
    form.fields['available_time'].queryset = available_time

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
            form.fields['available_time'].queryset = available_time

    context = {
    'course':course,
    'course_media':course_media,
    'available_time':available_time,
    'materials':materials,
    'form':form,
    'googlemap_api_key': googlemap_api_key,
    }

    return render(request, 'course_detail.html', context)

def ordering_detail(request, pk):
    ordering = get_object_or_404(Ordering, pk=pk)


    context = {
    'ordering': ordering,
    }

    return render(request, 'ordering_detail.html', context)
