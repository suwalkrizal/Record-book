from django.db import models
from django.utils.timezone import now

class GroupMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Record(models.Model):
    month = models.DateField(default=now)
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    saving_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('month', 'member')

    def __str__(self):
        return f"{self.member.name} - {self.month.strftime('%B %Y')}"

    @staticmethod
    def daily_total(date):
        return Record.objects.filter(month=date).aggregate(total=models.Sum('saving_amount'))['total'] or 0

    @staticmethod
    def grand_total():
        return Record.objects.aggregate(
            grand_total=models.Sum('saving_amount')
        )['grand_total'] or 0


class DepositedBy(models.Model):
    person = models.CharField(max_length=100)
    amount_deposited = models.DecimalField(max_digits=10, decimal_places=2)
    related_month = models.DateField()
    records = models.ManyToManyField('Record', blank=True) 
    image = models.ImageField(upload_to='deposit_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.person} - {self.amount_deposited} - {self.related_month.strftime('%B %Y')}"
