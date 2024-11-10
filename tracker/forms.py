from django import forms
from django.views.generic.edit import UpdateView
from tracker.models import Transaction, Category


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect,
    )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount < 0:
            raise forms.ValidationError("Amount must be positive")

        return amount

    class Meta:
        model = Transaction
        fields = (
            "type",
            "amount",
            "date",
            "category",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class TransactionFormUpdate(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "/tracker/partials/transactions-update.html"
    success_url = "transactions/"

