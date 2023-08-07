from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model

from .models import UserPermission, Module, UserExtraDetail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from core.decorators import user_permission
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
import random
import string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from _core.send_mail import sendMail
from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
User = get_user_model()

# @method_decorator(user_permission(1), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(View):
    def get_random_string(self,length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def post(self, request):
        print("sarathvnbvnbvn")
        email = request.POST.get('email').strip()
        is_user_exist = User.objects.filter(email=email).exclude(first_name="", last_name="", last_login=None).exists()

        if is_user_exist:
            return JsonResponse({"success": False, "message":"Email already exists"})

        is_already_invited = UserExtraDetail.objects.filter(user__email = email, is_invited=True).exists()
        uid = request.user.id
        if is_already_invited:
            user = User.objects.get(email=email)
            UserExtraDetail.objects.filter(user=user).update(created_by_id=uid, invite_date=timezone.now())
            print('i am already invited')
        else:
            pswd = self.get_random_string(10)
            user = User.objects.create_user(email, email=email, password=pswd, )
            UserExtraDetail.objects.create(user_id=user.id, created_by_id=uid, is_invited=True, invite_date=timezone.now())

        current_site = get_current_site(request)

        uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        message = render_to_string('accounts/user_invitation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid64,
            'token': account_activation_token.make_token(user),
        })

        email_from = "admin@dokotella.com"
        recipient_list = [email]
        plain_message = strip_tags(message)
        subject = "Webbie Admin Account Creation"
        send_mail( subject, plain_message, email_from, recipient_list,fail_silently=True)
   
        messages.success(request, 'User Invited Successfully.')
        return JsonResponse({"success":True})

# @method_decorator(user_permission(1), name='dispatch')
class UserUpdateView(View):
    def get(self, request, *args, **kwargs):

        # return render(request, 'account/user_creation_form.html', context={"uid": "uidb64", "token": "token"})
        # print("A",*args)
        # print("b",**kwargs)
        uidb64 = kwargs['uid']
        token = kwargs['token']

        # return render(request, 'account/user_creation_form.html', context={"uid": uidb64, "token": token})

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # print("=====",user.user_extra_detail.is_invited)

        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'account/user_creation_form.html', context={"uid": uidb64, "token": token})
        else:
            # return JsonResponse({"status":False, "message":"Invalid User"})
            return HttpResponse(status=500)

    def post(self,request,*args,**kwargs):
        uidb64 = kwargs['uid']
        token = kwargs['token']
        print(uidb64, token)

        fname = request.POST.get('first_name').strip()
        lname = request.POST.get('last_name').strip()
        uname = request.POST.get('username').strip()
        pass1 = request.POST.get('password').strip()
        pass2 = request.POST.get('password2').strip()



        if not pass2 == pass1:
            return JsonResponse({"success":False, "message":"Password and Confirm password not match."})

        print(fname,lname,uname,pass2,pass1)


        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            # u = User.objects.get(username=kwargs['username'])
            # u.save()
            user.first_name = fname
            user.last_name = lname
            user.username = uname
            # user.user_extra_detail.is_invited = False
            user.set_password(pass1)
            user.save()
            UserExtraDetail.objects.filter(user=user).update(is_invited=False)
            # login(request, user)
            return redirect('login')
        else:
            return JsonResponse({"status":False, "message":"Invalid User"})


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(user_permission(1), name='dispatch')
class UserListView(View):
    def get(self, request):
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
        print(kwargs)
        user_detail = User.objects.filter(**kwargs).select_related('user_extra_detail')
        paginator = Paginator(user_detail, 25)

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

        return render(request, 'account/user_list.html', context={"user_detail":user_detail, "kwargs":kwargs,
                                                                "index":index, "total_pages":total_pages,
                                                                  "next_page":next_page, "user_name":user_name,
                                                                  "user_email":user_email, "status":status})

    def post(self, request):
        print("i will update user status")
        status = json.loads(request.POST.get("status"))
        user_id = request.POST.get("user_id")
        UserExtraDetail.objects.update_or_create(user_id=user_id,
                                                 defaults={"updated_by_id": request.user.id,
                                                           "last_modified": timezone.now()})
        User.objects.filter(id=user_id).update(is_active=status)
        return JsonResponse({"success":True})


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_permission(1), name='dispatch')
class UserPermissionView(View):
    def get(self, request, *args, **kwargs):
        print("a",args)
        print("ab",kwargs)
        user_id = kwargs['id']
        modules = list(Module.objects.all())
        user_name = User.objects.get(id=user_id).username
        user_permission = list(UserPermission.objects.filter(user=user_id, permission=True).values('module_id'))
        permission_list = [p['module_id'] for p in user_permission]
        # module_list = []
        for m in modules:
            print(m)
            if m.id in permission_list:
                m.permission = True
            else:
                m.permission = False

        print('i am  in permission',modules)
        return render(request,  'account/user_permission_modal.html', context={"module_list":modules, "user_id":user_id, "username":user_name})

    def post(self, request, *args, **kwargs):
        user_id = kwargs['id']
        user_permission = json.loads(request.POST.get('permission_list'))
        UserExtraDetail.objects.update_or_create(user_id=user_id,
                                                 defaults={"updated_by_id":request.user.id, "last_modified":timezone.now()})
        for permission in user_permission:
            # try: [{'1': True}, {'2': False}]
            # per, value = permission.items()[0]
            module, per = permission["module"], permission['permission']
            UserPermission.objects.update_or_create(user_id=user_id, module_id=int(module),  defaults={"permission": per})

            # user = User.objects.get(id=user_id)

        # for s in Session.objects.all():
        #     print(s.get_decoded().get('_auth_user_id'), user_id)
        #     print(type(s.get_decoded().get('_auth_user_id')), type(user_id))
        #     try:
        #         if s.get_decoded().get('_auth_user_id') == str(user_id):
        #             s.delete()
        #     except:
        #         pass

        # try:
        #     [s.delete() for s in Session.objects.all() if int(s.get_decoded().get('_auth_user_id')) == user.id]
        # except:
        #     pass
            # logout(request)

        return HttpResponse("jjjjjjjj")

@csrf_exempt
def check_unique_user(request):
    uname = request.POST.get('username').strip()
    uidb64 = request.POST.get('uid').strip()

    uid = force_str(urlsafe_base64_decode(uidb64))

    v = User.objects.exclude(id=uid).filter(Q(email=uname)| Q(username=uname)).exists()
    return JsonResponse({"success": v})