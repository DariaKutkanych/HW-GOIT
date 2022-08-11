from tkinter import CASCADE
from django.db import models

class Transaction(models.Model):

    name = models.CharField(max_length=50, null=False)
    expense = models.BooleanField()

    def __str__(self):
        return self.name


class Entry(models.Model):

    amount = models.FloatField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.amount} {self.transaction} {self.created}"

