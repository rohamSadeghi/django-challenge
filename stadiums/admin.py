from django.contrib import admin

from stadiums.models import Stadium, Seat, Match


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "is_enable", "created_time"]
    search_fields = ('name', 'phone_number', )
    list_filter = ['is_enable', ]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ["stadium", "price", "price_discount", "is_enable", "is_available", "created_time"]
    search_fields = ('stadium__name', )
    list_filter = ['is_enable', 'is_available', 'stadium']
    autocomplete_fields = ('stadium', )
    list_select_related = ['stadium', ]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ["stadium", "title", "execute_time", "is_enable", "created_time"]
    search_fields = ('title', )
    list_filter = ['is_enable', 'stadium']
    autocomplete_fields = ('stadium', )
    list_select_related = ['stadium', ]