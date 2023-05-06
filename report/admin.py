from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, MustPay, MustPayReceipt, Recipient, Alimony, Currency, RecipientChild


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'id')
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(MustPayReceipt)
class MustPayReceiptAdmin(admin.ModelAdmin):
    list_display = ('must_pay', 'last_payment', 'last_payment_date', 'currency', 'photo')
    list_display_links = ('must_pay',)


@admin.register(MustPay)
class MustPayAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday', 'created')
    list_display_links = ('first_name',)
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


@admin.register(RecipientChild)
class RecipientChildAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'first_name', 'last_name', 'birthday')
    list_display_links = ('recipient', )
    

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday')
    list_display_links = ('first_name',)
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


@admin.register(Alimony)
class AlimonyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'executor',
        'ruling',
        'ruling_date',
        'must_pay',
        'recipient',
        'note',
        'status'
    )
    list_display_links = ('executor', 'ruling', 'must_pay', 'recipient')
    prepopulated_fields = {'slug': ('user', 'must_pay')}

