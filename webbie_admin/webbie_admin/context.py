from home.models import UserPermission



def user_permission(request):
    if request.user.is_superuser:
        permission_list = [i for i in range(1,50)]
    else:
        user_id = request.user.id
        user_p = list(UserPermission.objects.filter(user=user_id, permission=True).values('module_id'))
        permission_list = [p['module_id'] for p in user_p]
    return {"permission_list":permission_list}
