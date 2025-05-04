from django.contrib import admin
from django.db.models import Sum
from .models import *


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'month', 'saving_amount')
    list_filter = ('month', 'member')
    search_fields = ('member__name',)
    date_hierarchy = 'month'


@admin.register(DepositedBy)
class DepositedByAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'amount_deposited', 'related_month','image_display')
    list_filter = ('related_month',)
    search_fields = ('person',)
    date_hierarchy = 'related_month'

    def image_display(self, obj):
        if obj.image:
            return f"✅"
        return "❌"
    image_display.short_description = 'Image Uploaded'
    
# @admin.register(GrandTotal)
# class GrandTotalAdmin(admin.ModelAdmin):
#     list_display = ('total',)