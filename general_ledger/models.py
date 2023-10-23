from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Catalog(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Account(models.Model):
    code = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                                  blank=False, default=0)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE,
                                null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=False, blank=False)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Ledger(models.Model):
    start_date = models.DateTimeField(null=False)
    end_date = models.DateField(null=False)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.catalog)


class Transaction(models.Model):
    transaction_date = models.DateTimeField(null=False, blank=False)
    transaction_type = models.CharField(max_length=255, null=False,
                                        blank=False)
    transaction_credit_amount = models.DecimalField(max_digits=10,
                                                    decimal_places=2,
                                                    null=False, blank=False,
                                                    default=0)
    transaction_debit_amount = models.DecimalField(max_digits=10,
                                                   decimal_places=2,
                                                   null=False, blank=False,
                                                   default=0)
    transaction_description = models.CharField(max_length=255, null=False,
                                               blank=True, default='')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False,
                                blank=False)
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, null=False,
                               blank=False)

    def __str__(self):
        return f'{self.transaction_date} - {self.transaction_description}'
