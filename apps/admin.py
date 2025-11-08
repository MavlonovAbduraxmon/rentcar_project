from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import CarImage, User, Car, Brand, Category, Feature, FAQ
from apps.models.cars import CarColor, LongTermRental, CarTariff
from apps.models.news import New
from apps.models.users import AdminProfile, UserProfile


class CarImageStackedInline(StackedInline):
    model = CarImage
    extra = 1
    max_num = 8
    min_num = 1


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = 'id', 'phone', 'type'
    ordering = ("phone",)
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "usable_password", "password1", "password2"),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    ist_display = ['id', 'phone', 'get_first_name']

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = "First Name"


@admin.register(Car)
class CarAdminModel(ModelAdmin):
    list_display = 'name', 'brand', 'category', 'daily_price', 'deposit', 'transmission_type', 'fuel_type', 'is_available'
    list_filter = 'name', 'brand', 'category'
    readonly_fields = ['car_image']
    list_select_related = 'brand','category','color'
    inlines = [CarImageStackedInline,]


    def daily_price(self, obj):
        price = CarTariff.objects.filter(car=obj.id).first()
        return price.daily_price if price else "_"

    def car_image(self, obj):
        photos = CarImage.objects.filter(car_id=obj.id)
        if photos.exists():
            imgs = "".join(
                [f'<img src="{photo.image.url}" width="50" height="50" style="margin:2px;" />' for photo in photos])
        else:
            imgs = f'<img src="/media/car/noimage.png" width="50" height="50" style="margin:2px;" />'
        return mark_safe(imgs)


@admin.register(Brand)
class BrandAdminModel(ModelAdmin):
    list_display = 'name', 'logo',


@admin.register(CarColor)
class CarColorAdminModel(ModelAdmin):
    list_display = 'name',


@admin.register(Category)
class CategoryAdminModel(ModelAdmin):
    list_display = 'name', 'image',


@admin.register(Feature)
class FeatureModelAdmin(ModelAdmin):
    list_display = 'id', 'name', 'icon', 'description'


@admin.register(CarImage)
class CarImageModelAdmin(ModelAdmin):
    list_display = 'id', 'car', 'image'


@admin.register(FAQ)
class FAQModelAdmin(ModelAdmin):
    list_display = 'question', 'answer'


@admin.register(New)
class NewModelAdmin(ModelAdmin):
    list_display = 'id', 'title'


@admin.register(CarTariff)
class CarTariff(ModelAdmin):
    list_display = 'id', 'car', 'daily_price', 'one_to_three_day', 'three_to_seven_day', 'seven_to_half_month', 'half_to_one_month'


@admin.register(LongTermRental)
class LongTermRentalAdmin(ModelAdmin):
    list_display = 'id', 'car', 'user', 'pick_up_location', 'pick_up_data_time', 'drop_of_location', 'drop_of_data_time', 'payment_method'


class ManagerProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class AdminProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class UserAdminMixin(UserModelAdmin):
    search_fields = ['phone']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=self.type)


class UserProfileStackedInline(admin.StackedInline):
    model = UserProfile
    min_num = 1
    extra = 1
    max_num = 1


@admin.register(ManagerProxy)
class UserProxyModelAdmin(UserAdminMixin):
    type = False
    list_display = ['id', 'first_name', 'last_name', 'user_address', 'user_university']
    inlines = [UserProfileStackedInline]

    @admin.display(description="Address", empty_value='')
    def user_address(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.address

    @admin.display(description="University", empty_value='')
    def user_university(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.university


class AdminProfileStackedInline(admin.StackedInline):
    model = AdminProfile
    min_num = 1
    extra = 1
    max_num = 1
    readonly_fields = ['balance']


@admin.register(AdminProxy)
class AdminProxyModelAdmin(UserAdminMixin):
    type = True
    inlines = [AdminProfileStackedInline]
    list_display = ['id', 'phone', 'admin_balance']

    @admin.display(description="Balance")
    def admin_balance(self, obj):
        if hasattr(obj, 'adminprofile'):
            return obj.adminprofile.balance
        return 0




def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request)

    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
    all_models = []
    for app in app_list:
        all_models.extend(app.pop('models', []))
        app['models'] = []

    new_apps = {
        'label1': {
            'name': "Users",
            "app_label": 'label1',
            'models': list()
        },

        'label2': {
            'name': "Cars",
            "app_label": 'label2',
            'models': list()
        },

        'label3': {
            'name': "Rentals",
            "app_label": 'label3',
            'models': list()
        },
    }

    model_order = {
        'User': 'label1',
        'UserProfile': 'label1',

        'Car': 'label2',
        'CarBrand': 'label2',
        'CarColor': 'label2',
        'CarCategory': 'label2',
        'Feature': 'label2',
        'CarImage': 'label2',
        'CarPrice': 'label2',
        'CarFeature': 'label2',

        'Course': 'Rental',

    }

    for _model in all_models:
        if _model['object_name'] in model_order.keys():
            new_apps[model_order[_model['object_name']]]['models'].append(_model)
        else:
            app_list[0]['models'].append(_model)

    app_list.extend(new_apps.values())
    return app_list

admin.site.unregister(Group)