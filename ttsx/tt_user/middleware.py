class UrlMiddleware:
    def process_view(self,request,view_name,view_args,view_kwargs):
        # print '-----------------%s'%request.path
        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/register_valid/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/',
                                '/user/islogin/',]:
            request.session['url_path']=request.get_full_path()

'''
http://www.itcast.cn/python/?a=100

get_full_path()-->/python/?a=100
path-->/python/
'''
