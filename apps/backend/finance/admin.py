from django.contrib import admin
from finance.models import Category, Wallet, Transaction, Transfer, Tag, TransactionTag
from django.db.models import Sum
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user', 'icon_display', 'created_at')
    list_filter = ('type', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'created_at'
    
    def icon_display(self, obj):
        if obj.icon and obj.color:
            return format_html('<span style="color: {};">⬤ {}</span>', obj.color, obj.icon)
        elif obj.icon:
            return obj.icon
        return '-'
    icon_display.short_description = 'Icon'

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'wallet_type', 'user', 'currency', 'initial_balance', 'current_balance', 'is_active', 'created_at')
    list_filter = ('wallet_type', 'is_active', 'currency', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    readonly_fields = ('current_balance', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['recalculate_balances']
    
    def recalculate_balances(self, request, queryset):
        for wallet in queryset:
            wallet.update_balance()
        self.message_user(request, f"Successfully recalculated balances for {queryset.count()} wallets.")
    recalculate_balances.short_description = "Recalculate balances for selected wallets"

class TransactionTagInline(admin.TabularInline):
    model = TransactionTag
    extra = 1

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'wallet', 'category', 'amount', 'type', 'transaction_date', 'created_at')
    list_filter = ('type', 'transaction_date', 'wallet', 'category', 'user')
    search_fields = ('description', 'user__username', 'wallet__name', 'category__name')
    date_hierarchy = 'transaction_date'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TransactionTagInline]
    
    fieldsets = (
        (None, {
            'fields': ('user', 'wallet', 'category', 'amount', 'type')
        }),
        ('Additional Information', {
            'fields': ('description', 'transaction_date', 'created_at', 'updated_at')
        }),
    )

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'from_wallet', 'to_wallet', 'amount', 'fee', 'get_transaction_date', 'created_at')
    list_filter = ('from_wallet', 'to_wallet', 'created_at')
    search_fields = ('from_wallet__name', 'to_wallet__name', 'transaction__description')
    readonly_fields = ('transaction', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def get_transaction_date(self, obj):
        return obj.transaction.transaction_date if obj.transaction else None
    get_transaction_date.short_description = 'Transaction Date'
    get_transaction_date.admin_order_field = 'transaction__transaction_date'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'get_usage_count')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'user__username')
    
    def get_usage_count(self, obj):
        return obj.transaction_tags.count()
    get_usage_count.short_description = 'Usage Count'

@admin.register(TransactionTag)
class TransactionTagAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'tag')
    list_filter = ('tag', 'transaction__type')
    search_fields = ('tag__name', 'transaction__description')