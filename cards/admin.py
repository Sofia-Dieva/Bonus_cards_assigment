from django.contrib import admin
from .models import Purchase, BonusCard

@admin.register(BonusCard)
class BonusCardAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'expiry',
        'date_time',
        'updated_at',
        'sum_of_bonus',
        'status',
    )

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'card',
        'bill',
        'name',
        'shopping_date',
    )
