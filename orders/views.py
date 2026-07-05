from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet, CheckoutForm
from products.models import Product, Category


# ---------- STAFF/ADMIN ORDER MANAGEMENT ----------

@login_required
def order_list(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    orders = Order.objects.all().order_by("-created_at")

    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_email__icontains=query)
        )
    if status:
        orders = orders.filter(status=status)

    context = {
        "orders": orders,
        "query": query,
        "selected_status": status,
        "status_choices": Order.Status.choices,
    }
    return render(request, "orders/order_list.html", context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            order.calculate_total()
            messages.success(request, f"Order #{order.order_number} created!")
            return redirect("order_detail", pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, "orders/order_form.html", {
        "form": form,
        "formset": formset,
        "title": "Create Order",
    })


@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            order.calculate_total()
            messages.success(request, f"Order #{order.order_number} updated!")
            return redirect("order_detail", pk=order.pk)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, "orders/order_form.html", {
        "form": form,
        "formset": formset,
        "title": "Edit Order",
    })


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted!")
        return redirect("order_list")
    return render(request, "orders/order_confirm_delete.html", {"order": order})


@login_required
def order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save()
            messages.success(request, f"Status updated to {order.get_status_display()}!")
    return redirect("order_detail", pk=pk)


# ---------- CUSTOMER STOREFRONT ----------

@login_required
def storefront(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    products = Product.objects.filter(is_active=True, stock_quantity__gt=0)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, "orders/storefront.html", {
        "products": products,
        "categories": categories,
        "query": query,
    })


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data["quantity"]

            if qty > product.stock_quantity:
                messages.error(request, f"Only {product.stock_quantity} units available!")
                return redirect("buy_now", product_id=product.id)

            order = Order.objects.create(
                customer=request.user,
                customer_name=request.user.get_full_name() or request.user.username,
                customer_email=request.user.email,
                customer_phone=form.cleaned_data["phone"],
                shipping_address=form.cleaned_data["shipping_address"],
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                unit_price=product.price,
            )
            order.calculate_total()

            product.stock_quantity -= qty
            product.save()

            messages.success(request, f"Order #{order.order_number} placed successfully!")
            return redirect("my_orders")
    else:
        form = CheckoutForm(initial={
            "shipping_address": request.user.address,
            "phone": request.user.phone,
        })

    return render(request, "orders/buy_now.html", {
        "form": form,
        "product": product,
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})