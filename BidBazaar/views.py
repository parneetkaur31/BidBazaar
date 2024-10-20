from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from BidBazaar.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
# Create your views here.

def index(request):
    return render(request, "index.html")

# def buy(request):
#     return render(request, "buy.html")

def sell(request):
    listc = Listing.ItemCategory
    print(listc)
    return render(request, "sell.html", {"itemcat":listc})

def contact(request):
    return render(request, "contact.html")

# def sign(request):
#     return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def change_p(request):
    return render(request, "change.html")

def reg_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        
        myuser  = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "Account created succesfully.")
        return redirect('log_form')
    
    return render(request, "register.html")
 

def log_form(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # fname = user.first_name
            # messages.success(request, f'welcome {username} !!')
            return render(request, 'index.html')
        else:
            messages.error(request, "Invalid Credentials!")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def sell_form(request):
    if request.method == "POST":
        name = request.POST.get('item-name')
        desc = request.POST.get('item-desc')
        img = request.FILES.get('item-img')
        category = request.POST.get('item-category')
        base_prize = request.POST.get('item-base')
        incr_prize = request.POST.get('item-incr')
        start_auc = request.POST.get('item-start')
        end_auc =request.POST.get('item-end')

        current_datetime = datetime.now()
        if current_datetime < datetime.strptime(start_auc, '%Y-%m-%dT%H:%M'):
            auc_status = 'UP'
        elif current_datetime > datetime.strptime(end_auc, '%Y-%m-%dT%H:%M'):
            auc_status = 'PA'
        else:
            auc_status = 'AC'

        item = Listing(name=name, desc=desc, img=img, category=category, base_prize=base_prize, incr_prize=incr_prize, start_auc=start_auc, end_auc=end_auc, auc_status=auc_status)
        item.save()
    
    return redirect("sell")

def signout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect('index')


def buy(request):
    mylists = Listing.objects.all()
    
    # Loop through each listing and assign the auction status
    for listing in mylists:
        current_datetime = datetime.now()
        
        start_auc = listing.start_auc.strftime('%Y-%m-%dT%H:%M')
        end_auc = listing.end_auc.strftime('%Y-%m-%dT%H:%M')
        
        if current_datetime < datetime.strptime(start_auc, '%Y-%m-%dT%H:%M'):
            listing.auc_status = 'UP'  # Auction upcoming
        elif current_datetime > datetime.strptime(end_auc, '%Y-%m-%dT%H:%M'):
            listing.auc_status = 'PA'  # Auction passed
        else:
            listing.auc_status = 'AC'  # Auction active

    context = {
        'mylists': mylists,
    }
    
    print(context)
    return render(request, "buy.html", context)

# def buy(request):
#   mylists = Listing.objects.all()

#   context = {
#     'mylists': mylists,
#   }
#   print(context)
#   return render(request, "buy.html", context)


def update_listing(list_id):
    listing = get_object_or_404(Listing, pk=list_id)
    if listing.no_of_bids == 0:
        listing.latest_bid_prize = listing.base_prize
    else:
        listing.latest_bid_prize += listing.incr_prize
    listing.no_of_bids += 1
    listing.save()


def new_bid(request, list_id):
    if request.method == 'GET':
        update_listing(list_id)
        listing = get_object_or_404(Listing, pk=list_id)
        bid_amount = listing.latest_bid_prize
        
        bid_new = Bid(
            user_id = request.user,
            auction_id = listing, 
            bid_amt = int(bid_amount)
        )
        bid_new.save()
    return redirect("buy")

