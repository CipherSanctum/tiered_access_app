from django.db import models
from accounts_app.models import CustomUser


class TieredAppCustomUser(models.Model):
    TIER_CHOICES = (
            ('none', 'No access'),
            ('tier1', 'Tier 1'),  # ('database_value', 'display value')... smartest to have this rendered as a form too
            ('tier2', 'Tier 2'),
            ('tier3', 'Tier 3'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tier_choice = models.CharField(max_length=10, choices=TIER_CHOICES, default='tier1')

    def __str__(self):
        return self.user.username
