import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone


class RegToken(models.Model):
    """
    Model untuk Registration Token - Limited Access Control
    
    Token ini digunakan untuk mengontrol siapa yang bisa mendaftar ke sistem.
    Admin akan membuat token secara manual melalui Django Admin.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, 
        help_text="Nama/deskripsi token (misal: Batch Alpha Tester, Internal Team, dll)"
    )
    token_code = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Kode token unik yang akan digunakan untuk registrasi"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Status token - hanya token aktif yang bisa digunakan untuk registrasi"
    )
    max_usage = models.PositiveIntegerField(
        default=1,
        help_text="Maksimal berapa kali token ini bisa digunakan (0 = unlimited)"
    )
    current_usage = models.PositiveIntegerField(
        default=0,
        help_text="Berapa kali token ini sudah digunakan"
    )
    expires_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Tanggal kadaluarsa token (kosongkan jika tidak ada)"
    )
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Siapa yang membuat token ini"
    )
    notes = models.TextField(
        blank=True,
        help_text="Catatan tambahan tentang token ini"
    )

    class Meta:
        db_table = 'reg_tokens'
        verbose_name = 'Registration Token'
        verbose_name_plural = 'Registration Tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.token_code})"
    
    def is_valid(self):
        """
        Cek apakah token masih valid untuk digunakan
        """
        # Token harus aktif
        if not self.is_active:
            return False, "Token tidak aktif"
        
        # Cek expiry date
        if self.expires_at and timezone.now() > self.expires_at:
            return False, "Token sudah kadaluarsa"
        
        # Cek usage limit (0 = unlimited)
        if self.max_usage > 0 and self.current_usage >= self.max_usage:
            return False, "Token sudah mencapai batas maksimal penggunaan"
        
        return True, "Token valid"
    
    def use_token(self):
        """
        Gunakan token (increment usage counter)
        """
        self.current_usage += 1
        self.save(update_fields=['current_usage'])
    
    @property
    def remaining_usage(self):
        """
        Sisa penggunaan token
        """
        if self.max_usage == 0:
            return "Unlimited"
        return max(0, self.max_usage - self.current_usage)


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        # Handle full_name jika dikirim dari frontend/API
        if 'full_name' in extra_fields:
            full_name = extra_fields.pop('full_name')
            if full_name and not (extra_fields.get('first_name') or extra_fields.get('last_name')):
                # Split full_name jika first_name/last_name kosong
                name_parts = full_name.split(' ', 1)
                extra_fields['first_name'] = name_parts[0]
                extra_fields['last_name'] = name_parts[1] if len(name_parts) > 1 else ''
        
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User Model dengan Registration Token Support
    """
    # Override primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # AbstractUser udah include:
    # - username, first_name, last_name, email
    # - is_staff, is_active, date_joined
    # - groups, user_permissions (dari PermissionsMixin)
    
    # Tambahan field custom
    full_name = models.CharField(max_length=255, blank=True)  # Keep existing full_name
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Registration token reference
    reg_token = models.ForeignKey(
        RegToken,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registered_users',
        help_text="Token registrasi yang digunakan untuk mendaftar"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    # USERNAME_FIELD dan REQUIRED_FIELDS udah di-set di AbstractUser
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # email ditambah ke required

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Auto-update full_name berdasarkan first_name + last_name
        if self.first_name or self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
