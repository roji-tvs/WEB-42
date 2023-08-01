from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from .forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.core.paginator import Paginator
from .models import MerchantSubscription
from .models import User, UserExtraDetail, WebsiteInfo, AddressDetail, MerchantSubscription

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')

def index(request):

  return render(request, 'pages/index.html', { 'segment': 'index' })

def billing(request):
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
   queryset = MerchantSubscription.objects.prefetch_related('user', 'subscription_type').all().distinct()
   items_per_page = 5  # Set the number of items to display per page
   paginator = Paginator(queryset, items_per_page)
   page_number = request.GET.get('p',1)  # Get the page number from the query parameters
   try:
     page = paginator.page(page_number)
   except :
     page_number = 1
     page = paginator.page(page_number)

   total_pages = paginator.num_pages
  #  print(paginator)
   print(page.paginator.num_pages,page.number)
   context = {
        'cl': page, 
        'pagination_required':True,
        'total_pages':total_pages,
         # Pass the Paginator's Page object to the context as 'cl'
        # 'page_range': paginator.page_range,  # Pass the page range to the context
        # 'show_all_url': request.get_full_path(),  # Pass the current URL to 'show_all_url'

  

  "subscribers": page,
  "projects": [
    {
      "name": "Spotify",
      "budget": "$2,500",
      "status": "working",
      "completion_percentage": 60,
      "completion_color": "info",
      "logo": "{% static 'img/small-logos/logo-spotify.svg' %}"
    },
    {
      "name": "Invision",
      "budget": "$5,000",
      "status": "done",
      "completion_percentage": 100,
      "completion_color": "success",
      "logo": "{% static 'img/small-logos/logo-invision.svg' %}"
    },
    {
      "name": "Jira",
      "budget": "$3,400",
      "status": "canceled",
      "completion_percentage": 30,
      "completion_color": "danger",
      "logo": "{% static 'img/small-logos/logo-jira.svg' %}"
    },
    {
      "name": "Slack",
      "budget": "$1,000",
      "status": "canceled",
      "completion_percentage": 0,
      "completion_color": "success",
      "logo": "{% static 'img/small-logos/logo-slack.svg' %}"
    },
    {
      "name": "Webdev",
      "budget": "$14,000",
      "status": "working",
      "completion_percentage": 80,
      "completion_color": "info",
      "logo": "{% static 'img/small-logos/logo-webdev.svg' %}"
    },
    {
      "name": "Adobe XD",
      "budget": "$2,300",
      "status": "done",
      "completion_percentage": 100,
      "completion_color": "success",
      "logo": "{% static 'img/small-logos/logo-xd.svg' %}"
    }
  ]
}
   return render(request, 'pages/tables.html', context)

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def profile(request):
  return render(request, 'pages/profile.html', { 'segment': 'profile' })

def display_data(request):
    users = User.objects.all()
    user_extra_details = UserExtraDetail.objects.all()
    website_info = WebsiteInfo.objects.all()
    address_details = AddressDetail.objects.all()
    merchant_subscriptions = MerchantSubscription.objects.all()

    return render(request, 'pages/merchent_detail.html', {
        'users': users,
        'user_extra_details': user_extra_details,
        'website_info': website_info,
        'address_details': address_details,
        'merchant_subscriptions': merchant_subscriptions,
         'segment': 'profile'
    })

# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


from .dummydata import startdummy

# startdummy()
