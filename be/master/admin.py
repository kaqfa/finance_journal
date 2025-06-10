from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import User, RegToken


@admin.register(RegToken)
class RegTokenAdmin(admin.ModelAdmin):
    """
    Admin interface untuk Registration Token
    """
    list_display = [
        'name', 
        'token_code', 
        'is_active_display',
        'usage_display', 
        'expires_display',
        'created_at_display',
        'registered_users_count'
    ]
    list_filter = [
        'is_active', 
        'created_at',
        'expires_at'
    ]
    search_fields = [
        'name', 
        'token_code', 
        'created_by',
        'notes'
    ]
    readonly_fields = [
        'id',
        'current_usage',
        'created_at',
        'registered_users_count',
        'validation_status'
    ]
    
    fieldsets = (
        ('Token Information', {
            'fields': (
                'id',
                'name',
                'token_code',
                'notes'
            )
        }),
        ('Token Settings', {
            'fields': (
                'is_active',
                'max_usage',
                'current_usage',
                'expires_at'
            )
        }),
        ('Metadata', {
            'fields': (
                'created_by',
                'created_at',
                'validation_status'
            )
        }),
        ('Usage Statistics', {
            'fields': (
                'registered_users_count',
            )
        })
    )
    
    def is_active_display(self, obj):
        """Display active status with color"""
        if obj.is_active:
            return format_html(
                '<span style="color: green;">✅ Active</span>'
            )
        return format_html(
            '<span style="color: red;">❌ Inactive</span>'
        )
    is_active_display.short_description = 'Status'
    
    def usage_display(self, obj):
        """Display usage with progress"""
        if obj.max_usage == 0:
            return format_html(
                '<span style="color: blue;">{}/Unlimited</span>',
                obj.current_usage
            )
        
        percentage = (obj.current_usage / obj.max_usage) * 100 if obj.max_usage > 0 else 0
        color = 'green' if percentage < 80 else 'orange' if percentage < 100 else 'red'
        
        return format_html(
            '<span style="color: {};">{}/{} ({}%)</span>',
            color,
            obj.current_usage,
            obj.max_usage,
            int(percentage)
        )
    usage_display.short_description = 'Usage'
    
    def expires_display(self, obj):
        """Display expiry status"""
        if not obj.expires_at:
            return format_html('<span style="color: blue;">No Expiry</span>')
        
        now = timezone.now()
        if obj.expires_at > now:
            diff = obj.expires_at - now
            days = diff.days
            if days > 30:
                return format_html(
                    '<span style="color: green;">Expires in {} days</span>',
                    days
                )
            elif days > 7:
                return format_html(
                    '<span style="color: orange;">Expires in {} days</span>',
                    days
                )
            else:
                return format_html(
                    '<span style="color: red;">Expires in {} days</span>',
                    days
                )
        else:
            return format_html('<span style="color: red;">❌ Expired</span>')
    expires_display.short_description = 'Expiry'
    
    def created_at_display(self, obj):
        """Display created date in nice format"""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = 'Created'
    
    def registered_users_count(self, obj):
        """Count of users registered with this token"""
        count = obj.registered_users.count()
        if count > 0:
            return format_html(
                '<a href="/admin/master/user/?reg_token__id__exact={}">{} users</a>',
                obj.id,
                count
            )
        return '0 users'
    registered_users_count.short_description = 'Registered Users'
    
    def validation_status(self, obj):
        """Show token validation status"""
        is_valid, message = obj.is_valid()
        if is_valid:
            return format_html('<span style="color: green;">✅ {}</span>', message)
        return format_html('<span style="color: red;">❌ {}</span>', message)
    validation_status.short_description = 'Validation Status'
    
    # Custom actions
    actions = ['activate_tokens', 'deactivate_tokens', 'reset_usage']
    
    def activate_tokens(self, request, queryset):
        """Activate selected tokens"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} token(s) berhasil diaktifkan.'
        )
    activate_tokens.short_description = 'Activate selected tokens'
    
    def deactivate_tokens(self, request, queryset):
        """Deactivate selected tokens"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} token(s) berhasil dinonaktifkan.'
        )
    deactivate_tokens.short_description = 'Deactivate selected tokens'
    
    def reset_usage(self, request, queryset):
        """Reset usage counter for selected tokens"""
        updated = queryset.update(current_usage=0)
        self.message_user(
            request,
            f'Usage counter untuk {updated} token(s) berhasil direset.'
        )
    reset_usage.short_description = 'Reset usage counter'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Enhanced User Admin dengan Registration Token support
    """
    # Fields to display in list view
    list_display = [
        'username',
        'full_name', 
        'email',
        'reg_token_display',
        'is_active',
        'is_staff',
        'date_joined_display'
    ]
    
    # Add filters
    list_filter = BaseUserAdmin.list_filter + (
        'reg_token',
        'created_at',
    )
    
    # Add search fields
    search_fields = BaseUserAdmin.search_fields + (
        'full_name',
        'phone',
        'reg_token__name',
        'reg_token__token_code',
    )
    
    # Readonly fields
    readonly_fields = BaseUserAdmin.readonly_fields + (
        'id',
        'created_at',
        'updated_at',
    )
    
    # Custom fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Registration Info', {
            'fields': (
                'reg_token',
                'phone',
                'created_at',
                'updated_at',
            )
        }),
        ('System Info', {
            'fields': (
                'id',
            )
        }),
    )
    
    # Add fieldsets for creating user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'reg_token',
            )
        }),
    )
    
    def reg_token_display(self, obj):
        """Display registration token info"""
        if obj.reg_token:
            return format_html(
                '<span style="color: blue;" title="{}">{}</span>',
                obj.reg_token.token_code,
                obj.reg_token.name
            )
        return format_html('<span style="color: gray;">No Token</span>')
    reg_token_display.short_description = 'Reg Token'
    
    def date_joined_display(self, obj):
        """Display join date in nice format"""
        return obj.date_joined.strftime('%Y-%m-%d')
    date_joined_display.short_description = 'Joined'
    
    # Custom actions
    actions = ['assign_token', 'remove_token']
    
    def assign_token(self, request, queryset):
        """Assign token to selected users"""
        # This would open a form to select token, simplified here
        self.message_user(
            request,
            'Use individual user edit to assign tokens.'
        )
    assign_token.short_description = 'Assign registration token'
    
    def remove_token(self, request, queryset):
        """Remove token from selected users"""
        updated = queryset.update(reg_token=None)
        self.message_user(
            request,
            f'Registration token removed from {updated} user(s).'
        )
    remove_token.short_description = 'Remove registration token'
