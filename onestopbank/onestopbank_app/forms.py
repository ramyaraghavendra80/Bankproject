from django import forms
from django.contrib.auth.models import User
from .models import Profile, Account, BillPayment, Recipient, Transaction, MobileRecharge,Contact


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user)  # Create the profile
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_pic', 'dob', 'aadhar', 'pan', 'contact_email',
            'mobile', 'residence_phone', 'office_phone',
            'mailing_address', 'permanent_address', 'kyc_status'
        ]


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'balance', 'bank_name']


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'account_number', 'ifsc_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter recipient name'})
        self.fields['account_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter account number'})
        self.fields['ifsc_code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter IFSC code (optional)'})

class BankTransferForm(forms.ModelForm):
    sender_account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Sender Account")

    class Meta:
        model = Transaction
        fields = ['recipient', 'amount', 'sender_account']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['sender_account'].queryset = Account.objects.filter(user=user)

class BillPaymentForm(forms.ModelForm):
    sender_account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Sender Account")

    class Meta:
        model = BillPayment
        fields = ['bill_type', 'amount', 'sender_account']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['sender_account'].queryset = Account.objects.filter(user=user)

class MobileRechargeForm(forms.ModelForm):
    sender_account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Sender Account")

    class Meta:
        model = MobileRecharge
        fields = ['mobile_number', 'operator', 'amount','sender_account']
        widgets = {
            'operator': forms.TextInput(attrs={'placeholder': 'e.g., Airtel, Jio, etc.'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter recharge amount'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['sender_account'].queryset = Account.objects.filter(user=user)

class SelfTransferForm(forms.Form):
    source_account = forms.ModelChoiceField(
        queryset=Account.objects.none(), label="Source Account")
    destination_account = forms.ModelChoiceField(
        queryset=Account.objects.none(), label="Destination Account")
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=1, label="Amount")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_account'].queryset = Account.objects.filter(
            user=user)
        self.fields['destination_account'].queryset = Account.objects.filter(
            user=user)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }