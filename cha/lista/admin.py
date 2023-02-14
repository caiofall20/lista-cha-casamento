from django.contrib import admin
from .models import Couple, Product, Gift_item, Gift_list

admin.site.register(Couple)
admin.site.register(Product)
admin.site.register(Gift_list)
admin.site.register(Gift_item)