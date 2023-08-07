from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from .forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .models import MerchantSubscription
from .models import User, UserExtraDetail, WebsiteInfo, AddressDetail, MerchantSubscription,SubscriptionDetail,Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.



# def index(request):

# 	return render(request, 'pages/details.html', { 'segment': 'index', "id":1 })
@login_required
def index(request):
	
	page = request.GET.get('page', 1)

	user_detail = Product.objects.all()

	paginator = Paginator(user_detail, 5)
	try:
			user_detail = paginator.page(page)
	except PageNotAnInteger:
			user_detail = paginator.page(1)
	except EmptyPage:
			user_detail = paginator.page(paginator.num_pages)
	index = user_detail.start_index()
	total_pages = paginator.num_pages
	try:
			next_page = user_detail.next_page_number()
	except:
			next_page = None


	


	return render(request, 'pages/details.html', context={"user_detail":user_detail,
																															"index":index, "total_pages":total_pages,
																																"next_page":next_page,'segment': 'index'})

@login_required
def billing(request):
	return render(request, 'pages/billing.html', { 'segment': 'billing' })


@login_required
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

	"segment":"tables",

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

@login_required
def add_subcription(request):
	if request.method == "POST":
		name = request.POST.get('name')
		duration = int(request.POST.get('duration'))
		price = float(request.POST.get('price'))
		info = request.POST.get('info')
		discount = float(request.POST.get('discount'))


		# Create a new SubscriptionDetail object with the form data
		subscription_detail = SubscriptionDetail(
				name=name,
				duration=duration,
				price=price,
				info=info,
				discount=discount
		)

		# Save the object to the database
		subscription_detail.save()
	return render(request, 'pages/Subcription.html', { 'segment': 'subcription' })
		
		

@login_required
def subcription(request):
	if request.method == "POST":
		name = request.POST.get('name')
		duration = int(request.POST.get('duration'))
		price = float(request.POST.get('price'))
		info = request.POST.get('info')
		discount = float(request.POST.get('discount'))


		# Create a new SubscriptionDetail object with the form data
		subscription_detail = SubscriptionDetail(
				name=name,
				duration=duration,
				price=price,
				info=info,
				discount=discount
		)

		# Save the object to the database
		subscription_detail.save()
		return render(request, 'pages/Subcription.html', { 'segment': 'subcription' })
		
		
	else:

		page = request.GET.get('page', 1)

		subscription_detail = SubscriptionDetail.objects.all()
		paginator = Paginator(subscription_detail, 5)
		try:
				user_detail = paginator.page(page)
		except PageNotAnInteger:
				user_detail = paginator.page(1)
		except EmptyPage:
				user_detail = paginator.page(paginator.num_pages)
		index = user_detail.start_index()
		total_pages = paginator.num_pages
		try:
				next_page = user_detail.next_page_number()
		except:
				next_page = None

		return render(request, 'pages/sub_list.html', context={"user_detail":user_detail,
																															"index":index, "total_pages":total_pages,
																																"next_page":next_page,'segment': 'subcription'})
		
		return render(request, 'pages/Subcription.html', { 'segment': 'subcription' })



	
		
	
@login_required
def display_data(request):
	if request.method == "GET":
		kwargs = {}
		user_name = request.GET.get('user_name', "")
		user_email = request.GET.get('user_email', "")
		status = request.GET.get('status', "")	
		page = request.GET.get('page', 1)
		if user_name:
			kwargs['name__icontains'] = user_name.strip()
		if user_email:
			kwargs['email__icontains'] = user_email.strip()
		if status:
			kwargs['is_active'] = status
		user_detail = User.objects.filter(**kwargs).select_related('user_extra_detail')

		paginator = Paginator(user_detail, 5)
		try:
				user_detail = paginator.page(page)
		except PageNotAnInteger:
				user_detail = paginator.page(1)
		except EmptyPage:
				user_detail = paginator.page(paginator.num_pages)
		index = user_detail.start_index()
		total_pages = paginator.num_pages
		try:
				next_page = user_detail.next_page_number()
		except:
				next_page = None

		return render(request, 'pages/merchent_detail.html', context={"user_detail":user_detail, "kwargs":kwargs,
																															"index":index, "total_pages":total_pages,
																																"next_page":next_page, "user_name":user_name,
																																"user_email":user_email, "status":status,'segment': 'profile'})

	if request.method == "POST":
			print("i will update user status")
			status = json.loads(request.POST.get("status"))
			user_id = request.POST.get("user_id")
			UserExtraDetail.objects.update_or_create(user_id=user_id,
																								defaults={"updated_by_id": request.user.id,
																													"last_modified": timezone.now()})
			User.objects.filter(id=user_id).update(is_active=status)
			return JsonResponse({"success":True})


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

startdummy()
