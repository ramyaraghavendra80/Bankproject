from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import AccountForm, ProfileUpdateForm, UserRegistrationForm, BankTransferForm, SelfTransferForm, MobileRechargeForm, BillPaymentForm, RecipientForm, ContactForm
from .models import Account, Profile, Recipient, Transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class SignupView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet to set password
            user.set_password(form.cleaned_data['password'])
            user.save()  # Save the user

            # Create the profile
            Profile.objects.create(user=user)

            # Log the user in after successful signup
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('add_account')  # Redirect to the add_account view

        # If the form is invalid, render the signup page with the form errors
        return render(request, 'signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        # Display the login form
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            # Change 'home' to the appropriate redirect view name
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'profile.html', {
            'user': request.user,
            'profile': profile,
            'editable': False
        })


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileUpdateForm(instance=profile)
        return render(request, 'profile.html', {
            'form': form,
            'editable': True,
            'user': request.user,
            'profile': profile
        })

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, 'profile.html', {
            'form': form,
            'editable': True,
            'user': request.user,
            'profile': profile
        })


@method_decorator(login_required, name='dispatch')
class AddAccountView(View):
    def get(self, request):
        form = AccountForm()
        return render(request, 'add_account.html', {'form': form})

    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Associate account with the logged-in user
            account.save()
            messages.success(request, "Account added successfully!")
            # Redirect to account list or any other page
            return redirect('account_list')
        return render(request, 'add_account.html', {'form': form})


class AccountListView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Get accounts for the logged-in user
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_list.html', {'accounts': accounts})


class AccountdetailsView(View):
    @method_decorator(login_required)
    def get(self, request):
        account = get_object_or_404(Account, user=request.user)
        form = AccountForm(instance=account)
        context = {
            'account': account,
            'form': form
        }
        return render(request, 'account_details.html', context)


class AddRecipientView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = RecipientForm()
        return render(request, 'add_recipient.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = RecipientForm(request.POST)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.user = request.user  # Associate with the logged-in user
            recipient.save()
            messages.success(request, "Recipient added successfully.")
            # Redirect to the bank transfer page after adding the recipient
            return redirect('bank_transfer')
        return render(request, 'add_recipient.html', {'form': form})


# views.py
class BankTransferView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = BankTransferForm(user=request.user)  # Pass the user to the form
        return render(request, 'bank_transfer.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        # Pass the user to the form
        form = BankTransferForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'bank_transfer'
            transaction.description = f"Bank transfer to {form.cleaned_data['recipient'].name}"
            transaction.save()
            messages.success(
                request, f"Amount {transaction.amount} transferred to {form.cleaned_data['recipient'].name}.")
            return redirect('transaction_history')

        return render(request, 'bank_transfer.html', {'form': form})


class TransactionHistoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user).order_by('-date')
        return render(request, 'transaction_history.html', {'transactions': transactions})


class BillPaymentView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = BillPaymentForm()
        return render(request, 'bill_payment.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_payment = form.save(commit=False)
            bill_payment.user = request.user
            bill_payment.save()

            # Log the transaction in the Transaction model
            Transaction.objects.create(
                user=request.user,
                amount=bill_payment.amount,
                transaction_type='bill_payment',
                description=f"{bill_payment.get_bill_type_display()} bill payment",
            )

            messages.success(request, "Bill payment was successful.")
            return redirect('transaction_history')

        return render(request, 'bill_payment.html', {'form': form})


class MobileRechargeView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = MobileRechargeForm()
        return render(request, 'mobile_recharge.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = MobileRechargeForm(request.POST)
        if form.is_valid():
            mobile_recharge = form.save(commit=False)
            mobile_recharge.user = request.user
            mobile_recharge.save()

            # Log the transaction in the Transaction model
            Transaction.objects.create(
                user=request.user,
                amount=mobile_recharge.amount,
                transaction_type='mobile_recharge',
                description=f"Mobile recharge for {mobile_recharge.mobile_number} - {mobile_recharge.operator}",
            )

            messages.success(request, "Mobile recharge was successful.")
            return redirect('transaction_history')

        return render(request, 'mobile_recharge.html', {'form': form})


class SelfTransferView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = SelfTransferForm(user=request.user)
        return render(request, 'self_transfer.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = SelfTransferForm(user=request.user, data=request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            destination_account = form.cleaned_data['destination_account']
            amount = form.cleaned_data['amount']

            # Check if source account has sufficient funds
            if source_account.balance < amount:
                messages.error(
                    request, "Insufficient funds in source account.")
                return redirect('self_transfer')

            # Perform the transfer
            source_account.balance -= amount
            destination_account.balance += amount
            source_account.save()
            destination_account.save()

            # Log the transaction
            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='self_transfer',
                description=f"Transfer from {source_account.account_number} to {destination_account.account_number}",
            )

            messages.success(request, "Transfer completed successfully.")
            return redirect('transaction_history')

        return render(request, 'self_transfer.html', {'form': form})


class ContactUsView(View):
    template_name = 'contact_us.html'
    # Redirect URL after form submission
    success_url = reverse_lazy('contact_us')

    def get(self, request):
        form = ContactForm()  # Initialize an empty form for GET requests
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data to the database
            messages.success(
                request, "Your message has been sent successfully!")
            return redirect(self.success_url)
        else:
            # If the form is invalid, re-render with errors
            return render(request, self.template_name, {'form': form})
