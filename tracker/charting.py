from django.db.models import Sum
import plotly.express as px

from tracker.models import Category


def plot_income_expenses_bar_chart(qs):
    x_values = ["Income", "Expenses"]

    income = qs.filter(type="income").aggregate(total=Sum("amount"))["total"] or 0
    expense = qs.filter(type="expense").aggregate(total=Sum("amount"))["total"] or 0

    y_values = [income, expense]

    return px.bar(x=x_values, y=y_values)


def plot_category_pie_chart(qs):
    count_per_category = (
        qs.order_by("category").values("category").annotate(total=Sum("amount"))
    )
    category_pks = count_per_category.values_list("category", flat=True).order_by(
        "category"
    )
    categories = (
        Category.objects.filter(pk__in=category_pks)
        .order_by("pk")
        .values_list("name", flat=True)
    )
    total_amounts = count_per_category.values_list("total", flat=True)

    fig = px.pie(values=total_amounts, names=categories)
    fig.update_layout(title_text="Total amount per category")

    return fig
