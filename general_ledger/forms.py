from django.forms import ModelForm
from .models import Account, Transaction, Ledger


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['code', 'name', 'category']


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_date', 'account', 'transaction_type',
                  'transaction_description']


class LedgerForm(ModelForm):
    class Meta:
        model = Ledger
        fields = ['start_date', 'end_date']
