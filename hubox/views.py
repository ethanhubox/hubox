from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

def about(request):
    return render(request, 'about.html', {})

def join(request):
    return render(request, 'join.html', {})
