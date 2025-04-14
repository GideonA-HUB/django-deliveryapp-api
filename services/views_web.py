from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Service, Category
from .forms import ServiceForm

class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        queryset = Service.objects.all()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_services'] = Service.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:service-list')

    def test_func(self):
        return self.request.user.is_business

    def form_valid(self, form):
        form.instance.business = self.request.user.business
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'

    def test_func(self):
        service = self.get_object()
        return self.request.user.is_business and service.business == self.request.user.business

    def get_success_url(self):
        return reverse_lazy('services:service-detail', kwargs={'pk': self.object.pk})

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'
    success_url = reverse_lazy('services:service-list')

    def test_func(self):
        service = self.get_object()
        return self.request.user.is_business and service.business == self.request.user.business

class CategoryListView(ListView):
    model = Category
    template_name = 'services/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.service_count = Service.objects.filter(category=category).count()
        return context 