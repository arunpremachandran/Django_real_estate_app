from django.contrib import admin
from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
    list_editable = ('is_published',)
    list_filter = ('realtor',)
    list_per_page = 25
    search_fields = ('title', 'descripttion', 'address', 'city', 'state', 'zipcode', 'price')

admin.site.register(Listing, ListingAdmin)
