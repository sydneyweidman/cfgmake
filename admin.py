from cfgmake.models import Server, UnixUser, ConfigFile, Application, Partition
from django.contrib import admin

class PartitionAdmin(admin.ModelAdmin):
    list_display = ['server', 'mount', 'filesystem', 'size', 'avail']
        
class PartitionInline(admin.TabularInline):
    model = Partition
    extra = 3
    
admin.site.register(Partition, PartitionAdmin)

class ServerAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'ipaddr', 'location']
    inlines = [PartitionInline,]
    
admin.site.register(Server, ServerAdmin)

class UnixUserAdmin(admin.ModelAdmin):
    list_display = ['login', 'fullname', 'uid', 'gid', 'home']
    
admin.site.register(UnixUser, UnixUserAdmin)

admin.site.register(ConfigFile)
admin.site.register(Application)

