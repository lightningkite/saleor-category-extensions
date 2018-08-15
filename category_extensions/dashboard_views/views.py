from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from saleor.core.utils import get_paginator_items
from saleor.dashboard.views import staff_member_required
from .filters import CategoryExtensionFilter
from .forms import CategoryExtensionForm

from ..models import CategoryExtension


@staff_member_required
@permission_required('category_extensions.view')
def category_extension_list(request):
    category_extensions = (
        CategoryExtension.objects.all().select_related('category')
        .order_by('category'))
    category_extension_filter = CategoryExtensionFilter(
        request.GET, queryset=category_extensions)
    category_extensions = get_paginator_items(
        category_extensions, settings.DASHBOARD_PAGINATE_BY, request.GET.get('page'))
    # Call this so that cleaned_data exists on the filter_set
    category_extension_filter.form.is_valid()
    ctx = {
        'category_extensions': category_extensions, 'filter_set': category_extension_filter,
        'is_empty': not category_extension_filter.queryset.exists()}
    return TemplateResponse(request, 'category_extensions/dashboard/list.html', ctx)


@staff_member_required
@permission_required('category_extensions.edit')
def category_extension_create(request):
    category_extension = CategoryExtension()
    form = CategoryExtensionForm(request.POST or None)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy('Dashboard message', 'Created category extension')
        messages.success(request, msg)
        return redirect('category-extension-dashboard-list')
    ctx = {'category_extension': category_extension, 'form': form}
    return TemplateResponse(request, 'category_extensions/dashboard/detail.html', ctx)


@staff_member_required
@permission_required('category_extensions.edit')
def category_extension_details(request, pk):
    category_extension = CategoryExtension.objects.get(pk=pk)
    form = CategoryExtensionForm(
        request.POST or None, instance=category_extension)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Updated category extension %s') % category_extension.name
        messages.success(request, msg)
        return redirect('category-extension-dashboard-list')
    ctx = {'category_extension': category_extension, 'form': form}
    return TemplateResponse(request, 'category_extensions/dashboard/detail.html', ctx)


@staff_member_required
@permission_required('category_extensions.edit')
def category_extension_delete(request, pk):
    category_extension = get_object_or_404(CategoryExtension, pk=pk)
    if request.method == 'POST':
        category_extension.delete()
        msg = pgettext_lazy('Dashboard message',
                            'Removed category extension %s') % category_extension
        messages.success(request, msg)
        return redirect('category-extension-dashboard-list')
    return TemplateResponse(
        request, 'category_extensions/dashboard/modal/confirm_delete.html', {'category_extension': category_extension})
