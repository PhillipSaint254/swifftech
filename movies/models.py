from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Movie(models.Model):
    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=2000)
    description = models.TextField(default="Text Here", null=True)
    logo = models.CharField(max_length=2000, default="logo")
    date_of_release = models.DateField(null=True)
    year = models.IntegerField()
    rating = models.FloatField()
    searches = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    seasons = models.IntegerField(default=0)
    trailer = models.CharField(default='url', max_length=500)
    movie = models.BooleanField(default=False)
    video = models.CharField(null=True, default=None, max_length=500)
    trending = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Season(models.Model):
    series = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="all_seasons")
    unique_field = models.CharField(max_length=100, unique=True)
    series_name = models.CharField(max_length=50, default=" ")
    season_no = models.IntegerField(default=0)

    def __str__(self):
        return self.series_name + " season " + str(self.season_no)


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="all_episodes")
    series_name = models.CharField(max_length=50, default=" ")
    unique_field = models.CharField(max_length=100, unique=True)
    season_no = models.IntegerField(default=0, unique=False)
    video = models.CharField(null=True, default=None, max_length=500)
    no_of_episodes = models.IntegerField(default=0)

    def __str__(self):
        return self.series_name + " season " + str(self.season_no) + " episodes"


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20)
    requested_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, default="username")
    subscription_choice = [
        ('not subscribed', 'not subscribed'),
        ('standard', 'standard'),
        ('pro', 'pro'),
        ('pro max', 'pro max')
    ]
    subscription = models.CharField(max_length=20, choices=subscription_choice, default='not subscribed')
    subscription_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
    phone = models.CharField(max_length=15, default="number")
    coins = models.FloatField(default=0)
    points = models.FloatField(default=0)
    epic = models.IntegerField(default=0)
    drama = models.IntegerField(default=0)
    horror = models.IntegerField(default=0)
    comedy = models.IntegerField(default=0)
    fantasy = models.IntegerField(default=0)
    sci_fy = models.IntegerField(default=0)
    fiction = models.IntegerField(default=0)
    historical_film = models.IntegerField(default=0)
    investigative = models.IntegerField(default=0)
    thriller = models.IntegerField(default=0)
    romance = models.IntegerField(default=0)
    mystery = models.IntegerField(default=0)
    action = models.IntegerField(default=0)
    sitcom = models.IntegerField(default=0)
    adventure = models.IntegerField(default=0)
    war = models.IntegerField(default=0)
    musical = models.IntegerField(default=0)
    documentary = models.IntegerField(default=0)
    western = models.IntegerField(default=0)
    crime = models.IntegerField(default=0)
    sports = models.IntegerField(default=0)
    disaster = models.IntegerField(default=0)
    biographical = models.IntegerField(default=0)
    animation = models.IntegerField(default=0)
    christian = models.IntegerField(default=0)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        created = Details()
        created.user = instance


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.details.save()


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=20, default="")
    amount = models.IntegerField(default=0)
    transaction_code = models.CharField(max_length=20, unique=True)
    code_stamp = models.CharField(max_length=25, default="some code")
    created_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    useful = models.BooleanField(default=False)
    username = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))

    def __str__(self):
        return self.username


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000, default="")
    created_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))
    to = models.CharField(max_length=50, default="all")
    unread = models.BooleanField(default=False)

    def __str__(self):
        return self.message[:20] + " " + str(self.created_at)


class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    transaction_type_choice = [
        ("credit", "credit"),
        ("debit", "debit")
    ]
    transaction_type = models.CharField(max_length=15, choices=transaction_type_choice, default="choose type")
    item_sold = models.CharField(max_length=100, default="item")
    price = models.IntegerField(default=0)
    transaction_code = models.CharField(max_length=100, primary_key=True)
    transaction_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=3))

    def __str__(self):
        return self.username + " - " + self.transaction_code


class TC(models.Model):
    code = models.CharField(max_length=25)

    def __str__(self):
        return self.code


class Hash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=1050)
    num = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.num)
