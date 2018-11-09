from django.db import models
from accounts_app.models import User


class TieredAppUser(models.Model):
    TIER_CHOICES = (
            ('none', 'No access'),
            ('tier1', 'Tier 1'),
            ('tier2', 'Tier 2'),
            ('tier3', 'Tier 3'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tier_choice = models.CharField(max_length=10, choices=TIER_CHOICES, default='none')

    def __str__(self):
        return self.user.username
