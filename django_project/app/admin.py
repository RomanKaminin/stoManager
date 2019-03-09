from django.contrib import admin

from .models import Manager, Statement


class ManagerAdmin(admin.ModelAdmin):
    fields = ["name", "parent"]


class StatementAdmin(admin.ModelAdmin):
    list_display = ("manager", "first_name", "username", "date", "time", "auto_mark")
    list_filter = ["manager", "date", "time"]
    search_fields = ["manager", "date", "first_name"]


admin.site.register(Statement, StatementAdmin)
admin.site.register(Manager, ManagerAdmin)
