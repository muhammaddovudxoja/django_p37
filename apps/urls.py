from django.urls import path

from apps.views import product_list_page, product_detail_page, user_login_page, user_register_page, test_page, \
    logout_page

urlpatterns = [
    path('', product_list_page, name='product_list_page'),
    path('product-detail/<int:pk>', product_detail_page, name='product_detail_page'),
    path("login", user_login_page, name='user_login_page'),
    path("register", user_register_page, name='user_register_page'),
    path("test", test_page, name='test_page'),
    path("logout", logout_page, name='logout_page'),
    # path('', ProductGridView.as_view(), name='grid_page'),
]
