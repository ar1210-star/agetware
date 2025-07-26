import uuid
from django.db import models

class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    loan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.5%
    loan_period_years = models.IntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_emi = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    remaining_emi_count = models.IntegerField(default=0)


    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer.name}"

# models.py
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('EMI', 'EMI'),
        ('LUMP_SUM', 'Lump Sum'),
    ]

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} payment of ₹{self.amount} for loan {self.loan.loan_id}"

