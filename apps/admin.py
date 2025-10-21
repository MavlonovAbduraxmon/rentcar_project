from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.models import Group
from apps.models import CarImage, User, Car, Brand, Category, Feature, FAQ
from apps.models.cars import CarColor, LongTermRental
from apps.models.news import New


class CarImageStackedInline(StackedInline):
    model = CarImage
    extra = 1
    max_num = 8
    min_num = 1

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = 'id', 'phone',

@admin.register(Car)
class CarAdminModel(ModelAdmin):
    list_display = 'category', 'brand','limit_day','deposit','fuel_type',

@admin.register(Brand)
class CarBrandAdminModel(ModelAdmin):
    list_display = 'name', 'logo',

@admin.register(CarColor)
class CarColorAdminModel(ModelAdmin):
    list_display = 'name',

@admin.register(Category)
class CarTypeAdminModel(ModelAdmin):
    list_display = 'name', 'image',

@admin.register(Feature)
class FeatureModelAdmin(ModelAdmin):
    list_display = 'id','name','icon', 'description'


@admin.register(CarImage)
class CarImageModelAdmin(ModelAdmin):
    list_display = ('id', 'car', 'image')


@admin.register(FAQ)
class FAQModelAdmin(ModelAdmin):
    list_display = 'question', 'answer'


@admin.register(New)
class NewModelAdmin(ModelAdmin):
    list_display = 'id','title'


@admin.register(LongTermRental)
class LongtermRentalAdmin(ModelAdmin):
    list_display = 'id','car', 'user', 'start_data', 'end_data', 'total_price', 'is_paid'


admin.site.unregister(Group)




# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Group
# from django.utils.translation import gettext_lazy as _
#
# from apps.models import Car, Category, User
#


# class UserProxy(User):
#     class Meta:
#         proxy = True
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#
#
# class AdminProxy(User):
#     class Meta:
#         proxy = True
#         verbose_name = 'Admin'
#         verbose_name_plural = 'Admins'
#
#
# @admin.register(User)
# class UserAdminMixin(UserAdmin):
#     class Meta:
#         model = User
#         fields = "__all__"
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['phone'].initial = '+998'
#
#
#
#
# @admin.register(UserProxy)
# class UserProxyModelAdmin(UserAdminMixin):
#     type = False
#     list_display = ['id', 'first_name', 'last_name', 'user_address', 'user_university']
#
#     @admin.display(description="Address", empty_value='')
#     def user_address(self, obj):
#         if hasattr(obj, 'userprofile'):
#             return obj.userprofile.address
#
#     @admin.display(description="University", empty_value='')
#     def user_university(self, obj):
#         if hasattr(obj, 'userprofile'):
#             return obj.userprofile.university
#
#
# @admin.register(AdminProxy)
# class AdminProxyModelAdmin(UserAdminMixin):
#     type = True
#     list_display = ['id', 'phone', 'admin_balance']
#
#     @admin.display(description="Balance")
#     def admin_balance(self, obj):
#         if hasattr(obj, 'adminprofile'):
#             return obj.adminprofile.balance
#         return 0
#
#
# @admin.register(Category)
# class CategoryModelAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product_names')
#
#     @admin.display(description="Product names")
#     def product_names(self, obj):
#         return ", ".join([car.name for car in obj.cars.all()])
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('cars')
#
#
# @admin.register(Car)
# class CarModelAdmin(admin.ModelAdmin):
#     list_display = 'brand', 'limit_day', 'category', 'transmission_type', 'fuel_type'
#
#     # search_fields = 'name'
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('category')
#
#




# search_fields = ['phone']
#     ordering = ("phone",)
#     fieldsets = (
#         (None, {"fields": ("phone", "password")}),
#         (_("Personal info"), {"fields": ("first_name", "last_name")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("phone", "usable_password", "password1", "password2"),
#             },
#         ),
#     )
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(is_superuser=self.type)
