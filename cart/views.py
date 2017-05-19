from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import JsonResponse

from .models import Cart, CartItem
from .forms import CartItemForm
from ecommerce.models import Voucher
# Create your views here.

def cart(request):
    cart = ''
    request.session.set_expiry(0)
    cart_pk = request.session.get("cart_pk")
    if cart_pk == None:
        cart = Cart.objects.create()
        cart_pk = cart.pk
        request.session["cart_pk"] = cart_pk
    cart = Cart.objects.get(pk=cart_pk)
    if request.user.is_authenticated():
        cart.user = request.user
        cart.save()

    if request.method == "POST":
        form = CartItemForm(request.POST)
        if form.is_valid():
            available_time = form.cleaned_data['available_time']
            participants_number = form.cleaned_data['participants_number']
            cart_item = CartItem.objects.get_or_create(cart=cart, available_time=available_time)[0]
            cart_item.participants_number = participants_number
            cart_item.save()

        if request.POST.get('delete', '') and request.is_ajax():
            delete_pk = request.POST.get('delete', '')
            delete_item = CartItem.objects.get(pk=delete_pk)
            update_total = cart.total - delete_item.item_total
            delete_item.delete()

            return JsonResponse({'update_total':update_total})

    if request.is_ajax() and request.POST.get('voucher', ''):
        serial_number = request.POST.get('voucher', '')
        try:
            voucher = Voucher.objects.get(serial_number=serial_number)
            if voucher.aply == True:
                return JsonResponse({"data":"applied"})
            else:
                cart.voucher = voucher
                cart.save()
            return JsonResponse({"data":voucher.price})
        except:
            return JsonResponse({"data":"error"})

    if request.is_ajax() and request.POST.get('data', '') == "delete_voucher":
        cart.voucher = None
        cart.save()
        return JsonResponse({"data":"delete_voucher"})

    context = {
        'cart': cart
    }
    return render(request, "cart.html", context)


def check_out(request):
    user_auth = ''
    cart_pk = request.session.get("cart_pk")
    if cart_pk == None:
        return(reverse('cart'))
    cart = Cart.objects.get(pk=cart_pk)

    if not request.user.is_authenticated():
        user_auth = False

    context = {
     'cart': cart,
     'user_auth': user_auth,
    }

    return render(request, "check_out.html", context)

def cart_item_count(request):
    if request.is_ajax():
        cart_pk = request.session.get("cart_pk")
        if cart_pk == None:
            count = 0
        else:
            cart = Cart.objects.get(pk=cart_pk)
            count = len(cart.cartitem_set.all())

        return JsonResponse({"count": count})
    return HttpResponse()
