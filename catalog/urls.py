from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path('home/', views.ProductHomeListView.as_view(), name='home'),
    path('list/', views.ProductsListView.as_view(), name='list'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.ProductDeleteView.as_view(), name='delete'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('publish/<int:pk>/', views.UnpublishProductView.as_view(), name='publish')
]
