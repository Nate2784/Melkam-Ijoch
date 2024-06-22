from django.db import models
from django.contrib.auth.models import User
import uuid

class CompanyInformation(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='Images/')
    slogan = models.CharField(max_length= 100)
    description = models.TextField(max_length=2000)
    services = models.TextField(max_length=7000)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return self.user.username

class Charity(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='Images/')
    description = models.TextField(max_length = 2000)
    website = models.URLField(max_length=200)
    location = models.CharField(max_length=100)
    establishedYear = models.IntegerField()

    def __str__(self):
        return self.name
    
class Project(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    charity_ID = models.ForeignKey(Charity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length = 2000)
    image = models.ImageField(upload_to='Images/')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Donation(models.Model):
    PAYMENT_CHOICES = [
        ('Chapa', 'Chapa'),
        ('Telebirr', 'Telebirr'),
        ('CBE', 'CBE'),
        ('Other', 'Other'),
    ]

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    project_ID = models.ForeignKey(Project, on_delete=models.CASCADE)
    charity_ID = models.ForeignKey(Charity, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donationDate = models.DateTimeField(auto_now_add=True)
    paymentMethod = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    paymentTransactionID = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'Donation {self.id} by {self.user_ID.username}'

class AddCharity(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Images/')
    description = models.TextField(max_length=2000)
    website = models.URLField(max_length=200)
    location = models.CharField(max_length=100)
    establishedYear = models.IntegerField()
    authorisedDocuments = models.FileField(upload_to='AuthorisedDocuments/', blank=True) 
    statement = models.TextField(max_length=2000)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    