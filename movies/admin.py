from django.contrib import admin
from .models import *


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ("name", "pk", "description", "genre", "rating", "searches")


@admin.register(Transaction)
class TransactionsAdmin(admin.ModelAdmin):
    search_fields = ("transaction_code", "created_at")


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    search_fields = ("phone", "coins")


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    search_fields = ("series_name", "season_no", "unique_field")


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    search_fields = ("series_name", "season_no", "unique_field", "no_of_episodes")


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    search_fields = ("to", "message", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("username", "comment", "date", "useful")


@admin.register(TC)
class TCAdmin(admin.ModelAdmin):
    search_fields = ("code",)


@admin.register(Sale)
class SalesAdmin(admin.ModelAdmin):
    search_fields = ("transaction_type", "transaction_code", "transaction_time", "price", "item_sold", "username")
