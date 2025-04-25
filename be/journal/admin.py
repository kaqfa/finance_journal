from django.contrib import admin
from journal.models.master import Sekuritas, Sector, Asset, Dividend
from journal.models.transaction import Account, Portfolio, TopupWithdraw, Investment, Trading, Transaction

@admin.register(Sekuritas)
class SekuritasAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'asset_type', 'sector', 'last_price', 'last_update', 'price_check', 'dividend_check')
    list_filter = ('asset_type', 'sector', 'price_check', 'dividend_check')
    search_fields = ('name', 'code')
    readonly_fields = ('last_update',)

@admin.register(Dividend)
class DividendAdmin(admin.ModelAdmin):
    list_display = ('asset', 'amount', 'payment_date', 'type', 'status')
    list_filter = ('type', 'status', 'payment_date')
    search_fields = ('asset__name', 'asset__code')
    date_hierarchy = 'payment_date'

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'sekuritas', 'username')
    list_filter = ('sekuritas',)
    search_fields = ('user__username', 'sekuritas__name', 'username')

class InvestmentInline(admin.TabularInline):
    model = Investment
    extra = 1
    fields = ('asset', 'avg_price', 'goal_desc', 'strategy')

class TradingInline(admin.TabularInline):
    model = Trading
    extra = 1
    fields = ('asset', 'tp_plan', 'cl_plan', 'realized_pl', 'reasons', 'strategy')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'account', 'description')
    list_filter = ('account__sekuritas',)
    search_fields = ('name', 'user__username', 'account__sekuritas__name')
    inlines = [InvestmentInline, TradingInline]

@admin.register(TopupWithdraw)
class TopupWithdrawAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'type', 'trans_date')
    list_filter = ('type', 'trans_date', 'account__sekuritas')
    search_fields = ('account__user__username', 'account__sekuritas__name')
    date_hierarchy = 'trans_date'

class TransactionInvestmentInline(admin.TabularInline):
    model = Transaction
    extra = 1
    fields = ('transaction_type', 'quantity', 'price', 'transaction_date', 'fees')
    fk_name = 'investment'
    verbose_name = "Investment Transaction"
    verbose_name_plural = "Investment Transactions"

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'asset', 'avg_price')
    list_filter = ('asset__asset_type', 'portfolio__account__sekuritas')
    search_fields = ('portfolio__name', 'asset__name', 'asset__code')
    inlines = [TransactionInvestmentInline]

class TransactionTradingInline(admin.TabularInline):
    model = Transaction
    extra = 1
    fields = ('transaction_type', 'quantity', 'price', 'transaction_date', 'fees')
    fk_name = 'trading'
    verbose_name = "Trading Transaction"
    verbose_name_plural = "Trading Transactions"

@admin.register(Trading)
class TradingAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'asset', 'tp_plan', 'cl_plan', 'realized_pl')
    list_filter = ('asset__asset_type', 'portfolio__account__sekuritas')
    search_fields = ('portfolio__name', 'asset__name', 'asset__code', 'reasons', 'strategy')
    inlines = [TransactionTradingInline]

# Hapus registrasi admin untuk Transaction karena sekarang sudah menjadi inline
# di Investment dan Trading