from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .forms import ProfileForm
from .models import Subscribe, Profile

from ecommerce.models import Vendor


# Create your views here.

@login_required
def create_profile(request):
    form = ProfileForm()
    try:
        profile = request.user.profile
        if request.GET.get('next',''):
            return HttpResponseRedirect(request.GET.get('next',''))
        else:
            return HttpResponseRedirect(reverse('index'))
    except:
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                if request.GET.get('next',''):
                    return HttpResponseRedirect(request.GET.get('next',''))
                else:
                    return HttpResponseRedirect(reverse('profile'))
    context = {
        'form': form,
    }

    return render(request, 'create_profile.html', context)


@login_required
def profile(request):
    user = request.user
    ordering = user.ordering_set.all()
    subscribe = user.subscribe_set.all()

    if not Profile.objects.filter(user=user):
        return HttpResponseRedirect(reverse('create_profile'))


    context = {
        'user': user,
        'ordering': ordering,
        'subscribe': subscribe,
    }

    return render(request, 'profile.html', context)

def subscribe_ajax(request):
    vendor = get_object_or_404(Vendor, pk=request.POST.get("vendor", 0))
    if request.user.is_authenticated():
        user = request.user
        if request.method == "POST" and request.is_ajax():
            subscribe, created = Subscribe.objects.get_or_create(user=user, vendor=vendor)
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
