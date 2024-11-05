from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    aadhar = models.CharField(max_length=12, blank=True, null=True)
    pan = models.CharField(max_length=10, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    residence_phone = models.CharField(max_length=15, blank=True, null=True)
    office_phone = models.CharField(max_length=15, blank=True, null=True)
    mailing_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    kyc_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Account(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts")  # Allow multiple accounts per user
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    bank_name = models.CharField(max_length=100)  # New field for bank name

    def __str__(self):
        return f"{self.user.username}'s Account {self.account_number} ({self.bank_name})"


class Recipient(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipients")
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.name} ({self.account_number})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('bank_transfer', 'Bank Transfer'),
        ('bill_payment', 'Bill Payment'),
        ('mobile_recharge', 'Mobile Recharge'),
        ('self_transfer', 'Self Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        Recipient, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} to {self.recipient} on {self.date}"


class BillPayment(models.Model):
    BILL_TYPES = (
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('rent', 'Rent'),
        ('mobile', 'Mobile Recharge'),
        # Add more bill types as needed
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPES)
    trasaction_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill_type} bill payment of {self.amount} by {self.user.username}"


class MobileRecharge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    operator = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mobile_number} - {self.operator} - Rs.{self.amount}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"