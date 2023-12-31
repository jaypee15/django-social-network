from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class Profile(models.Model):

    JOB_TYPE_CHOICES = [
        ("Full Time", "full time"),
        ("Contract", "contract"),
        ("Freelance", "freelance"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True) 
    location = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(default='profile_avatars/avatar.jpg', upload_to='profile_avatars')
    cover_image = models.ImageField(default='cover_images/wallpaperflare.com_wallpaper_1.jpg', upload_to='cover_images')
    title =models.CharField(default='', max_length=255)
    job_description = models.CharField(max_length=255, default='')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full Time')
    rate = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default='20')
    nationality = CountryField( null=True, blank=True) 
    # facebook = models.CharField(max_length=140, null=True, blank=True, default='https://facebook.com')
    # twitter = models.CharField(max_length=140, null=True, blank=True, default='https://twitter.com')

    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self) -> str:
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.size or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

        cover_img = Image.open(self.cover_image.path)
        if cover_img.size or cover_img.width > 500:
            output_size = (1200, 500)
            cover_img.thumbnail(output_size)
            cover_img.save(self.cover_image.path)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

        



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='posts')
    body = models.CharField(max_length=140)
    post_image = models.ImageField(upload_to='post_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"{self.user}"
            f"({self.created_at:%Y-%m-%d %H:%M}):"
            f"{self.body[:30]}..."
        )