from django.contrib import admin
from models import TypeInfo,GoodsInfo
# Register your models here.
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gprice','gunit','gclick','gkucun','gtype']
    list_per_page = 15

admin.site.register(TypeInfo)
admin.site.register(GoodsInfo,GoodsAdmin)
