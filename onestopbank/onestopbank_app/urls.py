from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SignupView, LoginView, LogoutView, ProfileView, UpdateProfileView, HomeView, AddAccountView, AccountdetailsView, BankTransferView, TransactionHistoryView, BillPaymentView, MobileRechargeView,  SelfTransferView, AccountListView, AddRecipientView, ContactUsView


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='SignupView'),
    path('logout/', LogoutView.as_view(), name='LogoutView'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='UpdateProfileView'),
    path('add-account/', AddAccountView.as_view(), name='add_account'),
    path('accounts/', AccountListView.as_view(), name='account_list'),
    path('add_recipient/', AddRecipientView.as_view(), name='add_recipient'),
    path('bank_transfer/', BankTransferView.as_view(), name='bank_transfer'),
    path('transaction_history/', TransactionHistoryView.as_view(),
         name='transaction_history'),
    path('bill_payment/', BillPaymentView.as_view(), name='bill_payment'),
    path('mobile_recharge/', MobileRechargeView.as_view(), name='mobile_recharge'),
    path('self_transfer/', SelfTransferView.as_view(), name='self_transfer'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
