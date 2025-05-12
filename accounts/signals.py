from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MyUser


@receiver(post_save, sender=User)
def create_myuser(sender, instance, created, **kwargs):
    if created:
        # Tạo MyUser với avatar mặc định
        default_avatar = "https://img.freepik.com/premium-vector/user-profile-person-avatar-identity-login-icon-vector_1277826-995.jpg?w=360"
        # Tạo đối tượng MyUser với avatar mặc định
        MyUser.objects.create(
            user=instance, 
            link=default_avatar,
            bio=f"Xin chào! Tôi là {instance.username}."
        )


@receiver(post_save, sender=User)
def save_myuser(sender, instance, **kwargs):
    instance.myuser.save()
