from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, default=None, null=True)
    last_name = models.CharField(max_length=255, default=None, null=True)

    email = models.EmailField(max_length=100, unique=True)

    username = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    session_token = models.CharField(max_length=10, default=0)

    active = models.BooleanField(default=False)
    # a admin user; non super-user
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # a superuser

    phone = models.CharField(max_length=255, default=None, null=True)
    address = models.TextField(default=None, null=True)
    city = models.CharField(max_length=255, default=None, null=True)
    state = models.CharField(max_length=255, default=None, null=True)
    zip_code = models.CharField(max_length=255, default=None, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    UNIT_TYPES_CHOICES = (
        ('count', 0),
        ('weight', 1),
        ('volume', 2),
    )

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    unit_type = models.CharField(
        max_length=10,
        choices=UNIT_TYPES_CHOICES,
        default='count',
    )
    per_unit_price = models.FloatField('unit price')
    available_quantity = models.IntegerField()
    publish_date = models.DateField()
    product_image = models.ImageField(upload_to='shop/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField('date time created at', auto_now_add=True)
    updated_at = models.DateTimeField('date time updated at', auto_now=True)

    class Meta:
        ordering = ['product_id']

    def __str__(self):
        return f"{self.product_id} - {self.product_name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'ACTIVE'),
        ('shipped', 'SHIPPED'),
        ('delivered', 'DELIVERED'),
    )

    order_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255, default="")
    date = models.DateTimeField('order date', auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='active')
    # ordered_item = models.TextField()
    ordered_item = models.ManyToManyField(Product, help_text='Added products')

    # ordered_item = forms.ModelMultipleChoiceField(
    #     widget=widgets.FilteredSelectMultiple('Product name', False),
    #     queryset=Product.objects.all()
    # )

    def __str__(self):
        return f"{self.order_id} - {self.first_name}"

    def display_ordered_item(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(ordered_item.product_name for ordered_item in self.ordered_item.all()[:3])

    display_ordered_item.short_description = 'Ordered Items'


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="")
    update_desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"


class ContactUs(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.contact_id} - {self.name}"

    class Meta:
        verbose_name_plural = "Contact us"
