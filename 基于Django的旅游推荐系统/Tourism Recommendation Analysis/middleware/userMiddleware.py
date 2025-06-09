from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect
#  UserMiddleware 中间件的主要作用是：对用户访问路径进行登录状态的检查，
#  确保用户在访问受保护资源时是已登录状态，否则会被重定向到登录页面。
class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if path == '/app/login/' or path == '/app/register/':
            return None
        else:
            if not request.session.get('username'):
                return redirect('/app/login/')
            else:
                return None


    def process_view(self,request,callback,callback_args,callback_kwargs):
        pass

    def process_response(self,request,response):
        return response