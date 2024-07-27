from django.db import models
from decimal import Decimal

class Human(models.Model):
    name = models.CharField(max_length=45)
    isChild = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)

class Event(models.Model):
    name = models.CharField(max_length=45)

class Payment(models.Model):
    token = models.CharField(max_length=6, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    contact = models.ForeignKey(Human, on_delete=models.CASCADE)

class Ticket(models.Model):
    human = models.OneToOneField(Human, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    nights = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    ticketType = models.CharField(max_length=22)

    def price(self):
        price = Decimal(0)
        if self.ticketType == "standard":
            price = Decimal(86)
            if self.human.isChild:
                price = Decimal(33)
        elif self.ticketType == "crew":
            price = Decimal(33) * Decimal(self.nights)
            if self.human.isChild:
                price = Decimal(price) * Decimal(0.5)
        elif not self.ticketType == "custom":
            assert False, f"invalid ticket type {self.ticketType}"

        return Decimal(price)
            

