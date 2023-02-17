from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from . import models
from django.contrib import messages
from django.views.generic import DetailView
from lista.models import Product
from .forms import ProductForm

class IndexView(TemplateView):
    template_name = 'lista/index.html'


class ProductListView(ListView):
    model = models.Product

    def get_queryset(self):
        if self.request.method == 'GET':
            product_id = self.request.GET.get('product_id', None)
            if product_id is not None:
                self.add_product(product_id)
        return models.Product.objects.all()

    def add_product(self, product_id):
        user = self.request.user
        if not user or not user.is_authenticated:
            messages.error(self.request, "Cannot add product to gift list without authentication")
            return
        product = models.Product.objects.get(pk=product_id)
        gift_list = user.couple.gift_lists.all().first()
        gift, created = models.Gift_item.objects.get_or_create(gift_list=gift_list, product=product)
        if not created:
            gift.increase_quantity()
        messages.info(self.request, "Successfully added gift to gift list")


class GiftListView(ListView):
    context_object_name = 'gift_lists'
    template_name = 'lista/gift_list.html'
    model = models.Gift_list

    def get_queryset(self):
        if self.request.method == 'GET':
            delete_gift_id = self.request.GET.get('delete_gift_id', None)
            buy_gift_id = self.request.GET.get('buy_gift_id', None)
            if delete_gift_id is not None:  # TODO handle delete if one gift was already bought
                self.delete_gift(delete_gift_id)
            if buy_gift_id is not None:
                self.buy_gift(buy_gift_id)
        return models.Gift_list.objects.all()

    def delete_gift(self, gift_id):
        try:
            gift = models.Gift_item.objects.get(pk=gift_id)
            if gift.quantity == 1:
                gift.delete()
            else:
                gift.decrease_quantity()
            messages.info(self.request, "Successfully removed a gift")
        except ValidationError as err:
            messages.error("Error when deleting gift: {}".format(err))

    def buy_gift(self, gift_id):
        try:
            gift = models.Gift_item.objects.get(pk=gift_id)
            gift.buy_one()
            messages.info(self.request, "Successfully bought gift")
        except ValidationError as err:
            messages.error(self.request, "Error when buying gift: {}".format(err))


class ReportView(ListView):
    model = models.Gift_list
    context_object_name = 'reports'
    template_name = 'lista/report.html'


class LoginView(View):
    template_name = 'lista/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.info(self.request, "Successfully logged in")
            else:
                messages.error(self.request, "Inactive user.")
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(self.request, "Invalid login details supplied")
        return HttpResponseRedirect(reverse('lista:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



class EmpImageDisplay(DetailView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'product'

def salva_convidado(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProductForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            print("VALIDO")
            product = form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/lista/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProductForm()

    return render(request, 'lista/product_list.html', {'form': form})

# listings/views.py

def product_update(request, id):
    objeto_id = request.POST.get('guest_name')
    print(objeto_id)
    print(list(request.POST.items()))
    # product = Product.objects.get(id=objeto_id)
    # print(product.id)
    print(id)
    product = Product.objects.get(id=id)
    product.status = False
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return HttpResponseRedirect('/lista/')
    else:
        form = ProductForm(instance=product)

    return render(request, 'lista/product_list.html', {'form': form})