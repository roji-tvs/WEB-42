from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from .models import UserPermission, Module
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from core.decorators import user_permission
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





# @method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(user_permission(2), name='dispatch')
class ModuleListView(View):
    def get(self, request):
        kwargs = {}
        module_name = request.GET.get('module_name', "")
        status = request.GET.get('status', "")
        page = request.GET.get('page', 1)

        if module_name:
            kwargs['module_name__icontains'] = module_name.strip()
        if status:
            kwargs['status'] = status

        module_detail = Module.objects.filter(**kwargs)
        print("count = ",module_detail.count())
        paginator = Paginator(module_detail, 10)

        try:
            module_detail = paginator.page(page)
        except PageNotAnInteger:
            module_detail = paginator.page(1)
        except EmptyPage:
            module_detail = paginator.page(paginator.num_pages)
        index = module_detail.start_index()
        total_pages = paginator.num_pages
        try:
            next_page = module_detail.next_page_number()
        except:
            next_page = None

        return render(request, 'accounts/module_list.html', context={"module_detail":module_detail, "kwargs":kwargs,
                                                                    "index":index, "total_pages":total_pages, "next_page":next_page, "module_name":module_name, "status":status})

    def post(self, request):
        module_status = request.POST.get('status')

        if module_status:
            module_id = request.POST.get('module_id')
            Module.objects.filter(id=module_id).update(status=json.loads(module_status))
            [s.delete() for s in Session.objects.all()]
            return JsonResponse({"success": True})

        module_name = request.POST.get('module_name').strip()
        module_desc = request.POST.get('module_desc').strip()
        uid = request.user
        created_date = timezone.now()
        # last
        Module.objects.create(module_name=module_name, module_description=module_desc, created_date=created_date, created_by_id=uid.id)
        return HttpResponseRedirect(f"/account/module-list/")
