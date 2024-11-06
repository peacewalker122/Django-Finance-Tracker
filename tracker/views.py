from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracker.models import Transaction


# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}

    return render(request, 'tracker/transactions-list.html', context)