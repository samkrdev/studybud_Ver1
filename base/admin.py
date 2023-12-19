from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Topic)
admin.site.register(Message)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "updated", "created"]
    list_filter = ["updated", "created"]
    search_fields = ["name"]
    list_editable = ["name"]

    class Meta:
        model = Room
