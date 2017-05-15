from django.shortcuts import render
from .models import MemberTerms, PrivacyPolicy, FAQ

# Create your views here.
def member_terms(request):
    try:
        member_terms = MemberTerms.objects.all()[0]
    except:
        member_terms = ''
    context = {
        'member_terms':member_terms,
    }
    return render(request, 'member_terms.html', context)

def privacy_policy(request):
    try:
        privacy_policy = PrivacyPolicy.objects.all()[0]
    except:
        privacy_policy = ''
    context = {
        'privacy_policy':privacy_policy,
    }

    return render(request, 'privacy_policy.html', context)

def faq(request):
    try:
        faq = FAQ.objects.all()[0]
    except:
        faq = ''
    context = {
        'faq':faq,
    }

    return render(request, 'faq.html', context)
