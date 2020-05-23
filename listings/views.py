from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import bedroom_choices, price_choices, state_choices

def listing(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def listings(request):
        listings = Listing.objects.order_by('-list_date').filter(is_published=True)
        #Adding pagination
        paginator = Paginator(listings, 3)

        page = request.GET.get('page')

        paged_listings = paginator.get_page(page)

        context = {
            'listings': paged_listings
        }
        return render(request, 'listings/listings.html', context)

def search(request):
    Query_list = Listing.objects.order_by('-list_date')

    #Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            Query_list = Query_list.filter(descripttion__icontains=keywords)

    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            Query_list = Query_list.filter(city__iexact=city)
    #Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            Query_list = Query_list.filter(bedrooms__lte=bedrooms)

    #State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            Query_list = Query_list.filter(state__iexact = state)
    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            Query_list = Query_list.filter(price__lte=price)


    context = {
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'listings': Query_list,
        'values': request.GET
    }


    return render(request, 'listings/search.html', context)
