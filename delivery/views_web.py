from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Delivery, DeliveryZone
from .forms import DeliveryForm, DeliveryUpdateForm

class DeliveryListView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = 'delivery/delivery_list.html'
    context_object_name = 'deliveries'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_rider:
            return Delivery.objects.filter(rider=self.request.user.rider)
        elif self.request.user.is_business:
            return Delivery.objects.filter(order__service__business=self.request.user.business)
        else:
            return Delivery.objects.filter(order__user=self.request.user)

class DeliveryDetailView(LoginRequiredMixin, DetailView):
    model = Delivery
    template_name = 'delivery/delivery_detail.html'
    context_object_name = 'delivery'

    def get_queryset(self):
        if self.request.user.is_rider:
            return Delivery.objects.filter(rider=self.request.user.rider)
        elif self.request.user.is_business:
            return Delivery.objects.filter(order__service__business=self.request.user.business)
        else:
            return Delivery.objects.filter(order__user=self.request.user)

class DeliveryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Delivery
    form_class = DeliveryForm
    template_name = 'delivery/delivery_form.html'
    success_url = reverse_lazy('delivery:delivery-list')

    def test_func(self):
        return self.request.user.is_business

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        return super().form_valid(form)

class DeliveryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Delivery
    form_class = DeliveryUpdateForm
    template_name = 'delivery/delivery_form.html'

    def test_func(self):
        delivery = self.get_object()
        return (self.request.user.is_rider and delivery.rider == self.request.user.rider) or \
               (self.request.user.is_business and delivery.order.service.business == self.request.user.business)

    def get_success_url(self):
        return reverse_lazy('delivery:delivery-detail', kwargs={'pk': self.object.pk})

class DeliveryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Delivery
    template_name = 'delivery/delivery_confirm_delete.html'
    success_url = reverse_lazy('delivery:delivery-list')

    def test_func(self):
        delivery = self.get_object()
        return self.request.user.is_business and delivery.order.service.business == self.request.user.business

class RiderDeliveryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Delivery
    template_name = 'delivery/rider_delivery_list.html'
    context_object_name = 'deliveries'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_rider

    def get_queryset(self):
        return Delivery.objects.filter(rider=self.request.user.rider)

class RiderDeliveryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Delivery
    template_name = 'delivery/rider_delivery_detail.html'
    context_object_name = 'delivery'

    def test_func(self):
        delivery = self.get_object()
        return self.request.user.is_rider and delivery.rider == self.request.user.rider

class RiderDeliveryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Delivery
    form_class = DeliveryUpdateForm
    template_name = 'delivery/rider_delivery_form.html'

    def test_func(self):
        delivery = self.get_object()
        return self.request.user.is_rider and delivery.rider == self.request.user.rider

    def get_success_url(self):
        return reverse_lazy('delivery:rider-delivery-detail', kwargs={'pk': self.object.pk})

class DeliveryZoneListView(ListView):
    model = DeliveryZone
    template_name = 'delivery/zone_list.html'
    context_object_name = 'zones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for zone in context['zones']:
            zone.delivery_count = Delivery.objects.filter(zone=zone).count()
        return context

class DeliveryZoneDetailView(DetailView):
    model = DeliveryZone
    template_name = 'delivery/zone_detail.html'
    context_object_name = 'zone'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_deliveries'] = Delivery.objects.filter(
            zone=self.object,
            status__in=['pending', 'assigned', 'in_progress']
        )
        return context 