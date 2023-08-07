# populate_dummy_data.py

import os
from django.utils import timezone
from django.contrib.auth import get_user_model
from faker import Faker
from home.models import (UserExtraDetail, Module, UserPermission, WebsiteInfo,
                          AddressDetail, SubscriptionDetail, MerchantSubscription,
                          Currency, ProductCategory, Product, ProductImage)

def create_dummy_users(num_users=20):
    User = get_user_model()

    if User.objects.count()>10 :

        fake = Faker()

        for _ in range(num_users):
            email = fake.email()
            name = fake.name()
            country_code = fake.country_calling_code()
            mobile_number = fake.msisdn()
            user_type = User.MERCHANT
            user = User.objects.create_user(username=email, email=email, password="password123",
                                            name=name, country_code=country_code, mobile_number=mobile_number,
                                            user_type=user_type)

def create_dummy_modules(num_modules=20):
    fake = Faker()
    if Module.objects.count()  == 0:

        for _ in range(num_modules):
            module_name = fake.word()
            module_description = fake.sentence()
            status = fake.boolean()
            created_date = timezone.now()
            Module.objects.create(module_name=module_name, module_description=module_description,
                                status=status, created_date=created_date)

def create_dummy_user_permissions(num_permissions=100):
    fake = Faker()
    if UserPermission.objects.count()  == 0:

        users = get_user_model().objects.all()
        modules = Module.objects.all()

        for _ in range(num_permissions):
            user = fake.random_element(users)
            module = fake.random_element(modules)
            permission = fake.boolean()
            UserPermission.objects.create(user=user, module=module, permission=permission)

def create_dummy_website_infos(num_websites=20):
    fake = Faker()
    if WebsiteInfo.objects.count()  == 0:

        users = get_user_model().objects.all()

        for _ in range(num_websites):
            user = fake.random_element(users)
            website_name = fake.domain_name()
            host_name = fake.domain_name()
            logo = fake.url()
            banner = fake.url()
            status = fake.boolean()
            WebsiteInfo.objects.create(user=user, website_name=website_name, host_name=host_name,
                                    logo=logo, banner=banner, status=status)

def create_dummy_address_details(num_addresses=20):
    fake = Faker()
    if AddressDetail.objects.count()  == 0:

        users = get_user_model().objects.all()

        for _ in range(num_addresses):
            user = fake.random_element(users)
            address_line1 = fake.street_address()
            address_line2 = fake.secondary_address()
            city = fake.city()
            country = fake.country()
            postal_code = fake.postcode()
            receivers_name = fake.name()
            country_code = fake.country_calling_code()
            mobile_number = fake.msisdn()
            address_nick_name = fake.word()
            AddressDetail.objects.create(user=user, address_line1=address_line1, address_line2=address_line2,
                                        city=city, country=country, postal_code=postal_code, receivers_name=receivers_name,
                                        country_code=country_code, mobile_number=mobile_number,
                                     address_nick_name=address_nick_name)
def random_float(min, max, precision=2):
    fake = Faker()

    factor = 10 ** precision
    return round(fake.random_int(min=min * factor, max=max * factor) / factor, precision)

def create_dummy_subscription_details(num_subscriptions=10):
    fake = Faker()
    if SubscriptionDetail.objects.count()  == 0:

        for _ in range(num_subscriptions):
            name = fake.word()
            duration = fake.random_int(min=30, max=365)  # Random duration between 30 and 365 days
            price = random_float(min=10.0, max=1000.0)  # Random price between 10.0 and 1000.0
            info = fake.sentence()
            discount = random_float(min=0.0, max=50.0)  # Random discount between 0.0 and 50.0
            SubscriptionDetail.objects.create(name=name, duration=duration, price=price,
                                            info=info, discount=discount)

def create_dummy_merchant_subscriptions(num_subscriptions=50):
    fake = Faker()
    if MerchantSubscription.objects.count()  == 0:

        User = get_user_model()
        users = get_user_model().objects.filter(user_type=User.MERCHANT)
        subscription_types = SubscriptionDetail.objects.all()

        for _ in range(num_subscriptions):
            user = fake.random_element(users)
            subscription_type = fake.random_element(subscription_types)
            subscription_start_timestamp = fake.past_datetime(start_date="-30d", tzinfo=timezone.utc)  # Random date within the last 30 days
            MerchantSubscription.objects.create(user=user, subscription_type=subscription_type,
                                                subscription_start_timestamp=subscription_start_timestamp)

def create_dummy_currencies(num_currencies=10):
    fake = Faker()

    if Currency.objects.count()  == 0:
        for _ in range(num_currencies):
            code = fake.currency_code()
            name = fake.currency_name()
            exchange_rate = random_float(min=0.1, max=5.0)  # Random exchange rate between 0.1 and 5.0
            decimal_place = fake.random_int(min=2, max=4)  # Random decimal place between 2 and 4
            created_date = timezone.now()
            status = fake.boolean()
            Currency.objects.create(code=code, name=name, exchange_rate=exchange_rate,
                                    decimal_place=decimal_place, created_date=created_date, status=status)

def create_dummy_product_categories(num_categories=20):
    fake = Faker()
    if ProductCategory.objects.count()  == 0:

        for _ in range(num_categories):
            name = fake.word()
            parent = None
            status = fake.boolean()
            ProductCategory.objects.create(name=name, parent=parent, status=status)

def create_dummy_products(num_products=50):
    fake = Faker()
    if Product.objects.count()  == 0:

        User = get_user_model()
        merchants = get_user_model().objects.filter(user_type=User.MERCHANT)
        categories = ProductCategory.objects.all()
        currencies = Currency.objects.all()

        for _ in range(num_products):
            name = fake.word()
            description = fake.sentence()
            count = fake.random_int(min=0, max=100)
            currency = fake.random_element(currencies)
            price = random_float(min=10.0, max=1000.0)
            category = fake.random_element(categories)
            merchant_id = fake.random_element(merchants)
            brand = fake.company()
            dimension = f"{fake.random_int(min=1, max=100)}*{fake.random_int(min=1, max=100)}*{fake.random_int(min=1, max=100)}"
            size = fake.word()
            created = fake.past_datetime(start_date="-365d", tzinfo=timezone.utc)  # Random date within the last 365 days
            updated = fake.past_datetime(start_date="-30d", tzinfo=timezone.utc)  # Random date within the last 30 days
            status = fake.boolean()
            verification_status = fake.boolean()
            weight = random_float(min=0.1, max=100.0)  # Random weight between 0.1 and 100.0
            Product.objects.create(name=name, description=description, count=count, currency=currency,
                                price=price, category=category, merchant_id=merchant_id, brand=brand,
                               dimension=dimension, size=size, created=created, updated=updated,
                               status=status, verification_status=verification_status, weight=weight)

def create_dummy_product_images(num_images=100):
    fake = Faker()
    products = Product.objects.all()
    if ProductImage.objects.count()  == 0:

        for _ in range(num_images):
            product = fake.random_element(products)
            url = fake.image_url(width=800, height=600)  # Random image URL
            created = fake.past_datetime(start_date="-30d", tzinfo=timezone.utc)  # Random date within the last 30 days
            sequence = fake.random_int(min=0, max=9)  # Random sequence number between 0 and 9
            ProductImage.objects.create(product=product, url=url, created=created, sequence=sequence)

def startdummy():
    print("ok")
    print("ok")


    create_dummy_users()
    create_dummy_modules()
    create_dummy_user_permissions()
    create_dummy_website_infos()
    create_dummy_address_details()
    create_dummy_subscription_details()
    create_dummy_merchant_subscriptions()
    create_dummy_currencies()
    create_dummy_product_categories()
    create_dummy_products()
    create_dummy_product_images()
