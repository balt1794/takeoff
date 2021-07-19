from django.shortcuts import render, redirect
from .models import Listings
from .filters import ListingFilter
from .forms import ListingForm


def index(request):

    return render(request, 'listings/index.html')


def all_listings(request):
    all_listings = Listings.objects.order_by('-list_date')
    my_Filter = ListingFilter(request.GET, queryset=all_listings) 
    all_listings = my_Filter.qs


    context = {"all_listings": all_listings, "my_Filter": my_Filter}
    return render(request, 'listings/all_listings.html', context)


def new_listing(request):
    if request.method != 'POST': 
        form = ListingForm()
    else:
        form = ListingForm(request.POST, request.FILES) 
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.user = request.user 
            instance.save()
            return redirect('listings:all_listings')
            
    context = {'form': form}
    return render(request, 'listings/new_listing.html', context)
            

def detail(request, detail_id):
    detail = Listings.objects.get(id=detail_id)

    context = {'detail': detail}
    return render(request, 'listings/detail.html', context)


def my_listings(request):
    my_listings = request.user.listings_set.order_by('-list_date')

    context = {'my_listings': my_listings}
    return render(request, 'listings/my_listings.html', context)


def edit_listing(request, edit_id):
    listing = Listings.objects.get(id=edit_id)

    if request.method != 'POST':
        form = ListingForm(instance=listing) 
    else:
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings:my_listings')

    context = {'listing': listing, 'form': form}
    return render(request, 'listings/edit_listing.html', context)


def delete_listing(request, delete_id): 
    listing = Listings.objects.get(id=delete_id)

    if request.method == 'POST':
        listing.delete()
        return redirect('listings:my_listings') 

    context = {'listing': listing}
    return render(request, 'listings/delete_listing.html', context)