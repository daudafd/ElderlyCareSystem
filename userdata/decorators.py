from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):

            # print('working:', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorators


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'user':
            return redirect('home')
            
        if group == 'admin':
            return view_func(request, *args, **kwargs)
            
    return wrapper_func