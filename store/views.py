from django.shortcuts import render
from .models import *

from django.http import JsonResponse
import json
import datetime
from .forms import ContactForm
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . utils import cookieCart, cartData, guestOrder

# Create your views here.


def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'cartItems':cartItems}
    return render(request, 'store/home.html', context)

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    product = Product.objects.all()
    totalproducts = product.count()

    category_filter = request.GET.get('category', None)
    if category_filter == 'all_cats':
        pass
    elif category_filter == 'loafers':
        product = product.filter(category='Loafers')
    elif category_filter == 'peshawari':
        product = product.filter(category='Peshawari')
    elif category_filter == 'formal':
        product = product.filter(category='Formal Shoes')
    elif category_filter == 'khussa':
        product = product.filter(category='Khussa')
    elif category_filter == 'heels':
        product = product.filter(category='High Heels')
    


    # page = request.GET.get('page', 1)
    # paginator = Paginator(product, 3)
    # try:
    #     product = paginator.page(page)
    # except PageNotAnInteger:
    #     product = paginator.page(1)
    # except EmptyPage:
    #     product = paginator.page(paginator.num_pages)

    
    context = {'products':products, 'cartItems':cartItems,'product':product, 'totalproducts':totalproducts,}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'store/checkout.html', context)

def aboutus(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']
    context = {'cartItems':cartItems}
    return render(request, 'store/aboutus.html', context)

def contactus(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            email_content = get_template('store/email_template.html').render({
                'name': name,
                'phone_number': phone_number,
                'email': email,
                'message': message,
            })

            plain_email_content = strip_tags(email_content)

            send_mail(
                f"Contact Form Submission from {name}",
                plain_email_content,
                "arvikamran@gmail.com",
                ["hamzaarif1807@gmail.com"],
                html_message=email_content,
                fail_silently=False,
            )
            return render(request, 'store/contactus.html', {'form':form, 'success':True})
    else:
        form = ContactForm()

    context = {'cartItems':cartItems, 'form':form,'success':False}
    return render(request, 'store/contactus.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('Action:', action)
    # print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

        

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete', safe=False)