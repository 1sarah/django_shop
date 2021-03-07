from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    code = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name='orders', blank=True, null=True)

    item = models.CharField(max_length=250, null=True)
    amount = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.item


