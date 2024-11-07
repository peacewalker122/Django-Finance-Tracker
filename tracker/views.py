from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tracker.filter import TransactionFilter
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

    context = {'filter': transactions}
    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)

    return render(request, 'tracker/transactions-list.html', context)