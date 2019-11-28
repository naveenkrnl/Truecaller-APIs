from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
# Create your models here.

PHONENO_REGEX='^[0-9]{10}$'

class PersonalContacts(models.Model):
    user                        =   models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name                        =   models.CharField(max_length=200)
    phone_number                =   models.CharField(max_length=200,validators=[RegexValidator(
                                            regex=PHONENO_REGEX,
                                            message="Phone Number must be of 10 digits",
                                            code='invalid_username'
                                            )])
    email_address               =   models.EmailField(null=True, blank=True)
    spam_count                  =   models.IntegerField(default=0)
    def __str__(self):
        return self.name