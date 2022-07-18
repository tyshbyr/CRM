from django.contrib import admin

from crm.models import Client, Source, Status


class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'date_of_creation']

admin.site.register(Client, ClientAdmin)
admin.site.register(Source)
admin.site.register(Status)
