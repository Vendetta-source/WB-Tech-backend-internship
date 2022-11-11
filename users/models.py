from django.contrib.auth.models import User
from django.db import models


class FollowUser(models.Model):
    """
    User Subscription Model.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    time_sub = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique follow')
        ]


