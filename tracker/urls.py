from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name="index"),
    path("transactions/", views.transaction_list, name="transactions-list"),
    path("transactions/create", views.create_transaction, name="create-transaction"),
    path(
        "transactions/<int:id>/update/",
        views.update_transaction,
        name="update-transaction",
    ),
    path(
        "transactions/<int:id>/delete/",
        views.delete_transaction,
        name="delete-transaction",
    ),
    path("get-transaction/", views.get_transaction, name="get-transaction"),
    path("transactions-chart/", views.transactions_chart, name="transactions-chart"),
]
