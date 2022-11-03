from django.contrib import admin

from .models import User, Food_Obj, Food_Cat, Food_log_mdl, Image, UserWeight

admin.site.register(User)
admin.site.register(Food_Obj)
admin.site.register(Food_Cat)
admin.site.register(Food_log_mdl)
admin.site.register(Image)
admin.site.register(UserWeight)
