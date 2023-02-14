from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='upload/', null=True)
    guest_name = models.CharField(max_length=100, default="Convidado")
    guest_email = models.CharField(max_length=100, default="Convidado")
    in_stock_quantity = models.PositiveIntegerField(default=0)

    def buy(self):
        if self.in_stock_quantity == 0:
            raise ValidationError("Cannot buy products that are not in stock")
        self.in_stock_quantity -= 1
        self.save()

    def __str__(self):
        return str(self.name)


class Couple(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groom_name = models.CharField(max_length=100, default="Andy Groom")
    bride_name = models.CharField(max_length=100, default="Beatrix Kiddo")
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return str(self.email)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Couple.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.couple.save()


class Gift_list(models.Model):
    name = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    couple = models.ForeignKey(Couple, related_name="gift_lists", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Gift_item(models.Model):
    added = models.DateTimeField(auto_now_add=True, editable=False)
    bought_quantity = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=500)
    gift_list = models.ForeignKey(Gift_list, related_name="gifts", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="gifts", on_delete=models.CASCADE)

    def buy_one(self):
        if self.bought_quantity == self.quantity:
            raise ValidationError("Cannot buy more gift then needed!")
        self.product.buy()
        self.bought_quantity += 1
        self.save()

    def increase_quantity(self):
        self.quantity += 1
        self.save()

    def decrease_quantity(self):
        if self.quantity == 1:
            raise ValidationError("Cannot modify gift quantity below 1")
        self.quantity -= 1
        self.save()

    def __str__(self):
        return str(self.product.name)
