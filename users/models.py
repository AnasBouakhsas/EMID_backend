from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.timezone import now


# Custom user manager for users_customers
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


# CustomUser model for users_customers
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id_client = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users_customuser'

    def __str__(self):
        return self.username

class UserGroupe(models.Model):
    Code_groupe = models.CharField(max_length=50)
    Groupe_description = models.CharField(max_length=50)

    class Meta:
        db_table = 'UserGroupe'
    


# Model for internal user management in the 'users' table
class InternalUser(models.Model):
    UserCode = models.CharField(max_length=50, primary_key=True)
    Route_ID = models.ForeignKey('Routes', on_delete=models.SET_NULL, null=True, blank=True)
    UserName = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    UserType = models.CharField(max_length=15, null=True, blank=True)
    Grouping = models.CharField(max_length=50, null=True, blank=True)
    IsBlocked = models.BooleanField(default=False)
    LoginName = models.CharField(max_length=100)
    AreaCode = models.CharField(max_length=10, null=True, blank=True)
    CityID = models.IntegerField(null=True, blank=True)
    RouteCode = models.CharField(max_length=10, null=True, blank=True)
    ParentCode = models.CharField(max_length=50, null=True, blank=True)
    ParentDescription = models.CharField(max_length=50, null=True, blank=True)
    promotions = models.ManyToManyField('PromoHeaders', blank=True, related_name='users')



    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.UserCode

class Regions(models.Model):
    Region_Code = models.CharField(max_length=50, primary_key=True)
    Org_ID = models.CharField(max_length=50)
    Region_Description = models.CharField(max_length=100)
    Region_Alt_Description = models.CharField(max_length=100)
    Stamp_Date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Region_Description
    class Meta:
        db_table = 'Regions'

class Parameters(models.Model):
    ParameterName = models.CharField(max_length=100)
    DefaultValue = models.CharField(max_length=100)
    ParameterType = models.CharField(max_length=50)

    class Meta:
        db_table = 'User_Parameters'

    def __str__(self):
        return self.ParameterName
    
class Routes(models.Model):
    Route_ID = models.AutoField(primary_key=True)
    Branch_Code = models.CharField(max_length=50, blank=True, default='')
    Route_Description = models.CharField(max_length=100, blank=True, default='')
    Route_Alt_Description = models.CharField(max_length=100, blank=True, default='')
    Region_Code = models.CharField(max_length=50, blank=True, default='')
    RVSCode = models.CharField(max_length=50, blank=True, default='')
    RVSDescription = models.CharField(max_length=50, blank=True, default='')
    Stamp_Date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Routes'

    def __str__(self):
        return str(self.Route_ID)
    


class Client_Statut(models.Model):
    Client_Statut_ID = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    Statut_Description = models.CharField(max_length=50)

    class Meta:
        db_table = 'Client_Statut'
    
    def __str__(self):
        return self.Statut_Description
    
class Clients(models.Model):
    Client_Code = models.CharField(primary_key=True, max_length=20)
    Route_ID = models.ForeignKey('Routes', on_delete=models.SET_NULL, null=True, blank=True)
    Salesman = models.CharField(max_length=100, blank=True, default='N/A')
    Area_Code = models.CharField(max_length=50, blank=True, default='')
    Client_Description = models.CharField(max_length=50, blank=True, default='')
    Client_Alt_Description = models.CharField(max_length=50, blank=True, default='')
    Payment_Term_Code = models.CharField(max_length=50, blank=True, default='')
    Email = models.EmailField(unique=True)
    Has_Route = models.BooleanField(default=False)
    Address = models.CharField(max_length=50, blank=True, default='')
    Alt_Address = models.CharField(max_length=50, blank=True, default='')
    Contact_Person = models.CharField(max_length=50, blank=True, default='')   
    Phone_Number = models.CharField(max_length=50, blank=True, default='')
    Barcode = models.CharField(max_length=50, blank=True, default='')
    Client_Status_ID = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(2)])
    Channel_description = models.ForeignKey('Channels', on_delete=models.SET_NULL, null=True, blank=True)
    promotions = models.ManyToManyField('PromoHeaders', blank=True, null=True, related_name='clients')

    class Meta:
        
        db_table = 'Clients'
    def __str__(self):
        return self.Client_Code


class PromoHeaders(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    promotion_description = models.CharField(max_length=255)
    promotion_type = models.CharField(max_length=50, choices=[('Trade Sales', 'Trade Sales'), ('Consumer Sales', 'Consumer Sales')])
    start_date = models.DateField()
    end_date = models.DateField()
    is_forced = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField()
    promotion_apply = models.CharField(max_length=50, choices=[('ISELL', 'ISELL'), ('E-Ordering', 'E-Ordering'), ('Retail', 'Retail')])



    def __str__(self):
            return f'{self.promotion_description} ({self.promotion_id})'

    class Meta:
            db_table = 'Promo_Headers'

class PromoDetails(models.Model):
    promotion_id = models.ForeignKey('PromoHeaders', on_delete=models.CASCADE, related_name='promo', null=True, blank=True)
    basket = models.ForeignKey('PromoItemBasketHeaders', on_delete=models.CASCADE, related_name='promo_details', null=True, blank=True)
    quantity_buy = models.IntegerField()
    types_buy = models.CharField(max_length=50, choices=[('Amount', 'Amount'), ('Caisse', 'Caisse'), ('Cartouche', 'Cartouche'), ('Paquet', 'Paquet')])
    quantity_get = models.IntegerField()
    types_get = models.CharField(max_length=50, choices=[('Pourcentage', 'Pourcentage'), ('Cutoff Price', 'Cutoff Price')])

    class Meta:
            db_table = 'Promo_Details'


class PromoAssignments(models.Model):
    org_id = models.IntegerField()
    assignment_code = models.CharField(max_length=50, primary_key=True)
    assignment_type = models.CharField(max_length=50)
    second_assignment_type = models.CharField(max_length=50)
    second_assignment_code = models.CharField(max_length=50)
    stamp_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.assignment_code

class PromoItemBasketHeaders(models.Model):
    item_basket_id = models.AutoField(primary_key=True)
    item_basket_description = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now)
    last_updated_date = models.DateTimeField(default=timezone.now)
    products = models.ManyToManyField('Produit', related_name='baskets', blank=True)


    class Meta:
        db_table = 'Promo_Item_Basket_Headers'

    def __str__(self):
        return self.item_basket_description

class Area(models.Model):
    area = models.CharField(max_length=250)
    Area_description = models.CharField(max_length=255)



class Client_Discounts(models.Model):
    Client_Code = models.CharField(max_length=20)
    Trx_Code = models.CharField(max_length=50, default='',null=True )
    Discounts = models.IntegerField()
    Month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    Years = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2030)])
    Discounts_label = models.CharField(max_length=50)
    Applied = models.IntegerField(default=0, null=True)
    Stamp_Date = models.DateTimeField(default=now)
    Affected_item_code = models.CharField(max_length=50, default='')

class Client_Target(models.Model):
    Client_Code = models.CharField(max_length=20)
    Month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    years = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2030)])
    Target_value = models.DecimalField(max_digits=18,decimal_places=2)
    Targed_Achieved = models.DecimalField(max_digits=18,decimal_places=2)
    Stamp_Date = models.DateTimeField(default=now)

class Channels(models.Model):
    channel_code = models.CharField(max_length=50)
    Channel_description = models.CharField(max_length=255)
    delivery_system = models.IntegerField(default=0)
    related_price_list_code = models.CharField(max_length=50, null=True)
    return_price_list_code = models.CharField(max_length=50, null=True)

class Device(models.Model):
    device_serial = models.CharField(max_length=100, unique=True)
    device_name = models.CharField(max_length=100)
    UserCode = models.ForeignKey('InternalUser', on_delete=models.SET_NULL, null=True, blank=True)
    device_status = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default = 'HHT')
    Route_ID = models.ForeignKey('Routes', on_delete=models.SET_NULL, null=True, blank=True)



    def __str__(self):
        return self.device_name


class Produit(models.Model):
    CodeProduit = models.CharField(max_length=100, unique=True)
    ProduitDescription = models.CharField(max_length=100)
    AltProduitDescription = models.CharField(max_length=100, blank=True, null=True)
    typeProduit = models.CharField(max_length=100, default = 'Item')

    def __str__(self):
        return self.ProduitDescription