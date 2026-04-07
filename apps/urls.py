from django.urls import path

from apps.views import ProductListView, ProductDetailView, CustomLoginView, \
    CustomLogoutView, RegisterCreateView, ShoppingCartListView, CheckoutListView, AddCartView, RemoveCartView, \
    TodoListView, TodoDetailView, RemoveTodo, UpdateTodo

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail_page'),
    path("login", CustomLoginView.as_view(), name='login_page'),
    path("register", RegisterCreateView.as_view(), name='register_page'),
    path("logout", CustomLogoutView.as_view(), name='logout_page'),
    path("cart", ShoppingCartListView.as_view(), name='cart_page'),
    path("checkout", CheckoutListView.as_view(), name='checkout_page'),
    path("add_to_cart/<int:pk>", AddCartView.as_view(), name='add_to_cart'),
    path("remove-cart/<int:pk>", RemoveCartView.as_view(), name='remove_cart'),
    path("todo", TodoListView.as_view(), name='todo_page'),
    path("todo-detail/<int:pk>", TodoDetailView.as_view(), name='todo_detail_page'),
    path("remove-todo/<int:pk>", RemoveTodo.as_view(), name='remove_todo'),
    path("update-todo/<int:pk>", UpdateTodo.as_view(), name='update_todo'),
]
