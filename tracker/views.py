from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django_htmx.http import retarget

from finance_project import settings
from tracker.charting import plot_category_pie_chart, plot_income_expenses_bar_chart
from tracker.filter import TransactionFilter
from tracker.forms import TransactionForm
from tracker.models import Transaction


# Create your views here.
def index(request):
    return render(request, "tracker/index.html")


@login_required
def transaction_list(request):
    transactions = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )

    paginator = Paginator(transactions.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(1)  # by default return the first page

    expenses = transactions.queryset.get_total_expense()
    income = transactions.queryset.get_total_income()
    net_income = income - expenses

    context = {
        "transactions": transaction_page,
        "filter": transactions,
        "expense": expenses,
        "income": income,
        "net_income": net_income,
    }

    if request.htmx:
        return render(
            request,
            "tracker/partials/transactions-container.html",
            context,
        )

    return render(request, "tracker/transactions-list.html", context)


@login_required
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {"message": "Transaction created"}
            return render(
                request, "tracker/partials/transactions-success.html", context
            )
        else:
            context = {"form": form}
            response = render(
                request, "tracker/partials/create-transactions.html", context
            )
            return retarget(response, "#transaction-block")

    context = {
        "form": TransactionForm(),
    }

    return render(request, "tracker/partials/create-transactions.html", context)


@login_required  # type: ignore
def update_transaction(request, id):
    instance = get_object_or_404(Transaction, pk=id, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=instance)

        if form.is_valid():
            transastion = form.save(commit=False)
            transastion.save()

            return HttpResponse("Transaction updated")
        else:
            context = {"form": form, "instance": instance}
            response = render(
                request, "tracker/partials/update-transactions.html", context
            )
            return retarget(response, "#transactions_modal_content")

    else:
        form = TransactionForm(instance=instance)

    context = {
        "form": form,
        "instance": instance,
    }

    return render(request, "tracker/partials/update-transactions.html", context)


@login_required  # type: ignore
@require_http_methods(["DELETE"])
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, pk=id, user=request.user)
    transaction.delete()

    context = {"message": "Transaction deleted"}

    return render(request, "tracker/partials/transactions-success.html", context)


@login_required  # type: ignore
def get_transaction(request):
    transactions = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )
    page: int = request.GET.get("page", 1)
    paginator = Paginator(transactions.qs, settings.PAGE_SIZE)

    context = {
        "transactions": paginator.page(page),
    }

    return render(
        request,
        "tracker/partials/transactions-container.html#transactions-list",
        context,
    )


@login_required  # type: ignore
def transactions_chart(request):
    transactions = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )

    char = plot_income_expenses_bar_chart(transactions.qs)
    category_income_pie = plot_category_pie_chart(transactions.qs.filter(type="income"))
    category_expense_pie = plot_category_pie_chart(
        transactions.qs.filter(type="expense")
    )

    context = {
        "filter": transactions,
        "chart": char.to_html(),
        "category_income_pie": category_income_pie.to_html(),
        "category_expense_pie": category_expense_pie.to_html(),
    }

    if request.htmx:
        return render(request, "tracker/partials/charts-container.html", context)

    return render(request, "tracker/chart.html", context)
