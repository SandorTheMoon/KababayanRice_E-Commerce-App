from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum
from django.db.models import Count
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from .forms import RegistrationForm, AccountForm,EditProfileForm, ShippingAddressForm, ProductForm, CheckoutForm
from .models import Product, CartItem, Account, Order, ShippingAddress

# Create your views here.
def welcome_page(request):
    return render(request, "UsersAuthentication/welcome.html")


@login_required(login_url="/login/")
def home_page(request):
    products = Product.objects.all()
    return render(request, 'Home/Home.html', {'products': products })
    # return render(request, "Home/Home.html")


@login_required(login_url="/login/")
def product_page(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "Home/productpage.html", {'product': product})


def login_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home')
            
            else:
                messages.error(request, 'Invalid email or password.', extra_tags='login_error')

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        return render(request, 'UsersAuthentication/login.html')


def signup_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signup')
    else:
        if request.method == 'POST':
            user_form = RegistrationForm(request.POST, request.FILES)
            shipping_address_form = ShippingAddressForm(request.POST)

            if user_form.is_valid() and shipping_address_form.is_valid():
                user = user_form.save()  # Save the user instance
                profile_picture = user_form.cleaned_data['profile_picture']
                profile = Account(user=user, profile_picture=profile_picture)
                profile.save()

                shipping_address = shipping_address_form.save(commit=False)
                shipping_address.account = user
                shipping_address.save()
                return redirect('login')
            else:
                messages.error(request, 'Fill out the necessary informations.')
        else:
            user_form = RegistrationForm()
            shipping_address_form = ShippingAddressForm()

        return render(request, 'UsersAuthentication/signup.html', {'user_form': user_form, 'shipping_address_form': shipping_address_form})


@login_required(login_url="/login/")
def logout_account(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    

@login_required(login_url="/login/")
def editprofile_page(request):
    current_user = request.user
    shipping_address = current_user.shippingaddress_set.first()

    user_form = EditProfileForm(instance=current_user)
    address_form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        user_form = EditProfileForm (request.POST, instance=current_user)
        address_form = ShippingAddressForm(request.POST, instance=shipping_address)

        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            login(request, current_user)
            return redirect('profile')
        
        else:

            print("not valid")
            print("User Form Errors:")
            for field, errors in user_form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")

            print("Address Form Errors:")
            for field, errors in address_form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
    
    else:
        user_form = EditProfileForm(instance=current_user)
        address_form = ShippingAddressForm(instance=shipping_address)

    return render(request, 'Profile/editprofile.html', {'user_form': user_form, 'address_form': address_form})


def navbarAndfooter(request):
    return render(request, "Home/navbarAndfooter.html")


@login_required(login_url="/login/")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if the product is already in the cart
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()
    
    if cart_item:
        # If the product is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If the product is not in the cart, create a new cart item
        CartItem.objects.create(user=request.user, product=product, quantity=1)
    
    return redirect('cart')


@login_required(login_url="/login/")
def cart_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)
    return render(request, "Home/cart.html", {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url="/login/")
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url="/login/")
def update_cart(request):
    if request.method == 'POST':
        for item in request.user.cartitem_set.all():
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity is not None:
                item.quantity = int(quantity)
                item.save()
                print("saved")
            
            print("found item")
        
        print("method posted")
    
    print("no method")
    return redirect('cart')


@login_required(login_url="/login/")
def checkout_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)
    return render(request, "Checkout/checkout.html", {'total_price': total_price, 'user': request.user})

@login_required(login_url="/login/")
def ordersummary_page(request):
    if request.method == 'POST':
        # Process user information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Process payment method
        payment_method = request.POST.get('payment_method')

        # Process card details if card payment selected
        if payment_method == 'card_payment':
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')

        # Process order
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.product_price * item.quantity for item in cart_items)

        if payment_method in ['cash_on_delivery', 'card_payment']:
            # Create an order for each item in the cart
            for item in cart_items:
                seller_account = Account.objects.get(user=item.product.account)
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.product.product_price * item.quantity,
                    payment_method=payment_method,
                    seller=seller_account
                )
            cart_items.delete()  # Empty the cart after checkout
            messages.success(request, 'Order placed successfully!')
            return redirect('home')

    # If GET request or form submission fails, render the checkout page with cart items
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)
    
    return render(request, 'Checkout/ordersummary.html', {'cart_items': cart_items, 'total_price': total_price, 'user': request.user})

@login_required(login_url="/login/")
def profile_page(request):
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    
    else:
        return render(request, "Home/profile.html")


@login_required(login_url="/login/")
def addproduct_page(request):
    if request.method == 'POST':
        add_product_form = ProductForm(request.POST, request.FILES)

        if add_product_form.is_valid():
            print("product saved")
            add_product_form.instance.account = request.user
            add_product_form.save()
            return redirect('profile')
        else:
            print("product not saved due to invalid form")
    else:
        add_product_form = ProductForm()
        print("GET request, product form initialized")

    return render(request, 'Profile/addproduct.html', {'add_product_form': add_product_form})


login_required(login_url="/login/")
def my_orders(request):
    user_orders = Order.objects.filter(user=request.user)

    return render(request, 'Profile/my_orders.html', {'user_orders': user_orders})


@login_required(login_url="/login/")
def seller_orders(request):
    seller_account = request.user.account
    
    # Get all orders where the current user is the seller
    seller_orders = Order.objects.filter(seller=seller_account)

    return render(request, 'Profile/seller_orders.html', {'seller_orders': seller_orders})

@login_required(login_url="/login/")
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user_shipping_address = ShippingAddress.objects.get(account=order.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, 'Order status updated successfully!')
        return redirect('order_details', order_id=order_id)
    
    return render(request, 'Profile/order_details.html', {'order': order, 'user_shipping_address': user_shipping_address})


@login_required(login_url="/login/")
def seller_analytics(request):
    seller_account = request.user.account

    # Fetch order data
    total_orders = Order.objects.filter(seller=seller_account).count()
    orders_to_pack = Order.objects.filter(seller=seller_account, status=1).count()
    orders_to_ship = Order.objects.filter(seller=seller_account, status=2).count()
    orders_to_deliver = Order.objects.filter(seller=seller_account, status=3).count()

    # Data for the pie chart (excluding total products)
    data = [orders_to_pack, orders_to_ship, orders_to_deliver]
    labels = ['Orders to Pack', 'Orders to Ship', 'Orders to Deliver']
    colors = ['#FF6384', '#36A2EB', '#FFCE56']

    # Handle cases where all data is zero
    if sum(data) == 0:
        data = [1, 1, 1]  # Ensure at least minimal non-zero data
        labels = ['No Orders', 'No Orders', 'No Orders']

    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors, textprops={'fontsize': 16})
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Save it to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    # Encode the BytesIO object in base64 and pass it to the template
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    context = {
        'image_base64': image_base64,
        'total_orders': total_orders,
        'orders_to_pack': orders_to_pack,
        'orders_to_ship': orders_to_ship,
        'orders_to_deliver': orders_to_deliver,
    }

    return render(request, 'Profile/seller_analytics.html', context)