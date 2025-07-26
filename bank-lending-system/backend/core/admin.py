from django.contrib import admin
from .models import Customer, Loan, Payment
# Register your models here.

admin.site.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'created_at')
admin.site.register(Loan)
admin.site.register(Payment)
