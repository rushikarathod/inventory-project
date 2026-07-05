from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Payment
from .forms import PaymentForm, PaymentStatusForm
from orders.models import Order


@login_required
def payment_create(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)

    if hasattr(order, "payment"):
        messages.warning(request, "Payment already exists for this order!")
        return redirect("payment_detail", pk=order.payment.pk)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.amount = order.total_amount
            if payment.status == Payment.Status.PAID:
                payment.paid_at = timezone.now()
            payment.save()
            messages.success(request, "Payment recorded successfully!")
            return redirect("payment_detail", pk=payment.pk)
    else:
        form = PaymentForm(initial={"amount": order.total_amount})

    return render(request, "payments/payment_form.html", {
        "form": form,
        "order": order,
        "title": "Create Payment",
    })


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, "payments/payment_detail.html", {"payment": payment})


@login_required
def payment_list(request):
    payments = Payment.objects.all().select_related("order").order_by("-created_at")
    status = request.GET.get("status", "")
    method = request.GET.get("method", "")

    if status:
        payments = payments.filter(status=status)
    if method:
        payments = payments.filter(method=method)

    context = {
        "payments": payments,
        "selected_status": status,
        "selected_method": method,
        "status_choices": Payment.Status.choices,
        "method_choices": Payment.Method.choices,
    }
    return render(request, "payments/payment_list.html", context)


@login_required
def payment_status_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentStatusForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            if payment.status == Payment.Status.PAID:
                payment.paid_at = timezone.now()
            payment.save()
            messages.success(request, f"Payment status updated to {payment.get_status_display()}!")
    return redirect("payment_detail", pk=pk)


@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            if payment.status == Payment.Status.PAID:
                payment.paid_at = timezone.now()
            payment.save()
            messages.success(request, "Payment updated successfully!")
            return redirect("payment_detail", pk=payment.pk)
    else:
        form = PaymentForm(instance=payment)
    return render(request, "payments/payment_form.html", {
        "form": form,
        "order": payment.order,
        "title": "Edit Payment",
    })