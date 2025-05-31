# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FinanceCategory(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'finance_category'
        unique_together = (('user', 'name'),)


class FinanceTag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'finance_tag'
        unique_together = (('user', 'name'),)


class FinanceTransaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    type = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    transaction_date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category = models.ForeignKey(FinanceCategory, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    wallet = models.ForeignKey('FinanceWallet', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'finance_transaction'


class FinanceTransactiontag(models.Model):
    tag = models.ForeignKey(FinanceTag, models.DO_NOTHING)
    transaction = models.ForeignKey(FinanceTransaction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'finance_transactiontag'
        unique_together = (('transaction', 'tag'),)


class FinanceTransfer(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    fee = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transaction = models.OneToOneField(FinanceTransaction, models.DO_NOTHING)
    from_wallet = models.ForeignKey('FinanceWallet', models.DO_NOTHING)
    to_wallet = models.ForeignKey('FinanceWallet', models.DO_NOTHING, related_name='financetransfer_to_wallet_set')

    class Meta:
        managed = False
        db_table = 'finance_transfer'


class FinanceWallet(models.Model):
    name = models.CharField(max_length=100)
    wallet_type = models.CharField(max_length=10)
    currency = models.CharField(max_length=5)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    current_balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'finance_wallet'
        unique_together = (('user', 'name'),)


class JournalAccount(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    sekuritas = models.ForeignKey('JournalSekuritas', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_account'


class JournalAsset(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    endpoint_url = models.CharField(max_length=200, blank=True, null=True)
    asset_type = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    last_update = models.DateTimeField()
    price_check = models.BooleanField()
    dividend_check = models.BooleanField()
    sector = models.ForeignKey('JournalSector', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_asset'


class JournalDividend(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    payment_date = models.DateField()
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    asset = models.ForeignKey(JournalAsset, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_dividend'


class JournalInvestment(models.Model):
    avg_price = models.IntegerField()
    goal_desc = models.TextField(blank=True, null=True)
    strategy = models.TextField(blank=True, null=True)
    asset = models.ForeignKey(JournalAsset, models.DO_NOTHING)
    portfolio = models.ForeignKey('JournalPortfolio', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_investment'


class JournalPortfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    account = models.ForeignKey(JournalAccount, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_portfolio'


class JournalSector(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'journal_sector'


class JournalSekuritas(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'journal_sekuritas'


class JournalTopupwithdraw(models.Model):
    amount = models.IntegerField()
    type = models.CharField(max_length=10)
    trans_date = models.DateTimeField()
    account = models.ForeignKey(JournalAccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_topupwithdraw'


class JournalTrading(models.Model):
    tp_plan = models.IntegerField()
    cl_plan = models.IntegerField()
    realized_pl = models.IntegerField()
    reasons = models.CharField(max_length=255, blank=True, null=True)
    strategy = models.CharField(max_length=255, blank=True, null=True)
    asset = models.ForeignKey(JournalAsset, models.DO_NOTHING)
    portfolio = models.ForeignKey(JournalPortfolio, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'journal_trading'


class JournalTransaction(models.Model):
    quantity = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    transaction_type = models.CharField(max_length=10)
    transaction_date = models.DateTimeField()
    fees = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    investment = models.ForeignKey(JournalInvestment, models.DO_NOTHING, blank=True, null=True)
    trading = models.ForeignKey(JournalTrading, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'journal_transaction'


class TokenBlacklistBlacklistedtoken(models.Model):
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'
