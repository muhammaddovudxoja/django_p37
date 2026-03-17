from django.urls import path

from apps.views import product_list_page, product_detail_page, user_login_page, user_register_page

urlpatterns = [
    path('', product_list_page, name='product_list_page'),
    path('product-detail/<int:pk>', product_detail_page, name='product_detail_page'),
    path("", user_login_page, name='user_login_page'),
    path("", user_register_page, name='user_register_page'),
    # path('', ProductGridView.as_view(), name='grid_page'),
]
