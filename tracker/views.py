from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django_htmx.http import retarget

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

    expenses = transactions.queryset.get_total_expense()
    income = transactions.queryset.get_total_income()
    net_income = income - expenses

    context = {
        "filter": transactions,
        "expense": expenses,
        "income": income,
        "net_income": net_income,
    }
    if request.htmx:
        return render(request, "tracker/partials/transactions-container.html", context)

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
