from django.contrib import admin
from django.db.models import Sum
from .models import *

from django.core.mail import send_mail
from django.conf import settings

from threading import Thread


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
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
    
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # check if it's a new object
        super().save_model(request, obj, form, change)

        if is_new:
            # Send email to all group members
            recipient_list = list(GroupMember.objects.values_list('email', flat=True))
            subject = "New Deposit Notification"
            message = f"{obj.person} has deposited Rs {obj.amount_deposited}."
            
            def send_email():
                if recipient_list:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        recipient_list,
                        fail_silently=False,
                    )
                
            # Run the email in a separate thread
            Thread(target=send_email).start()
    
