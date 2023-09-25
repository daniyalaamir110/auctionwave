from django.contrib import admin
from .models import Product
from bids.models import Bid


class BidInline(admin.TabularInline):
    model = Bid
    fields = ("bidder", "bid_amount", "created_at", "updated_at")
    readonly_fields = ("bidder", "bid_amount", "created_at", "updated_at")
    can_delete = False
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "creator",
        "base_price",
        "is_available",
        "bid_count",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "base_price",
                    "creator",
                    "category",
                )
            },
        ),
        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    list_filter = ("category", "created_at", "creator", "base_price")
    search_fields = ("title", "description")
    readonly_fields = (
        "creator",
        "created_at",
        "updated_at",
    )
    inlines = (BidInline,)


admin.site.register(Product, ProductAdmin)
