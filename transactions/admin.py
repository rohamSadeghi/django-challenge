from django.contrib import admin

from transactions.models import PurchaseMatch


@admin.register(PurchaseMatch)
class PurchasePackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'seat', 'is_paid', 'created_time')
    autocomplete_fields = ['user', 'match', 'seat']
    list_select_related = ['user', 'match', 'seat']
    list_filter = ['is_paid', ]
    list_per_page = 30
    search_fields = ['user__phone_number', ]
    readonly_fields = ['is_paid', ]

    def save_model(self, request, obj, form, change):
        obj.is_paid = True
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
