from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random

# Create your models here.

def numeric_validation(value):
    if not value.isnumeric():
        raise ValidationError("Field should be numeric")
    
    return value
class BaseManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('Email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    objects = BaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    choices = (('user','user'),('cashier','cashier'),('manager','manager'))
    usertype = models.CharField(max_length = 10, default = "user")

    def __str__(self):
        return self.email

class Branch(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)

    # Account information
    account_number = models.CharField(max_length = 10,unique = True,validators=[numeric_validation])
    balance = models.BigIntegerField()
    branch  = models.ForeignKey(Branch,null = True,blank=True,on_delete=models.SET_NULL)
    account_type = models.CharField(max_length = 10, choices = (('current','current'),('savings','savings')),default = "savings")
    
    # Personal Information
    first_name = models.CharField(max_length = 256)
    middle_name = models.CharField(max_length = 256, blank = True)
    last_name = models.CharField(max_length = 256)
    dob = models.DateField(blank=True,null = True)
    gender = models.CharField(max_length= 2, choices=(('m',"male"),('f',"female")), blank=True)
    city = models.CharField(max_length= 20, blank=True)
    religion = models.CharField(max_length= 20, blank=True)
    marital_status = models.CharField(max_length= 2, choices=(('s',"Single"),('m',"Married")), blank=True)
    address = models.CharField(max_length= 40, blank=True)
    contact = models.CharField(max_length=12,blank=True, validators=[numeric_validation])

    # Means of Identity
    means_of_id = models.CharField(max_length = 10, choices = (('nid','national id card'),('dl','driver licence'),('vc','Voters Card'),
    ('ip','International Passport')), blank=True)
    id_number = models.CharField(max_length= 20, blank=True)
    id_expiry_date = models.DateField(blank=True,auto_now_add=False)

    # Next of Kin
    next_of_kin_title = models.CharField(max_length= 256, blank=True)
    next_of_kin_name = models.CharField(max_length= 256, blank=True)
    next_of_kin_email = models.EmailField(blank=True)
    next_of_kin_dob = models.DateField(blank=True, auto_now_add=False)
    next_of_kin_contact = models.CharField(max_length= 12, blank=True)
    
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.email


    def save(self,*args,**kwargs):
        while not self.account_number:
            account_number = str(random.randint(1000000000,2000000000))
            similar_number =Account.objects.filter(account_number = account_number).exists()
            if not similar_number:
                self.account_number = account_number
                break
        return super().save(*args,**kwargs)
    
class Transfer(models.Model):
    sent_from = models.ForeignKey(Account,related_name = "transfers",on_delete=models.CASCADE)
    sent_to = models.ForeignKey(Account,related_name = "receives",on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank = True)
    amount = models.BigIntegerField()
    date_created =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transfer made by {self.sent_from} to {self.sent_to}; Amount- {self.amount}'

    

class Deposit(models.Model):
    amount = models.PositiveBigIntegerField()
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank = True)
    status = models.CharField(max_length=10, choices=(("pending","pending"),("success","success")),default="pending")
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Deposit made to {self.account.user.email}; Amount - {self.amount}"
    class Meta:
        ordering= ("status","date_created")
    def get_type(self):
        return "deposit"

class Withdraw(models.Model):
    amount = models.BigIntegerField()
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    description = models.CharField(max_length=200,blank=True)
    status = models.CharField(max_length=10, choices=(("pending","pending"),("success","success")),default="pending")
    date_created = models.DateTimeField(default=timezone.now)

    def get_type(self):
        return "withdraw"
    class Meta:
        ordering= ("status","date_created")
    def __str__(self):
        return f"Withdrawal made from {self.account.user.email}; Amount - {self.amount}"

class Notification(models.Model):
    user = models.ForeignKey(User,related_name="notification", on_delete=models.CASCADE)
    fromm = models.ForeignKey(User,related_name="sends", on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    date_sent = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, null  = True, blank=True, on_delete=models.SET_NULL)
    message = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    
class BlockedTransfer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.account.user.email +"--"+self.message

class OtherAccount(models.Model):
    # Account information
    account_number = models.CharField(max_length = 10,unique = True,validators=[numeric_validation])
    balance = models.BigIntegerField()
    bank = models.CharField(max_length=100)
    account_type = models.CharField(max_length = 10, choices = (('current','current'),('savings','savings')),default = "savings")
    
    # Personal Information
    first_name = models.CharField(max_length = 256)
    middle_name = models.CharField(max_length = 256, blank = True)
    last_name = models.CharField(max_length = 256)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name +" Accounts"