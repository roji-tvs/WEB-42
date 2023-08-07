from django.core.exceptions import PermissionDenied
from home.models import UserPermission
from functools import wraps
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect


def user_permission(module_id):
    def _user_permission(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            print("args  ",args)
            print("kargs  ",kwargs)

            user_perm = UserPermission.objects.filter(user_id=request.user.id, module_id=module_id, module__status=True,
                                                 permission=True).exists()
            if user_perm or request.user.is_superuser:
                return function(request, *args, **kwargs)
            else:
                print("sarat")
                messages.warning(request, 'You dont have sufficient permission. Please contact admin.')
                return redirect('/' )
                # raise PermissionDenied
        # wrap.__doc__ = function.__doc__
        # wrap.__name__ = function.__name__
        return wrapper
    return _user_permission

