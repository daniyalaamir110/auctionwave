from django.contrib import admin
from .models import Category
from products.models import Product


class ProductInline(admin.TabularInline):
    model = Product
    fields = ("title", "description", "creator")
    readonly_fields = ("title", "description", "creator")
    can_delete = False
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fieldsets = (
        (
            None,
            {"fields": ("title",)},
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
    list_filter = ("created_at",)
    search_fields = ("title",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    inlines = (ProductInline,)


admin.site.register(Category, CategoryAdmin)
