from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404

from apps.models import Product, Test


def product_list_page(request):
    context = {
        'products': Product.objects.all()
    }

    return render(request, 'apps/product-grid.html', context)


def product_detail_page(request, pk):
    product = get_object_or_404(Product, id=pk)

    context = {
        'product': product,
        'tags': product.tags.all(),
    }

    return render(request, 'apps/product-details.html', context)


def user_login_page(request):
    context = {
    }

    return render(request, "apps/auth/login.html", context)


def user_register_page(request):
    context = {

    }

    return render(request, "apps/auth/register.html", context)


def logout_page(request):
    logout(request)
    return render(request, "apps/auth/login.html")

def test_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Test.objects.create(name=name, email=email, subject=subject, message=message)

    return render(request, "apps/test.html")

# class ProductGridView(TemplateView):
#     template_name = 'apps/product-grid.html'
