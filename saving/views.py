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
    def monthly_totals(self, request):
        month_param = request.query_params.get('month')
        if not month_param:
            return Response({"error": "month parameter required"}, status=400)
        try:
            month = datetime.strptime(month_param, "%Y-%m")
        except ValueError:
            return Response({"error": "Invalid format. Use YYYY-MM."}, status=400)

        total = Record.monthly_total(month)
        return Response({
            "month": month_param,
            "monthly_total": total
        })

    @action(detail=False, methods=['get'])
    def grand_total(self, request):
        return Response({"grand_total": Record.grand_total()})

    @action(detail=False, methods=['get'])
    def daily_totals_html(self, request):
        """Renders daily totals in an HTML template"""
        selected_date = request.GET.get('date')
        daily_total = None
        records_for_day = None

        if selected_date:
            try:
                selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
                # Get total savings for the selected day
                daily_total = Record.objects.filter(month=selected_date).aggregate(total=models.Sum('saving_amount'))['total'] or 0
                # Get all records for the selected day
                records_for_day = Record.objects.filter(month=selected_date)
            except ValueError:
                daily_total = "Invalid format. Use YYYY-MM-DD."

        grand_total = Record.grand_total()

        return render(request, 'daily_totals.html', {
            'selected_date': selected_date.strftime('%Y-%m-%d') if selected_date else None,
            'daily_total': daily_total,
            'records_for_day': records_for_day,
            'grand_total': grand_total
        })

class DepositedByViewSet(viewsets.ModelViewSet):
    queryset = DepositedBy.objects.all()
    serializer_class = DepositedBySerializer


# class GrandTotalViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = GrandTotal.objects.all()
#     serializer_class = GrandTotalSerializer