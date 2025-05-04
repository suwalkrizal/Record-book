from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import datetime
from django.shortcuts import render


class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    @action(detail=False, methods=['get'])
    def grand_total(self, request):
        return Response({"grand_total": Record.grand_total()})

    @action(detail=False, methods=['get'])
    def daily_totals_html(self, request):
        selected_date = request.GET.get('date')
        daily_total = None
        records_for_day = None

        # Get all unique record dates
        available_dates = Record.objects.order_by('-month').values_list('month', flat=True).distinct()

        if selected_date:
            try:
                selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
                daily_total = Record.objects.filter(month=selected_date_obj).aggregate(total=models.Sum('saving_amount'))['total'] or 0
                records_for_day = Record.objects.filter(month=selected_date_obj)
            except ValueError:
                daily_total = "Invalid format. Use YYYY-MM-DD."
                selected_date_obj = None
        else:
            selected_date_obj = None

        grand_total = Record.grand_total()

        return render(request, 'daily_totals.html', {
            'selected_date': selected_date,
            'selected_date_obj': selected_date_obj,
            'daily_total': daily_total,
            'records_for_day': records_for_day,
            'grand_total': grand_total,
            'available_dates': sorted(set(available_dates)),
        })

class DepositedByViewSet(viewsets.ModelViewSet):
    queryset = DepositedBy.objects.all()
    serializer_class = DepositedBySerializer