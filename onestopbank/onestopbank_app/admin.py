from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Account,Recipient, Transaction, BillPayment


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Unregister the default User admin
admin.site.unregister(User)
# Register the new User admin with Profile inline
admin.site.register(User, UserAdmin)

# Optionally register Profile if you want to manage it separately as well
admin.site.register(Profile)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance')
    search_fields = ('user__username', 'account_number')
    list_filter = ('balance',)


admin.site.register(Account, AccountAdmin)

# admin.site.register(BillPayment)

admin.site.register(Recipient)
admin.site.register(Transaction)
admin.site.register(BillPayment)
