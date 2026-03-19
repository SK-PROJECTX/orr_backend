from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from  ...models import Transaction


class PerformanceService:

    @staticmethod
    def get_last_six_months_performance(user):
        today = timezone.now()

        start_date = today - relativedelta(months=5)
        start_date = start_date.replace(day=1)

        queryset = (
            Transaction.objects.filter(
                wallet__owner=user,
                transaction_type="payment",
                date__gte=start_date,
            )
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

       
        data_map = {
            entry["month"].date(): entry["total"]
            for entry in queryset
        }

      
        graph_data = []
        for i in range(6):
            month_date = (start_date + relativedelta(months=i)).date()

            graph_data.append({
                "name": month_date.strftime("%b"),
                "full_date": month_date.strftime("%Y-%m-01"),
                "value": data_map.get(month_date, 0)
            })

        return graph_data
