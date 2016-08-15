import json
from django.db                  import models
from django.conf                import settings
#from steam                      import settings
from django.templatetags.static import static
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )
from content.models             import ( MyUserManager, MyUser )
import csv

with open('python.csv', 'rb') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=',')
  for row in reader:
    print row['email'];
    user = MyUser(email=row['email'], password=row['password']);
    #user = MyUser.objects.get(email=row['email']);
    user.set_password(row['password']);
    user.is_active=True;
    user.init_profile();
