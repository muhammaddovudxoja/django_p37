from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, EmailField, URLField, BooleanField, BigIntegerField, DateField, FileField
from django.db.models import Model, CharField, ForeignKey, CASCADE, DecimalField, ImageField, Q, ManyToManyField, \
    JSONField
from django.db.models.constraints import CheckConstraint
from django.db.models.fields import PositiveIntegerField, DateTimeField, PositiveSmallIntegerField, \
    TextField
from django.utils.timezone import now


class Course(Model):
    name = CharField("Course name", max_length=100)
    price = BigIntegerField("Course price")

    def __str__(self):
        return self.name


class Student(Model):
    first_name = CharField("Student first name", max_length=100)
    last_name = CharField("Student last name", max_length=100)
    birth_date = DateField("Student birth date")
    phone = CharField("Student phone number", max_length=12, unique=True)
    passport_number = CharField("Student passport number", max_length=7)
    passport_series = CharField("Passport series", max_length=5)
    courses = ManyToManyField("apps.Course", blank=True)
    image = ImageField(upload_to="student/%Y/%m/d")
    class Meta:
        unique_together = [["passport_series", "passport_number"]]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Document(Model):
    document = FileField(upload_to="student/%Y/%m/d")
    student = ForeignKey("apps.Student", CASCADE)







class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(null=False, blank=False, max_length=100)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    description = TextField()
    specification = JSONField(default=dict)
    price = DecimalField(max_digits=10, decimal_places=2)
    discount = PositiveSmallIntegerField(default=0, help_text='Chegirma (% foizda)')
    tags = ManyToManyField('apps.Tag', blank=True, related_name='product_tags')
    shipping_cost = PositiveIntegerField(default=0)
    like_count = PositiveIntegerField(default=0)

    quantity = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now=True)

    @property
    def current_price(self):
        return self.price - self.price * self.discount / 100

    @property
    def is_new(self):
        return now().date() - self.created_at.date() < timedelta(days=3)

    @property
    def is_in_stock(self):
        return self.quantity > 0

    class Meta:
        constraints = [
            CheckConstraint(condition=Q(discount__lte=100), name='check_product_price',
                            violation_error_message="Chegirma foizda (0-100 oraliqda bolishi kerak)")
        ]

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')

    def __str__(self):
        return self.product.name


class Review(Model):
    title = CharField(max_length=255)
    comment = TextField()
    product = ForeignKey('apps.Product', CASCADE, related_name='reviews')
    author = ForeignKey('auth.User', CASCADE, related_name='reviews')
    created_at = DateTimeField(auto_now=True)


class Cart(Model):
    user = ForeignKey('auth.User', CASCADE, related_name='carts')
    product = ForeignKey('apps.Product', CASCADE, related_name='carts')
    quantity = PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('user', 'product'),)


class Post(Model):
    user = ForeignKey('auth.User', CASCADE, related_name='posts')
    title = CharField(max_length=255)
    body = TextField()
    created_at = DateTimeField(auto_now=True)


class Comment(Model):
    post = ForeignKey('apps.Post', CASCADE, related_name='comments')
    name = CharField(max_length=255)
    email = EmailField()
    body = TextField()
    created_at = DateTimeField(auto_now=True)


class Album(Model):
    user = ForeignKey('auth.User', CASCADE, related_name='albums')
    title = CharField(max_length=255)


class Photo(Model):
    album = ForeignKey('apps.Album', CASCADE, related_name='photos')
    title = CharField(max_length=255)
    url = URLField()
    thumbnail = ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return self.album.title


class Todo(Model):
    user = ForeignKey('auth.User', CASCADE, related_name='todos')
    title = CharField(max_length=255)
    completed = BooleanField(default=False)


class Company(Model):
    name = CharField(max_length=255)
    catchPhrase = CharField(max_length=255)
    bs = CharField(max_length=255)


class User(Model):
    name = CharField(max_length=255)
    username = CharField(max_length=255)
    email = EmailField()
    phone = CharField(max_length=255)
    website = CharField(max_length=255)
    company = ForeignKey('apps.Company', CASCADE, related_name='users')

class Address(Model):
    user = ForeignKey('auth.User', CASCADE, related_name='addresses')
    street = CharField(max_length=255)
    city = CharField(max_length=255)
    suite = CharField(max_length=255)
    zipcode = CharField(max_length=255)
    geo = JSONField(default=dict, help_text='Geographic coordinates (latitude, longitude)')















