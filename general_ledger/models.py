from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.category_name


class Catalog(models.Model):
    catalog_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.catalog_name


class Account(models.Model):
    account_code = models.CharField(max_length=10, null=False)
    account_name = models.CharField(max_length=255, null=False)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=False)
    catalog = models.ForeignKey(Catalog,
                                on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account_code} - {self.account_name}'


class Ledger(models.Model):
    catalog = models.ForeignKey(Catalog,
                                on_delete=models.CASCADE)

    def __str__(self):
        return str(self.catalog)


class Journal(models.Model):
    ledger = models.ForeignKey(Ledger,
                               on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ledger)


class IVAType(models.Model):
    iva_type_name = models.CharField(max_length=255, null=False)
    iva_type_percentage = models.DecimalField(max_digits=5, decimal_places=2,
                                              null=False)
    transaction = models.ForeignKey('Transaction', on_delete=models.SET_NULL,
                                    related_name='iva_types', null=True)

    def __str__(self):
        return self.iva_type_name


class Transaction(models.Model):
    transaction_date = models.DateField(auto_now=True, null=False)
    transaction_debit = models.DecimalField(max_digits=10, decimal_places=2,
                                            null=True,
                                            blank=True)
    transaction_credit = models.DecimalField(max_digits=10, decimal_places=2,
                                             null=True,
                                             blank=True)
    transaction_description = models.CharField(max_length=255, null=False,
                                               blank=True)
    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE)
    journal = models.ForeignKey(Journal,
                                on_delete=models.CASCADE)
    iva_type = models.ForeignKey(IVAType, on_delete=models.SET_NULL,
                                 related_name='iva_types', null=True)

    def __str__(self):
        return f'{self.transaction_date} - {self.transaction_description}'
