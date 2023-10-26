from django.db import models


class Stock(models.Model):
    stock_name = models.CharField(max_length=255, null=False, blank=False, default='Existencias')
    stock_quantity = models.IntegerField(null=False, blank=False)
    stock_unitPrice = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=False, blank=False)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, blank=False)

    def __str__(self):
        return ' Cantidad: ' + str(
            self.stock_quantity) + ' Precio Unitario: ' + str(
            self.stock_unitPrice) \
            + ' Precio: ' + str(self.stock_price)


class Move(models.Model):
    move_date = models.DateField(null=False, blank=False)
    move_description = models.CharField(max_length=255, null=False,
                                        blank=True)
    move_type = models.CharField(max_length=10, null=False, blank=False)
    move_quantity = models.IntegerField(null=False, blank=False)
    move_unitPrice = models.DecimalField(max_digits=10, decimal_places=2,
                                         null=False, blank=False)
    move_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     null=False, blank=False)
    stock_quantity = models.IntegerField(null=False, blank=False,default=0)
    stock_unitPrice = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=False, blank=False, default=0)
    stock_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, blank=False, default=0)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False,
                              blank=False)

    def __str__(self):
        return 'fecha: ' + str(self.move_date) + ' movimiento: ' + \
            self.move_description + self.stock.__str__()
