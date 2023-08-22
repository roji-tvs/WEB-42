from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import *

# Create your views here.


def add_markup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        value = float(request.POST.get('value'))
        markup_type = int(request.POST.get('type'))
        merchant_name = request.POST.get('merchants').strip()
        category_name = request.POST.get('category').strip()
        status = request.POST.get('status', False) == 'on'
        priority = int(request.POST.get('priority'))
        currency_name = request.POST.get('currency').strip()

        if Markup.objects.filter(name=name).exists():
            messages.error(request, "A markup with this name already exists.")
            return render(request, 'merchant/add_markup.html', {'segment': 'markup'})



        try:
            merchant = User.objects.get(name__iexact=merchant_name)
            category = ProductCategory.objects.get(name__iexact=category_name)
            currency = Currency.objects.get(name__iexact=currency_name)
        except User.DoesNotExist:
            messages.error(request, f"Merchant '{merchant_name}' does not exist.")
            return render(request, 'merchant/add_markup.html', {'segment': 'markup'})
        except ProductCategory.DoesNotExist:
            messages.error(request, f"Category '{category_name}' does not exist.")
            return render(request, 'merchant/add_markup.html', {'segment': 'markup'})
        except Currency.DoesNotExist:
            messages.error(request, f"Currency '{currency_name}' does not exist.")
            return render(request, 'merchant/add_markup.html', {'segment': 'markup'})

        markup = Markup.objects.create(
            name=name,
            value=value,
            type=markup_type,
            merchants_id=merchant,
            category_id=category,
            status=status,
            priority=priority,
            currency=currency
        )

        markup.save()
        # messages.success(request, "Data added/updated successfully.")
        return redirect('markup')

    return render(request, 'merchant/add_markup.html', {'segment': 'markup'})



def update_markup(request,id):  
    print(id)
    try:
        markup = Markup.objects.get(pk=id)
    except Markup.DoesNotExist:
        messages.error(request, f"Markup with ID {id} does not exist.")
        return render(request,'merchant/update_markup.html',context={'segment':'markup'})
    

    print(markup.merchants_id,markup.category_id)
    # currencies=Currency.objects.all()
    if request.method == 'POST':
       markup.name = request.POST.get('name')
       markup.value = float(request.POST.get('value'))
       markup.type = int(request.POST.get('type'))
       merchant_name = request.POST.get('merchants').strip()
       category_name = request.POST.get('category').strip()
       markup.status = request.POST.get('status', False) == 'on'
       markup.priority = int(request.POST.get('priority'))
       currency_name = request.POST.get('currency').strip()

       try:
            markup.merchants_id = User.objects.get(name__iexact=merchant_name)
            markup.category_id = ProductCategory.objects.get(name__iexact=category_name)
            markup.currency = Currency.objects.get(name__iexact=currency_name)
       except User.DoesNotExist:
            messages.error(request, f"Merchant '{merchant_name}' does not exist.")
            return render(request, 'merchant/update_markup.html', {'segment': 'markup','markup': markup})
       except ProductCategory.DoesNotExist:
            messages.error(request, f"Category '{category_name}' does not exist.")
            return render(request, 'merchant/update_markup.html', {'segment': 'markup','markup': markup})
       except Currency.DoesNotExist:
            messages.error(request, f"Currency '{currency_name}' does not exist.")
            return render(request, 'merchant/update_markup.html', {'segment': 'markup','markup': markup})
       
       markup.save() 
       return redirect('markup')
    

    return render(request,'merchant/update_markup.html',context={'markup': markup ,'segment':'markup'})
    


def markup_list(request):
    
        page = request.GET.get('page', 1)

        markup_detail = Markup.objects.all().order_by('-updated_at')

        paginator = Paginator(markup_detail, 5)
        try:
            markup_detail = paginator.page(page)
        except PageNotAnInteger:
            markup_detail = paginator.page(1)
        except EmptyPage:
            markup_detail = paginator.page(paginator.num_pages)
        index = markup_detail.start_index()
        total_pages = paginator.num_pages
        try:
            next_page = markup_detail.next_page_number()
        except:
            next_page = None
        print(markup_detail,total_pages)
        context={"markup_detail": markup_detail,
             "index": index, 
             "total_pages": total_pages,                                              
             "next_page": next_page, 
             'segment': 'markup'}

        return render(request,'merchant/markup_details.html',context)


def add_discount(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        value = float(request.POST.get('value'))
        discount_type = int(request.POST.get('type'))
        merchant_name = request.POST.get('merchants').strip()
        category_name = request.POST.get('category').strip()
        status = request.POST.get('status', False) == 'on'
        priority = int(request.POST.get('priority'))
        currency_name = request.POST.get('currency').strip()

        if Discount.objects.filter(name=name).exists():
            messages.error(request, "A discount with this name already exists.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount'})



        try:
            merchant = User.objects.get(name__iexact=merchant_name)
            category = ProductCategory.objects.get(name__iexact=category_name)
            currency = Currency.objects.get(name__iexact=currency_name)
        except User.DoesNotExist:
            messages.error(request, f"Merchant '{merchant_name}' does not exist.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount'})
        except ProductCategory.DoesNotExist:
            messages.error(request, f"Category '{category_name}' does not exist.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount'})
        except Currency.DoesNotExist:
            messages.error(request, f"Currency '{currency_name}' does not exist.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount'})

        discount = Discount.objects.create(
            name=name,
            value=value,
            type=discount_type,
            merchants_id=merchant,
            category_id=category,
            status=status,
            priority=priority,
            currency=currency
        )
        discount.save()
        return redirect('discount')  # Redirect to the list of markup objects
        
    return render(request, 'merchant/add_discount.html',  context={ 'segment': 'discount' })


def update_discount(request,id):  
    print(id)
    try:
        discount = Discount.objects.get(pk=id)
    except Discount.DoesNotExist:
        messages.error(request, f"Discount with ID {id} does not exist.")
        return render(request,'merchant/update_discount.html',context={'segment':'discount'})

    if request.method == 'POST':
        discount.name = request.POST.get('name')
        discount.value = float(request.POST.get('value'))
        discount.type = int(request.POST.get('type'))
        merchant_name = request.POST.get('merchants').strip()
        category_name = request.POST.get('category').strip()
        discount.status = request.POST.get('status', False) == 'on'
        discount.priority = int(request.POST.get('priority'))
        currency_name = request.POST.get('currency').strip()

        try:
            discount.merchants_id = User.objects.get(name__iexact=merchant_name)
            discount.category_id = ProductCategory.objects.get(name__iexact=category_name)
            discount.currency = Currency.objects.get(name__iexact=currency_name)
        except User.DoesNotExist:
            messages.error(request, f"Merchant '{merchant_name}' does not exist.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount','discount': discount })
        except ProductCategory.DoesNotExist:
            messages.error(request, f"Category '{category_name}' does not exist.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount','discount': discount })
        except Currency.DoesNotExist:
            messages.error(request, f"Currency '{currency_name}' does not exist.")
            return render(request, 'merchant/add_discount.html', {'segment': 'discount','discount': discount })
        
        discount.save()
        
        return redirect('discount')
    

    return render(request,'merchant/update_discount.html',context={'discount': discount ,'segment':'discount'})
    



def discount_list(request):
        page = request.GET.get('page', 1)

        discount_detail = Discount.objects.all().order_by('-updated_at')

        paginator = Paginator(discount_detail, 5)
        try:
            discount_detail = paginator.page(page)
        except PageNotAnInteger:
            discount_detail = paginator.page(1)
        except EmptyPage:
            discount_detail = paginator.page(paginator.num_pages)
        index = discount_detail.start_index()
        total_pages = paginator.num_pages
        try:
            next_page = discount_detail.next_page_number()
        except:
            next_page = None
        print(discount_detail,total_pages)
        context={"discount_detail": discount_detail,
             "index": index, 
             "total_pages": total_pages,                                              
             "next_page": next_page, 
             'segment': 'discount'}
        return render(request,'merchant/discount_details.html',context)
    

def transaction_list(request):
        page = request.GET.get('page', 1)

        transaction_detail = Transaction.objects.all().order_by('-updated_at')

        paginator = Paginator(transaction_detail, 5)
        try:
            transaction_detail = paginator.page(page)
        except PageNotAnInteger:
            transaction_detail = paginator.page(1)
        except EmptyPage:
            transaction_detail = paginator.page(paginator.num_pages)
        index = transaction_detail.start_index()
        total_pages = paginator.num_pages
        try:
            next_page = transaction_detail.next_page_number()
        except:
            next_page = None
        print(transaction_detail,total_pages)
        context={"transaction_detail": transaction_detail,
             "index": index, 
             "total_pages": total_pages,                                              
             "next_page": next_page, 
             'segment': 'transactions'}

        return render(request,'merchant/transaction_details.html',context)


def update_transaction(request,id):  
    print(id)
    try:
        transaction = Transaction.objects.get(pk=id)
    except Transaction.DoesNotExist:
        messages.error(request, f"Transactions with ID {id} does not exist.")
        return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})

    if request.method == 'POST':
        transaction.price = float(request.POST.get('price'))
        transaction.markup_value = float(request.POST.get('markup_value'))
        transaction.discount_value = float(request.POST.get('discount_value'))
        merchant = request.POST.get('merchant').strip()
        product = request.POST.get('product').strip()
        discount = request.POST.get('discount').strip()
        markup = request.POST.get('markup').strip()
        user = request.POST.get('user').strip()
        currency = request.POST.get('currency').strip()

        try:
            transaction.merchant = User.objects.get(name__iexact=merchant)
            transaction.product= Product.objects.get(name__iexact=product)
            transaction.discount= Discount.objects.get(name__iexact=discount)
            transaction.markup = Markup.objects.get(name__iexact=markup)
            transaction.currency = Currency.objects.get(name__iexact=currency)
            transaction.user = User.objects.get(name__iexact=user)
        except User.DoesNotExist:
            messages.error(request, f"Merchant '{merchant}' does not exist.")
            return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
        except Product.DoesNotExist:
            messages.error(request, f"Category '{product}' does not exist.")
            return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
        except Discount.DoesNotExist:
            messages.error(request, f"Currency '{discount}' does not exist.")
            return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
        except Markup.DoesNotExist:
            messages.error(request, f"Currency '{markup}' does not exist.")
            return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
        except Currency.DoesNotExist:
            messages.error(request, f"Currency '{currency}' does not exist.")
            return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
        except User.DoesNotExist:
            messages.error(request, f"Currency '{user}' does not exist.")
            return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
        
        
        transaction.save()
        
        return redirect('transactions')
    

    return render(request,'merchant/update_transaction.html',context={'transaction': transaction ,'segment':'transactions'})
    
     
@require_GET
def autocomplete_user(request):
    # Modify the query to match against your available fields
    users = User.objects.filter(Q(name__icontains=request.GET['term']))[:10]
    suggestions = [{'id': user.id, 'value': user.name} for user in users]
    return JsonResponse(suggestions, safe=False)

@require_GET
def autocomplete_product_category(request):
    categories = ProductCategory.objects.filter(name__icontains=request.GET['term'])[:10]
    suggestions = [{'id': category.id, 'value': category.name} for category in categories]
    return JsonResponse(suggestions, safe=False)

@require_GET
def autocomplete_currency(request):
    currencies = Currency.objects.filter(name__icontains=request.GET['term'])[:10]
    suggestions = [{'id': currency.code, 'value': currency.name} for currency in currencies]
    return JsonResponse(suggestions, safe=False)

@require_GET
def autocomplete_product(request):
    products = Product.objects.filter(name__icontains=request.GET['term'])[:10]
    suggestions = [{'id': product.id, 'value': product.name} for product in products]
    return JsonResponse(suggestions, safe=False)

@require_GET
def autocomplete_markup(request):
    markups = Markup.objects.filter(name__icontains=request.GET['term'])[:10]
    suggestions = [{'id': markup.id, 'value': markup.name} for markup in markups]
    return JsonResponse(suggestions, safe=False)

@require_GET
def autocomplete_discount(request):
    discounts = Discount.objects.filter(name__icontains=request.GET['term'])[:10]
    suggestions = [{'id': discount.id, 'value': discount.name} for discount in discounts]
    return JsonResponse(suggestions, safe=False)






