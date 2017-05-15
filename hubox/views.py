from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import os
from hubox.settings import BASE_DIR
from django.core.mail import send_mail


def about(request):
    return render(request, 'about.html', {})

def join(request):
    if request.method == "POST":
        company_name = request.POST.get('company-name', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        if name and email and phone and message:
            with open(os.path.join(BASE_DIR, 'templates') + '/join.txt', 'w') as content:
                content.write("公司名稱：{}\n聯絡人姓名：{}\n信箱：{}\n電話：{}\n要說的話：\n{}".format(company_name, name, email, phone, message))
            file = open(os.path.join(BASE_DIR, 'templates') + '/join.txt', 'r')
            content = file.read()

            to_mail = ['ethan@hubox.life', 'frank@hubox.life']
            # to_mail = ['miwooro@hotmail.com']
            send_mail(
                '成為合作夥伴',
                content,
                'Hubox哈盒子',
                to_mail,
                fail_silently=False,
            )
    return render(request, 'join.html', {})

def member_terms(request):
    pass

def privacy_policy(request):
    pass
