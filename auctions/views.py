from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import User

from .models import User, AuctionListing, Bid, Comment
from .forms import AuctionListingForm, CommentForm


def index(request):
    return render(request, "auctions/index.html",{
        "listing": AuctionListing.objects.all().order_by('-created_at')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")
    


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='auctions/login.html')
def create(request):
    return render(request, 'auctions/login.html',{
        'form' : AuctionListingForm
    })

@login_required(login_url='auctions/login.html')
def insert(request):
    form = AuctionListingForm(request.POST)
    if form.is_valid:
        auction = AuctionListing(user=request.user, **form.cleaned_date)
        if not auction.image_url:
            auction.image_url = 'https://images.app.goo.gl/h7sWyqSwujg2qvzN9'
        auction.save()

        starting_bid = auction.starting_bid

        bid = Bid(amount=starting_bid, user=request.user, auction=auction)
        bid.save()
        print("auction" + auction.image_url)

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auction/create/html',{
            'form': form,
            'error': form.errors
        })
    

def listing(request, id):
    current = AuctionListing.objects.get(pk=id)
    bid = get_list_or_404(Bid, auction=current)
    comments = Comment.objects.filter(auction=current)
    print("here:" + AuctionListing.objects.get(pk=id).image_url)
    return render(request, 'auctions/listing.html',{
        'auction': current,
        'user': request.user,
        'bid': bid,
        'comments': comments,
        'comment_form':CommentForm()
    })

@login_required(login_url='auctions/login.html')
def update_bid(request, id):
    amount = request.POST['bid']
    if amount:
        amount = float(amount)
        auction = get_list_or_404(AuctionListing, id=id)
        if amount > get_list_or_404(Bid, id=id).amount:
            bid = get_list_or_404(Bid, id=id)
            bid.user, bid.amount = request.user, amount 
            bid.save()
            auction.bid_counter +=1
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            raise ValidationError('Bid Must be greater than the current bid value')
    else:
        raise ValidationError('Bid Must be greater than current Bid value')
    
@login_required(login_url='auctions/login.html')
def close_bid(request, id):
    auction = get_list_or_404(AuctionListing,id=id)
    auction.active, auction.winner = False, request.user.username
    auction.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='auctions/login.html')
def watchlist(request):
    return render(request, 'auctions/watchlist.html',{
        "watchlist": request.user.watchlist.all()
    })

@login_required(login_url='auctions/login.html')
def watch(request, id):
    auction = get_list_or_404(AuctionListing,id=id)
    request.user.watchlist.add(auction)
    request.user.watchlist_counter +=1
    request.user.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='auctions/login.html')
def unwatch(request, id):
    auction = get_list_or_404(AuctionListing,id=id)
    request.user.watchlist.remove(auction)
    request.user.watchlist_counter -=1
    request.user.save()

    if '/unwatch/' in request.path:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('wishlist'))


def categories(request):
    return render(request, 'auctions/categories.html')


def filter(request):
    q = request.GET['category'].lower()
    return render(request, 'auctions/category.html',{
        'listing' : AuctionListing.objects.filter(category=q)
    })

def add_comment(request, id):
    anonymous = User.first_name
    if request.user is not anonymous:
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            comment = Comment(
                user = request.user,
                auction = get_list_or_404(AuctionListing, id=id),
                **f
            )
            comment.save()
            return HttpResponseRedirect(reverse('listing', kwargs={
                'id':id
            }))
        else:
            return render(request, 'auction/login.html',{
                'message':'Must be logged in to be able to comment'
            })
        