from cfgmake.models import Server, UnixUser, ConfigFile, Application
from django.contrib import admin

admin.site.register(Server)
admin.site.register(UnixUser)
admin.site.register(ConfigFile)
admin.site.register(Application)
