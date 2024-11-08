
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tracker.filter import TransactionFilter
from tracker.forms import TransactionForm
from tracker.models import Transaction


# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transaction_list(request):
    transactions = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    expenses = transactions.qs.get_total_income()
    income = transactions.qs.get_total_expense()
    net_income = income - expenses

    context = {
        'filter': transactions,
        'expense': expenses,
        'income': income,
        'net_income': net_income,
    }
    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)

    return render(request, 'tracker/transactions-list.html', context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': 'Transaction created'}
            return render(request, 'tracker/partials/transactions-success.html', context)

    context = {
        'form': TransactionForm(),
    }

    return render(request, 'tracker/partials/create-transactions.html', context)