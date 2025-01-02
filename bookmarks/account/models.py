from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    """ User profile """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        """ String representation of a user """
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    """ Defines the following/follower relationship """
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ Defines the class Metadata """
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']

    def __str__(self):
        """ String representation of the class """
        return f'{self.user_from} follows {self.user_to}'


# Add the 'following' field to User model dynamically
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self',
                        through=Contact, related_name='followers',
                        symmetrical=False))
