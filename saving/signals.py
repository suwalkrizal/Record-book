# # signals.py
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Record, GrandTotal
# from django.db.models import Sum

# def update_grand_total():
#     total = Record.objects.aggregate(total=Sum('saving_amount'))['total'] or 0.00
#     obj, created = GrandTotal.objects.get_or_create(pk=1)
#     obj.total = total
#     obj.save()

# @receiver(post_save, sender=Record)
# def update_on_save(sender, instance, **kwargs):
#     update_grand_total()

# @receiver(post_delete, sender=Record)
# def update_on_delete(sender, instance, **kwargs):
#     update_grand_total()
