# from apps.models import Course, Student, Document


# Register your models here.


# class StudentInline(admin.TabularInline):
#     model = Student
#     extra = 1
#
#
# @admin.register(University)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ["name", "established_date", "address"]
#     search_fields = ["name", "address"]
#     list_filter = ["established_date", "address"]
#     ordering = ["established_date"]
#     inlines = [StudentInline]
#     readonly_fields = ["established_date"]
#     list_display_links = ["name", "address"]

# def student_count(self, obj):
#     return obj.student_count
# student_count.admin_order_field = "student_count"
# student_count.short_description = "Students"


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ["first_name", "last_name", "phone", "birth_date", "university", ]
#     search_fields = ["first_name", "last_name", "phone"]
#     list_filter = ["university", "birth_date"]
#     ordering = ["first_name", "university"]
#     list_display_links = ["first_name", "last_name", "phone"]


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ["name", "price", "student_count"]
#     search_fields = ["name", "price"]
#     list_filter = ["name", "price"]
#     ordering = ["name"]
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(
#             _student_count=Count("student", distinct=True),
#         )
#         return queryset
#
#     def student_count(self, obj):
#         return obj._student_count
#
#     student_count.admin_order_field = '_student_count'
#
#
# class DocumentStackedInline(admin.StackedInline):
#     model = Document
#     extra = 1
#     min_num = 1
#
#
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ["phone", "day_to_birthday", "passport", "course_count", "student_image"]
#     search_fields = ["phone", "first_name", "last_name"]
#     list_filter = ["courses", "birth_date"]
#     ordering = ["first_name"]
#     inlines = [DocumentStackedInline]
#
#     @admin.display(description="Rasmlar")
#     def student_image(self, obj: Student):
#         student_image = obj.image
#         if student_image and student_image.url:
#             return mark_safe(
#                 f'<img src="{student_image.url}" width="60" height="40" style="object-fit:cover;border-radius:4px;" />'
#             )
#         return "-"
#
#     @admin.display(description="Ismi")
#     def custom_name(self, obj: Student):
#         return obj.first_name
#
#     @admin.display(description="Rasmlar soni")
#     def images_count(self, obj: Student):
#         return obj.studentimage_set.count()
#
#     @admin.display(description='Passport')
#     def passport(self, obj):
#         return f"{obj.passport_series}-{obj.passport_number}"
#
#     @admin.display(description="Tug'ligan sanasi")
#     def day_to_birthday(self, obj: Student):
#         today = date.today()
#         next_birthday = date(today.year, obj.birth_date.month, obj.birth_date.day)
#
#         if next_birthday < today:
#             next_birthday = date(today.year + 1, obj.birth_date.month, obj.birth_date.day)
#
#         return f"{obj.birth_date}({(next_birthday - today).days})"
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(
#             _course_count=Count("courses", distinct=True),
#         )
#         return queryset
#
#     def course_count(self, obj) -> Any:
#         return obj._course_count
#
#     course_count.admin_order_field = '_course_count'


# from django.contrib.admin import AdminSite
#
#
# class EventAdminSite(AdminSite):
#     site_header = "UMSRA Events Admin"
#     site_title = "UMSRA Events Admin Portal"
#     index_title = "Welcome to UMSRA Researcher Events Portal"
#
#
# event_admin_site = EventAdminSite(name='event_admin')
#
# event_admin_site.register(Student)
# event_admin_site.register(Course)


from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Count

from apps.models import Product, Category, Tag, ProductImage, Review


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0

class ReviewModelAdmin(admin.StackedInline):
    model = Review
    min_num = 0
    extra = 0


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = 'name', 'category', 'price'
    filter_horizontal = 'tags',
    inlines = [ProductImageStackedInline, ReviewModelAdmin]


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = 'name', 'products_count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _product_count=Count("products", distinct=True),
        )
        return queryset

    @admin.display(description="Productlar soni" ,ordering='_products_count')
    def products_count(self, obj: Category):
        return obj._product_count

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = 'name',





admin.site.unregister(User)
admin.site.unregister(Group)
