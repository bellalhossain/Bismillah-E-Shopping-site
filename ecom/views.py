from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from ecommerce.settings import EMAIL_HOST_USER
from django.conf import settings
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

def home(request):
    items=models.Item.objects.all()
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        productcounter=itemid.split('|')
        item_count_insidecart=len(set(productcounter))
    else:
        item_count_insidecart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'ecom/customer_home.html', {'items':items, 'item_count_insidecart':item_count_insidecart})


#for showing login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def consumer_signup_view(request):
    AdminForm=forms.consumer_user_form()
    consumerForm=forms.ConsumerForm()
    mydict={'AdminForm':AdminForm,'consumerForm':consumerForm}
    if request.method=='POST':
        AdminForm=forms.consumer_user_form(request.POST)
        consumerForm=forms.ConsumerForm(request.POST, request.FILES)
        if AdminForm.is_valid() and consumerForm.is_valid():
            user=AdminForm.save()
            user.set_password(user.password)
            user.save()
            customer=consumerForm.save(commit=False)
            customer.user=user
            customer.save()
            customer_group = Group.objects.get_or_create(name='CUSTOMER')
            customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'ecom/customersignup.html',context=mydict)

def is_consumer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_consumer(request.user):
        return redirect('consumer-home')
    else:
        return redirect('admin-dashboard')


@login_required(login_url='adminlogin')
def admin_dashboard(request):

    customercount=models.Consumer.objects.all().count()
    itemcount=models.Item.objects.all().count()
    ordercount=models.ConsumerOrder.objects.all().count()

    orders=models.ConsumerOrder.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Item.objects.all().filter(id=order.item.id)
        ordered_by=models.Consumer.objects.all().filter(id = order.consumer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'itemcount':itemcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'ecom/admin_dashboard.html',context=mydict)


@login_required(login_url='adminlogin')
def view_consumer(request):
    consumers=models.Consumer.objects.all()
    return render(request,'ecom/view_customer.html', {'consumers':consumers})

# admin delete consumer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    consumer=models.Consumer.objects.get(id=pk)
    user=models.User.objects.get(id=consumer.user_id)
    user.delete()
    consumer.delete()
    return redirect('view-consumer')


@login_required(login_url='adminlogin')
def update_view_of_consumer(request, pk):
    consumer=models.Consumer.objects.get(id=pk)
    user=models.User.objects.get(id=consumer.user_id)
    userForm=forms.consumer_user_form(instance=user)
    consumer_form=forms.ConsumerForm(request.FILES, instance=consumer)
    mydict={'userForm':userForm,'consumer_form':consumer_form}
    if request.method=='POST':
        userForm=forms.consumer_user_form(request.POST, instance=user)
        consumer_form=forms.ConsumerForm(request.POST, instance=consumer)
        if userForm.is_valid() and consumer_form.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            consumer_form.save()
            return redirect('view-consumer')
    return render(request,'ecom/admin_update_customer.html',context=mydict)

@login_required(login_url='adminlogin')
def view_of_admin_item(request):
    items=models.Item.objects.all()
    return render(request,'ecom/admin_products.html',{'items':items})

@login_required(login_url='adminlogin')
def admin_add_item(request):
    countitem=models.Item.object.count
    itemForm=forms.ItemForm()
    if request.method=='POST':
        itemForm=forms.ItemForm(request.POST, request.FILES)
        if itemForm.is_valid():
            itemForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'ecom/admin_add_products.html',{'itemForm':itemForm,'countitem':countitem})


@login_required(login_url='adminlogin')
def delete_item_view(request, pk):
    item=models.Item.objects.get(id=pk)
    item.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_item_view(request, pk):
    item=models.Item.objects.get(id=pk)
    itemsForm=forms.ItemForm(instance=item)
    if request.method=='POST':
        itemsForm=forms.ItemForm(request.POST, request.FILES, instance=item)
        if itemsForm.is_valid():
            itemsForm.save()
            return redirect('admin-products')
    return render(request,'ecom/admin_update_product.html',{'itemsForm':itemsForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    consumerorders=models.ConsumerOrder.objects.all()
    ordered_products=[]
    consumerordered_bys=[]
    for order in consumerorders:
        ordered_item=models.Item.objects.all().filter(id=order.item.id)
        ordered_by=models.Consumer.objects.all().filter(id = order.consumer.id)
        ordered_products.append(ordered_item)
        consumerordered_bys.append(ordered_by)
    return render(request,'ecom/admin_view_booking.html',{'data':zip(ordered_products,consumerordered_bys,consumerorders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.ConsumerOrder.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')


@login_required(login_url='adminlogin')
def update_order_status(request, pk):
    consumerorder=models.ConsumerOrder.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=consumerorder)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=consumerorder)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'ecom/update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def feedback_view(request):
    consumerfeedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'consumerfeedbacks':consumerfeedbacks})


def search_view(request):

    query = request.GET['query']
    items=models.Item.objects.all().filter(name__icontains=query)
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        counter=itemid.split('|')
        item_count_insidecart=len(set(counter))
    else:
        item_count_insidecart=0

    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home.html',{'items':items,'word':word,'item_count_insidecart':item_count_insidecart})
    return render(request,'ecom/index.html',{'items':items,'word':word,'item_count_insidecart':item_count_insidecart})


# any one can add item to cart, no need of signin
def add_to_cart_view(request,pk):
    items=models.Item.objects.all()

    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        counter=itemid.split('|')
        item_count_insidecart=len(set(counter))
    else:
        item_count_insidecart=1

    res = render(request, 'ecom/index.html',{'items':items,'item_count_insidecart':item_count_insidecart})

    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        if itemid=="":
            itemid=str(pk)
        else:
            itemid=itemid+"|"+str(pk)
        res.set_cookie('itemid', itemid)
    else:
        res.set_cookie('itemid', pk)

    items=models.Item.objects.get(id=pk)
    messages.info(request, items.name + ' added to cart successfully!')

    return res

@login_required(login_url='customerlogin')
def cart(request):
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        counter=itemid.split('|')
        item_count_insidecart=len(set(counter))
    else:
        item_count_insidecart=0

    items=None
    total=0
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        if itemid != "":
            item_count_insidecart=itemid.split('|')
            items=models.Item.objects.all().filter(id__in = item_count_insidecart)

            for p in items:
                total=total+p.price
    return render(request,'ecom/cart.html',{'items':items,'total':total,'item_count_insidecart':item_count_insidecart})

@login_required(login_url='customerlogin')
def delete_cart(request, pk):
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        counter=itemid.split('|')
        item_count_insidecart=len(set(counter))
    else:
        item_count_insidecart=0

    total=0
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        item_id_insidecart=itemid.split('|')
        item_id_insidecart=list(set(item_id_insidecart))
        item_id_insidecart.remove(str(pk))
        items=models.Item.objects.all().filter(id__in = item_id_insidecart)
        for p in items:
            total=total+p.price

        #  for update coookie value after removing item id in cart
        value=""
        for i in range(len(item_id_insidecart)):
            if i==0:
                value=value+item_id_insidecart[0]
            else:
                value=value+"|"+item_id_insidecart[i]
        res = render(request, 'ecom/cart.html',{'items':items,'total':total,'item_count_insidecart':item_count_insidecart})
        if value=="":
            res.delete_cookie('itemid')
        res.set_cookie('itemid',value)
        return res


def send_feedback_view(request):
    feedbackForm=forms.Form_of_Feedback()
    if request.method == 'POST':
        feedbackForm = forms.Form_of_Feedback(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'ecom/send_feedback.html', {'feedbackForm':feedbackForm})


@login_required(login_url='customerlogin')
@user_passes_test(is_consumer)
def consumer_home(request):
    items=models.Item.objects.all()
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        counter=itemid.split('|')
        item_count_insidecart=len(set(counter))
    else:
        item_count_insidecart=0
    return render(request,'ecom/index.html',{'items':items,'item_count_insidecart':item_count_insidecart})

@login_required(login_url='customerlogin')
def consumer_address(request):
    item_inside_cart=False
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        if itemid != "":
            item_inside_cart=True
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        counter=itemid.split('|')
        item_count_insidecart=len(set(counter))
    else:
        item_count_insidecart=0

    Address_form = forms.form_of_address()
    if request.method == 'POST':
        Address_form = forms.form_of_address(request.POST)
        if Address_form.is_valid():
            email = Address_form.cleaned_data['Email']
            mobile=Address_form.cleaned_data['Mobile']
            address = Address_form.cleaned_data['Address']
            total=0
            if 'itemid' in request.COOKIES:
                itemid = request.COOKIES['itemid']
                if itemid != "":
                    item_id_insidecart=itemid.split('|')
                    products=models.Item.objects.all().filter(id__in = item_id_insidecart)
                    for p in products:
                        total=total+p.price

            res = render(request, 'ecom/payment.html',{'total':total})
            res.set_cookie('email',email)
            res.set_cookie('mobile',mobile)
            res.set_cookie('address',address)
            return res
    return render(request,'ecom/customer_address.html',{'Address_form':Address_form,'item_inside_cart':item_inside_cart,'item_count_insidecart':item_count_insidecart})


@login_required(login_url='customerlogin')
def payment_view(request):
    consumer=models.Consumer.objects.get(user_id=request.user.id)
    items=None
    email=None
    mobile=None
    address=None
    if 'itemid' in request.COOKIES:
        itemid = request.COOKIES['itemid']
        if itemid != "":
            item_id_insidecart=itemid.split('|')
            items=models.Item.objects.all().filter(id__in = item_id_insidecart)
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']

    for product in items:
        models.ConsumerOrder.objects.get_or_create(consumer=consumer, item=product, status='Pending', email=email, mobile=mobile, address=address)

    # after order placed cookies should be deleted
    res = render(request,'ecom/payment_success.html')
    res.delete_cookie('itemid')
    res.delete_cookie('email')
    res.delete_cookie('mobile')
    res.delete_cookie('address')
    return res




@login_required(login_url='customerlogin')
@user_passes_test(is_consumer)
def consumer_order_view(request):
    consumer=models.Consumer.objects.get(user_id=request.user.id)
    consumerorders=models.ConsumerOrder.objects.all().filter(consumer_id = consumer)
    ordered_products=[]
    for order in consumerorders:
        ordered_item=models.Item.objects.all().filter(id=order.item.id)
        ordered_products.append(ordered_item)

    return render(request,'ecom/my_order.html',{'data':zip(ordered_products,consumerorders)})


def direct_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_consumer)
def get_invoice_view(request, orderID, productID):
    consumerorder=models.ConsumerOrder.objects.get(id=orderID)
    product=models.Item.objects.get(id=productID)
    mydict={
        'orderDate':consumerorder.order_date,
        'customerName':request.user,
        'customerEmail':consumerorder.email,
        'customerMobile':consumerorder.mobile,
        'shipmentAddress':consumerorder.address,
        'orderStatus':consumerorder.status,

        'productName':product.name,
        'productImage':product.product_image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return direct_to_pdf('ecom/download_invoice.html', mydict)






@login_required(login_url='customerlogin')
@user_passes_test(is_consumer)
def consumer_profile_view(request):
    consumer=models.Consumer.objects.get(user_id=request.user.id)
    return render(request,'ecom/my_profile.html',{'consumer':consumer})


@login_required(login_url='customerlogin')
@user_passes_test(is_consumer)
def edit_profile(request):
    consumer=models.Consumer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=consumer.user_id)
    userForm=forms.consumer_user_form(instance=user)
    consumerForm=forms.ConsumerForm(request.FILES, instance=consumer)
    mydict={'userForm':userForm,'consumerForm':consumerForm}
    if request.method=='POST':
        userForm=forms.consumer_user_form(request.POST, instance=user)
        consumerForm=forms.ConsumerForm(request.POST, instance=consumer)
        if userForm.is_valid() and consumerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            consumerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/edit_profile.html',context=mydict)



def aboutus(request):
    return render(request,'ecom/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'ecom/contactussuccess.html')
    return render(request, 'ecom/contactus.html', {'form':sub})

def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to our shop'
        message = 'You have successfully subscribed'
        recepient = str(sub['Email'].value())
        send_mail(subject,
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'ecom/index.html')
    return render(request, 'ecom/subscribe.html', {'form':sub})