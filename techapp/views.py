from django.shortcuts import render,get_object_or_404
from .models import Product
from .models import CartItem

# Create your views here.

from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

    

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template('contact.html')
    return HttpResponse(template.render())

# def user(request):
#     template = loader.get_template('user_page.html')
#     return HttpResponse(template.render())

def user(request):
    if request.user.is_authenticated:
        print(f"Authenticated user: {request.user}")
    else:
        print("User is not authenticated.")
    return render(request, 'user_page.html')



def address(request):
    template = loader.get_template('address_page.html')
    return HttpResponse(template.render())

def orders(request):
    template = loader.get_template('orders_page.html')
    return HttpResponse(template.render())

def watch(request):
    template = loader.get_template('smartwatch.html')
    return HttpResponse(template.render())

def headphone(request):
    template = loader.get_template('headphone.html')
    return HttpResponse(template.render())

def speaker(request):
    template = loader.get_template('speaker.html')
    return HttpResponse(template.render())

def joystick(request):
    template = loader.get_template('joystick.html')
    return HttpResponse(template.render())

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# from.forms import SignupForm
from django.contrib.auth.hashers import make_password
from .forms import SignupForm
from django.contrib import messages



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(username=first_name, email=email)
            user.set_password(password)
            user.save()
            return redirect('user_login')  # Redirecting to the login page
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm  # Make sure LoginForm is defined in forms.py

def user_login(request):
    error_message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Retrieve the user object using the email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            # Authenticate with the username (not email) and password
            if user is not None:
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("index")  # Replace 'index' with your desired redirect URL
                else:
                    error_message = "Invalid email or password."
            else:
                error_message = "Invalid email or password."
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error_message": error_message})



from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactDetail

def contact_view(request):
    if request.method == 'POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contactlist')
        
    else:
        form=ContactForm()
    
    return render(request, 'contact.html', {'form':form})

def contactlist(request):
    detail=ContactDetail.objects.all()
    return render(request, 'contact.html', {'detail':detail})




   
def shop(request):
    gadgets=Product.objects.all()
    return render(request,'product-single.html',{'gadgets':gadgets})


def product_detail(request, product_id):
    thing=get_object_or_404(Product,pk=product_id)
    return render(request,'gadget_detail.html',{'thing':thing})

from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.total() for item in cart_items)
    return render(request, 'cart_page.html',{'cart_items':cart_items, 'total_quantity':total_quantity, 'total_price':total_price})   
    
from django.contrib import messages
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created =CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item =get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
    return redirect('cart')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, CartItem, BillingDetails, Order, OrderItem
from .forms import BillingDetailsForm

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.total() for item in cart_items)
    
    if total_quantity == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Check if billing details already exist for the user
    billing_details = BillingDetails.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = BillingDetailsForm(request.POST, instance=billing_details)
        if form.is_valid():
            billing_details = form.save(commit=False)  # Save without committing to DB yet
            billing_details.user = request.user  # Ensure the user field is set
            billing_details.save()  # Save the instance with the user field set
    #         messages.success(request, 'Billing details updated successfully!')
    #         return redirect('order_summary')  # Redirect to order summary or payment page
    # else:
    #     form = BillingDetailsForm(instance=billing_details)
            cart_items = CartItem.objects.filter(user =request.user)
            total_price = sum(item.total() for item in cart_items)
            total_quantity = sum(item.quantity for item in cart_items)
            
            # create the order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                total_quantity=total_quantity,
                shipping_address=billing_details.address,
            )
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            
            # CartItem.objects.filter(user=request.user).delete()
            
            messages.success(request, 'Billing details updatedand order placed Succesfully!')
            return redirect ('order_summary', order_id=order.id)
    else:
        form = BillingDetailsForm(instance=billing_details)
            
    return render(request, 'checkout_page.html', {
        'cart_items': cart_items, 
        'total_quantity': total_quantity, 
        'total_price': total_price,
        'form': form
    })


@login_required
def order_summary(request, order_id):
    order =Order.objects.filter(id=order_id, user=request.user).first()
    if not order:
        messages.error(request, 'Order not found.')
        return redirect('cart')
    order_items =OrderItem.objects.filter(order=order)
    
    total_quantity = sum(item.quantity for item in order_items)
    total_price = sum(item.total() for item in order_items)
    
    order_items_with_names =[
        {
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price,
            'total':item.quantity * item.price
        }
        for item in order_items
    ]
    
    return render(request, 'order_summary.html', {
        'order': order,
        'order_items': order_items, 
        'total_quantity': total_quantity, 
        'total_price': total_price
    })
    
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('order_date')
    
    return render(request, "order_history.html",{
        'orders':orders
    })
    
    
    
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Order  # Adjust the import based on your project structure

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def razorpay_payment(request):
    if request.method == 'POST':
        try:
            # Get order details
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            total_price = order.total_price  # Ensure this field exists in your model

            # Razorpay amount should be in paise
            amount_in_paise = int(total_price * 100)

            # Create Razorpay order
            razorpay_order = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1  # Auto-capture after payment
            })

            # Save Razorpay order ID to your database (optional)
            order.razorpay_order_id = razorpay_order['id']
            order.save()

            # Return Razorpay order details to the frontend
            return JsonResponse({
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': amount_in_paise,
                'currency': "INR"
            })

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    return JsonResponse({'error': 'Invalid Request'}, status=400)
    

