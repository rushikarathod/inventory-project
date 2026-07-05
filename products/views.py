from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Count
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from orders.models import Order


@login_required
def dashboard(request):
    total_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(
        status="delivered"
    ).aggregate(total=Sum("total_amount"))["total"] or 0
    low_stock_products = Product.objects.filter(
        is_active=True,
        stock_quantity__lte=10
    )
    recent_orders = Order.objects.order_by("-created_at")[:5]
    total_categories = Category.objects.count()

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock_products,
        "recent_orders": recent_orders,
        "total_categories": total_categories,
    }
    return render(request, "products/dashboard.html", context)


@login_required
def product_list(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    products = Product.objects.filter(is_active=True).select_related("category")

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        )
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": category_id,
    }
    return render(request, "products/product_list.html", context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {
        "form": form,
        "title": "Add Product"
    })


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {
        "form": form,
        "title": "Edit Product"
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.is_active = False
        product.save()
        messages.success(request, "Product deleted successfully!")
        return redirect("product_list")
    return render(request, "products/product_confirm_delete.html", {
        "product": product
    })


@login_required
def category_list(request):
    categories = Category.objects.annotate(
        product_count=Count("products")
    )
    return render(request, "products/category_list.html", {
        "categories": categories
    })


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "products/category_form.html", {
        "form": form,
        "title": "Add Category"
    })


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "products/category_form.html", {
        "form": form,
        "title": "Edit Category"
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted!")
        return redirect("category_list")
    return render(request, "products/category_confirm_delete.html", {
        "category": category
    })