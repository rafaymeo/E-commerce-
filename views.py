from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import User
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Customer
from django.contrib import messages

def index_view(request):
    return render(request,'index.html')

def home_view(request):
    return render(request, 'index.html')  # your home page

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        raw_password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(raw_password)
        user.save()

        # Create related Customer
        Customer.objects.create(
            user=user,
            username=username,
            email=email,
            password=user.password  # hashed
        )

        return redirect('login')

    return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')



from django.shortcuts import render, redirect

def product_detail_view(request):
    # Extract product info from GET parameters (URL query)
    name = request.GET.get('name')
    price = request.GET.get('price')
    image = request.GET.get('image')

    if not all([name, price, image]):
        return redirect('index')  # fallback if missing data

    context = {
        'name': name,
        'price': price,
        'image': image
    }
    return render(request, 'product.html', context)


# views.py
from django.shortcuts import render

def contact_view(request):
    return render(request, 'contact.html')




from django.shortcuts import render
from .models import Product

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {
        'name': product.name,
        'price': product.price,
        'image': product.image.url
    })

from django.shortcuts import render
from .models import Order

def contact_view(request):
    success_message = None
    if request.method == "POST":
        Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            street_address=request.POST.get('street_address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            payment_method=request.POST.get('payment_method'),
            card_number=request.POST.get('card_number'),
            expiry_date=request.POST.get('expiry_date'),
            cvv=request.POST.get('cvv'),
        )
        success_message = "✅ Order placed successfully!"
    return render(request, "contact.html", {"success_message": success_message})
