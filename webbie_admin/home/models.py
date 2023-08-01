from django.db import models
# Create your models here.
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

# from .managers import UserManager



class User(AbstractUser):
    SUPER_ADMIN = 1
    ADMIN = 2
    MERCHANT = 3
    MERCHANT_STAFF = 4
    CUSTOMER = 5

    USER_TYPE_CHOICES = [(SUPER_ADMIN, "super-admin"),
                    (ADMIN, "admin"),
                    (MERCHANT, "merchant"),
                    (MERCHANT_STAFF, "merchant-staff"),
                    (CUSTOMER, "customer")]

    # username = None
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=25, null=False)
    country_code = models.CharField(max_length=5, null=True, default=None, help_text="do not add + extension")
    mobile_number = models.CharField(max_length=10, null=True, default=None,
                                     help_text="do not add country code")
    phone_number = models.CharField(max_length=10, null=True, default=None, help_text="landline number")
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_mail_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, default=None)
    otp_created_time = models.DateTimeField(null=True, default=None)

    # objects = UserManager()

    REQUIRED_FIELDS = ["email", "country_code", "mobile_number"]
    def save(self, *args, **kwargs):
        # Check if the user_type is set to SUPER_ADMIN or MERCHANT_STAFF
        # and set is_admin and is_staff fields accordingly.
        if self.user_type == self.SUPER_ADMIN :
            self.is_superuser = True
            self.is_staff = True
        
        elif self.user_type == self.ADMIN:
            self.is_staff = True

        super(User, self).save(*args, **kwargs)
    class Meta:
        db_table = "user"
        # unique_together = ('country_code', 'mobile_number', 'parent')




class UserExtraDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_extra_detail', unique=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_created_by', null=True, default=None, unique=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user_updated_by', unique=False, null=True, default=None)
    last_modified = models.DateTimeField(null=True, blank=True, default=None)
    is_invited = models.BooleanField(null=True, default=None) # True => Sent, False = > Account Created
    invite_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    # invited_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user_invited_by', null=True, default=None,)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'User_extra_detail'





class Module(models.Model):
    module_name = models.CharField(max_length=200, blank=False, null=False)
    module_description = models.TextField(blank=True, null=True, default=None)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_created_by', null=True, default=None,
                                   unique=False)
    created_date = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_updated_by', unique=False, null=True, default=None)
    last_modified = models.DateTimeField(null=True, blank=True, default=None)
    
    class Meta:
        db_table = 'User_module'

class UserPermission(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, unique=False)
    module = models.ForeignKey(Module,  on_delete=models.CASCADE, unique=False)
    permission = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'User_permission'


class WebsiteInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_website', blank=False, null=False)
    website_name = models.CharField(max_length=25, null=False, unique=True)
    host_name = models.CharField(max_length=25, null=False, unique=True)
    logo = models.URLField()
    banner = models.URLField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "website_info"


class AddressDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address', blank=False, null=False)
    address_line1 = models.CharField(max_length=25, null=False, unique=False)
    address_line2 = models.CharField(max_length=25, null=False, unique=False)
    city = models.CharField(max_length=25, null=False, unique=False)
    country = models.CharField(max_length=25, null=False, unique=False)
    postal_code = models.CharField(max_length=25, null=False, unique=False)
    receivers_name = models.CharField(max_length=25, null=False, unique=False)
    country_code = models.CharField(max_length=5, null=True, default=None, help_text="do not add + extension")
    mobile_number = models.CharField(unique=True, max_length=10, null=True, default=None,
                                     help_text="do not add country code")
    address_nick_name = models.CharField(max_length=25, null=False, unique=False)

    class Meta:
        db_table = "address_detail"


class SubscriptionDetail(models.Model):
    name = models.CharField(max_length=25, null=False, unique=False)
    duration = models.IntegerField(help_text="duration in days")
    price = models.FloatField()
    info = models.CharField(max_length=250, null=False, unique=False)
    discount = models.FloatField()

    class Meta:
        db_table = "subscription_detail"


class MerchantSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_subscription_map', blank=False, null=False)
    subscription_type = models.ForeignKey(SubscriptionDetail, on_delete=models.CASCADE,
                                          related_name='subscription_type_map', blank=False, null=False)
    subscription_start_timestamp = models.DateTimeField()

    
    # def is_active_subscription(self):
    #     """
    #     Check if the user has an active subscription.
    #     An active subscription is one whose start timestamp is in the past
    #     and has not yet reached the end of the subscription period.
    #     """
    #     now = timezone.now()
    #     return self.subscription_start_timestamp <= now and \
    #            self.subscription_type.end_timestamp > now

    # def save(self, *args, **kwargs):
    #     """
    #     Override the default save method to check for an active subscription
    #     before saving the new subscription object.
    #     """
    #     if self.is_active_subscription():
    #         # Assuming you want to prevent creating multiple active subscriptions for the same user
    #         raise ValueError("User already has an active subscription.")
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = "merchant_subscription"



class Currency(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=15)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    decimal_place = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'currencies'


class ProductCategory(models.Model):
    name = models.CharField(max_length=15)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_category'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If the instance is a parent, update all children status
        if self.parent is None:
            self.update_children_status()

    def update_children_status(self):
        # Update status of all children recursively
        children = ProductCategory.objects.filter(parent=self)
        for child in children:
            child.status = self.status
            child.save()

class Product(models.Model):
    name = models.CharField(max_length=255, help_text="The name of the product.")
    description = models.TextField(help_text="A detailed description of the product.")
    count = models.PositiveIntegerField(default=0, help_text="The available quantity of the product.")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, help_text="The currency used for pricing the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="The price of the product.")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, help_text="The category of the product.")
    merchant_id = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The ID of the merchant selling the product.")
    brand = models.CharField(max_length=100, help_text="The brand name of the product.")  # Added brand field
    dimension = models.CharField(max_length=20, help_text="The dimensions of the product in the format: Length*Width*Height.")
    size = models.CharField(max_length=50, help_text="The size or measurement information of the product.")
    created = models.DateTimeField(auto_now_add=True, help_text="The date and time when the product was created.")
    updated = models.DateTimeField(auto_now=True, help_text="The date and time when the product was last updated.")
    status = models.BooleanField(default=True, help_text="The status of the product. True means active, and False means inactive.")
    verification_status = models.BooleanField(default=False, help_text="The verification status of the product. True means verified, and False means not verified.")
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, help_text="The weight of the product.")

    class Meta:
        db_table = 'product'



class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', help_text="The product associated with this image.")
    url = models.URLField(max_length=500, help_text="The URL of the product image.")  # Increased max_length to 500
    created = models.DateTimeField(auto_now_add=True, help_text="The date and time when the product image was created.")
    sequence = models.PositiveIntegerField(default=0, help_text="The sequence number to order the images.")

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        db_table = 'product_image'
