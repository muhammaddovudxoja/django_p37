from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import F, Q
from django.http import HttpResponseRedirect, request
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView

from apps.forms import RegisterUserModelForm, TodoUpdateListForm
from apps.models import Product, Cart, Category, Todo
from root.settings import EMAIL_HOST_USER


class CategoryMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductListView(CategoryMixin, ListView):
    template_name = "apps/product-grid.html"
    queryset = Product.objects.all()
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        if _category := self.request.GET.get("category"):
            qs = qs.filter(category_id=_category)

        if _search := self.request.GET.get("search"):
            qs = qs.filter(Q(name__icontains=_search) | Q(description__icontains=_search))
        return qs


class ProductDetailView(CategoryMixin, DetailView):
    template_name = "apps/product-details.html"
    queryset = Product.objects.all()
    context_object_name = "product"



class CustomLoginView(LoginView):
    template_name = "apps/auth/login.html"
    next_page = "product_list_page"


class RegisterCreateView(CreateView):
    queryset = User.objects.all()
    form_class = RegisterUserModelForm
    template_name = "apps/auth/register.html"
    success_url = reverse_lazy("product_list_page")

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        # subject = "Ro'yxatdan o'tish"
        # message = f"{self.object.first_name}Bizning saytda ro'yxatdan o'tdingiz"
        # send_mail(subject, message, EMAIL_HOST_USER, [self.object.email])
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("product_list_page")


class CheckoutListView(CategoryMixin, LoginRequiredMixin, ListView):
    template_name = "apps/checkout.html"
    queryset = Cart.objects.all()

class ShoppingCartListView(LoginRequiredMixin, ListView):
    template_name = "apps/shopping-cart.html"
    queryset = Cart.objects.all()
    context_object_name = "carts"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        user = self.request.user
        context["categories"] = Category.objects.all()
        total_price = 0
        total_count = 0
        for cart in user.carts.all():
            total_price += cart.product.current_price * cart.quantity
            total_count += cart.quantity
        context["total_price"] = total_price
        context["total_count"] = total_count


        return context


class AddCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart.quantity = F("quantity") + 1
            cart.save()

        return redirect(request.META['HTTP_REFERER'])


class RemoveCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        Cart.objects.filter(id=pk).delete()
        return redirect('cart_page')


class TodoListView(ListView):
    template_name = "apps/todo.html"
    queryset = Todo.objects.all()
    context_object_name = "todos"

    def get_queryset(self):
        qs = super().get_queryset()
        if _search := self.request.GET.get("search"):
            qs = qs.filter(Q(title__icontains=_search))
        return qs

class TodoDetailView(DetailView):
    queryset = Todo.objects.all()
    template_name = "apps/todo_detail.html"
    context_object_name = "todo"


class RemoveTodo(View):
    def get(self, request, pk, *args, **kwargs):
        Todo.objects.filter(id=pk).delete()
        return redirect("todo_page")


class UpdateTodo(UpdateView):
    queryset = Todo.objects.all()
    form_class = TodoUpdateListForm


# def test_page(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         subject = request.POST.get("subject")
#         message = request.POST.get("message")
#         Test.objects.create(name=name, email=email, subject=subject, message=message)
#
#     return render(request, "apps/test.html")
#
#
# def test4_page(request):
#     if request.method == "POST":
#         user_name = request.POST.get("user_name")
#         user_password = request.POST.get("user_password")
#         password_confirm = request.POST.get("password_confirm")
#         user_email = request.POST.get("user_email")
#         user_answer = request.POST.get("user_answer")
#         user_question = request.POST.get("user_question")
#         Test4.objects.create(user_name=user_name, password=user_password, email=user_email, answer=user_answer,
#                              question_type=user_question)
#         if user_password != password_confirm:
#             return render(request, "apps/test4.html")
#     context = {
#         "choices": Test4.QuestionType,
#     }
#     return render(request, "apps/test4.html", context)

# class ProductGridView(TemplateView):
#     template_name = 'apps/product-grid.html'
