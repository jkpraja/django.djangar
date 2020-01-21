from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, StockForm
from .models import Stock

# Create your views here.
# homapage view
def home(request):
    import requests
    import json

    #Grab crypto
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,DBC,XRP,ETH,MIOTA,ADA&tsyms=USD")
    price = json.loads(price_request.content)

    #Grab stocks
    #pk_062031d20883444f9ea74e2610fe2011
    stocks_data = Stock.objects.all()
    stock_list = []
    for stock_item in stocks_data:
        stock_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(stock_item) + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
        try:
            stock = json.loads(stock_request.content)
            stock_list.append(stock)
        except Exception as e:
            stock = "Error..."


    #Grab crypto news
    api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang-EN")
    api = json.loads(api_request.content)
    return render(request, "home.html", {'api': api, 'price': price, 'stock': stock_list})

# aboutus view
def about(request):
    from pages.namer import naming
    return render(request, "about.html", {"aboutName": naming})

# login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect("home")
        else:
            messages.success(request, ('Error! Please try again!'))
            return redirect("login_user")
    else:
        return render(request, "login.html", {})

# logout view
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, ('You have been logged out!'))
        return redirect("login_user")
    else:
        return redirect("home")

# register view
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been registered!'))
            return redirect("home")
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, "register.html", context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your Profile has been successfully updated!'))
            return redirect("home")
    else:
        form = EditProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, "edit_profile.html", context)

def change_passwd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your Password has been successfully edited!'))
            return redirect("home")
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {'form': form}
    return render(request, "change_password.html", context)

def prices(request):
    import requests
    import json
    if request.method == "POST":
        quote = request.POST['quote']
        quote.upper()
        #Grab crypto
        crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+ quote +"&tsyms=USD")
        crypto = json.loads(crypto_request.content)
        return render(request, 'prices.html', {'quote':quote, 'crypto':crypto})
    else:
        return render(request, "prices.html", {})

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect("add_stock")
        else:
            stocks = Stock.objects.all()
            return render(request, "add_stock.html", {'stocks': stocks}) 
    else:
        stocks = Stock.objects.all()
        return render(request, "add_stock.html", {'stocks': stocks})

def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success( request, ("Stock Has Been Removed!"))
    return redirect(add_stock)
