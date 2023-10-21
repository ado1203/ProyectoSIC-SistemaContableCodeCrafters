from django.contrib import admin
from .models import Category, Catalog, Account, Ledger, Transaction

admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Account)
admin.site.register(Ledger)
admin.site.register(Transaction)
