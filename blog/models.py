from django.db import models as mod
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
# Create your models here.

#User Model
class User(AbstractUser):
  email=mod.EmailField(unique=True,blank=False,null=False)
  phone_number=mod.CharField(max_length=15,blank=True,null=True)
  city=mod.CharField(max_length=15, blank=True, null=True ) 
  state=mod.CharField(max_length=15, blank=True, null=True)
  image=mod.ImageField(upload_to='profiles/', blank=True, null=True)

  USERNAME_FIELD='email'
  REQUIRED_FIELDS=['username','first_name','last_name']
  def __str__(self):
    return self.email



#Category Model
class Category(mod.Model):
  name= mod.CharField(max_length=50)
  slug=AutoSlugField(populate_from='name' , unique=True)

  def __str__(self):
    return self.name

#Tag Model
class Tag(mod.Model):
  name=mod.CharField(max_length=50)
  slug=AutoSlugField(populate_from='name',unique=True)

  def __str__(self):
    return self.name
  
#Post Model
class Post(mod.Model):
  author= mod.ForeignKey(User, on_delete=mod.CASCADE)
  title= mod.CharField(max_length=200)
  text= mod.TextField()
  created_date= mod.DateTimeField(default=timezone.now)
  published_date= mod.DateTimeField(blank=True, null=True)
  slug=AutoSlugField(populate_from='title', unique=True)
  category=mod.ForeignKey(Category,null=True,blank=True,on_delete=mod.CASCADE)
  tag=mod.ManyToManyField(Tag,blank=True)
  thumbnail=mod.ImageField(upload_to='posts/thumbnails/', blank=True, null=True)
  featured=mod.ImageField(upload_to='posts/featured/', blank=True, null=True)
  

  def publish(self):
    self.published_date=timezone.now()
    self.save()

  def __str__(self):
    return self.title
  
class Comment(mod.Model):
  author=mod.ForeignKey(User,on_delete=mod.CASCADE)
  post=mod.ForeignKey(Post,on_delete=mod.CASCADE ,related_name='comments')
  text=mod.TextField()
  posted_date=mod.DateTimeField(default=timezone.now)
  reply=mod.ForeignKey('self',null=True,blank=True, on_delete=mod.CASCADE)

  def __str__(self):
    return f"{self.author.username} on {self.post.title}"
  @property
  def is_reply(self):
    return self.reply is None

