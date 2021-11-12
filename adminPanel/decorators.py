from django.shortcuts import redirect


def admin_ony(view_fun):
    def wrapper(request, *args, **kwargs):
        if 'admin' not in request.session:
            return redirect('admin-panel:login')
        return view_fun(request, *args, **kwargs)
    return wrapper
