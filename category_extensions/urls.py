from django.conf.urls import url

from .dashboard_views import views as dashboard_views

urlpatterns = [
    url(r'^dashboard/category-extensions/$',
        dashboard_views.category_extension_list,
        name='category-extension-dashboard-list'),
    url(r'^dashboard/category-extensions/create/$',
        dashboard_views.category_extension_create,
        name='category-extension-dashboard-create'),
    url(r'^dashboard/category-extensions/(?P<pk>[0-9]+)/$',
        dashboard_views.category_extension_details,
        name='category-extension-dashboard-detail'),
    url(r'^dashboard/category-extensions/(?P<pk>[0-9]+)/delete/$',
        dashboard_views.category_extension_delete,
        name='category-extension-dashboard-delete'),
]
