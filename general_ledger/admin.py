from django.contrib import admin
from .models import Category, Account, Transaction, Ledger

admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Ledger)
