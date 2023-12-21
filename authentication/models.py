from django.contrib import auth
from django.contrib.auth.models import  PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.utils.itercompat import is_iterable
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        first_name = first_name
        last_name = self.last_name
        user = self.model(first_name, last_name,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username = models.CharField(_('Username'), unique=True, max_length=255)
    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=150)
    
    email = models.EmailField(_('E-mail'), unique=True)
    is_staff = models.BooleanField(
        _('Is Staff'),
        default=False,
        help_text=_("Designates whether the user can connect to this Dashboard."),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Indicates whether this user should be treated as active. '
            'Deselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
    
    def __str__(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        if self.first_name and not self.last_name:
            return "%s"%(self.first_name)
        elif self.last_name and not self.first_name:
            return "%s"%(self.last_name)
        else:
            return full_name.strip()
    
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_email(self):
        """
        Return the email.
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
    def user_role(self):
        obj = self.user_staff
        if obj:
            return obj
        else:
            obj = self.user_student
            if obj:
                return obj
            else:
                obj = self.user_applicant
                return obj
        
    def user_position(self):
        obj = self.user_staff
        
        return (obj.position)
        
    def user_profile_picture(self):
        obj = self.user_staff
        
        if obj:
            return (obj.passport_photo)
        else:
            return None
    
    def user_detail(self):
        obj = self.user_staff
        if obj:
            return obj
        else:
            obj = self.user_student
            if obj:
                return obj
            else:
                obj = self.user_driver

    def user_student(self):
        obj = self.user_student

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False
    
class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    # class Meta(AbstractUser.Meta):
    #     swappable = ''AUTH_USER_MODEL

    
class Province(models.Model):
    name = models.CharField(_("province"), max_length=50)
    
    class Meta:
        db_table = "provinces"
        verbose_name = _("province")
        verbose_name_plural = _("provinces")
        ordering = ['name']

    
        def __str__(self):
            return self.name
        
    def __str__(self):
        return self.name

class District(models.Model):
    
    name = models.CharField(_("district"), max_length=50)
    province = models.ForeignKey(
        "Province", 
        db_column = 'province',
        verbose_name=_("Province"), 
        on_delete=models.CASCADE
        )

    class Meta:
        db_table = "districts"
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        ordering = ['name']

    def __str__(self):
        return "%s"%(self.name)

class Sector(models.Model):
    name = models.CharField(_("sector"), max_length=50)
    district = models.ForeignKey(
        "District", 
        db_column = 'district',
        verbose_name=_("District"), 
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'sectors'
        verbose_name = _('sector')
        verbose_name_plural = _('Sectors')
        ordering = ['name']
    
    def __str__(self):
        return "%s - %s"%(self.district.name, self.name)
        
class Cell(models.Model):
    
    name = models.CharField(_("Cell"), max_length=50)
    
    sector = models.ForeignKey(
        "Sector", 
        db_column = 'sector',
        verbose_name=_("Sectors"), 
        on_delete=models.CASCADE
        )

    class Meta:
        db_table = "cells"
        verbose_name = _("Cell")
        verbose_name_plural = _("Cells")
        ordering = ['name']

    def __str__(self):
        return "%s - %s"%(self.sector.name, self.name)
    
class Village(models.Model):
    name = models.CharField(_("Village"), max_length=50)
    cell = models.ForeignKey(
        "Cell", 
        db_column = 'cell',
        verbose_name=_("Cell"), 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return "%s - %s"%(self.cell.name, self.name)

    class Meta:
        db_table = 'villages'
        verbose_name = 'Village'
        verbose_name_plural = 'Villages'
        ordering = ['name']
