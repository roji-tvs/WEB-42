from django.db import models
from home.models import *
from django.utils import timezone

# Create your models here.



class Discount(models.Model):
    DISCOUNT_TYPES = (
        (1, 'Percentage'),
        (2, 'Flat'),
    )

    name = models.CharField(max_length=100,unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveIntegerField(choices=DISCOUNT_TYPES)
    merchants_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    status= models.BooleanField(default=False)
    priority = models.PositiveIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'discount'



class Markup(models.Model):
    MARKUP_TYPES = (
        (1, 'Percentage'),
        (2, 'Flat'),
    )

    name = models.CharField(max_length=100, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveIntegerField(choices=MARKUP_TYPES)
    merchants_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    status= models.BooleanField(default=False)
    priority = models.PositiveIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'markup'

    def __str__(self):
        return self.name



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, related_name='merchant_transactions', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)  # Use the price from Product model
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    markup = models.ForeignKey(Markup, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    markup_value = models.DecimalField(max_digits=100, decimal_places=2)
    discount_value = models.DecimalField(max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'transaction'

    def __str__(self):
        return f"Transaction: {self.id}"
