from django.forms import ModelForm
from .models import Account, Transaction


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['code', 'name', 'category']


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_date', 'account', 'transaction_type',
                  'transaction_description']
