from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from apps.models import Product


def product_list_page(request):
    context = {
        'products': Product.objects.all()
    }

    return render(request, 'apps/product-grid.html', context)


def product_detail_page(request, pk):
    product = get_object_or_404(Product, id=pk)

    context = {
        'product': product,
        'tags': product.tags.all()
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


# class ProductGridView(TemplateView):
#     template_name = 'apps/product-grid.html'

