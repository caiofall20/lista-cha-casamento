from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
app_name = 'lista'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('login/gifts/', (views.GiftListView.as_view()), name='gifts'),
    path('report/', login_required(views.ReportView.as_view()), name='report'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('salva_convidado/', views.salva_convidado, name='salva_convidado'),
    path('product_update/<id>', views.product_update, name='product_update'),
    #path('product_update/', views.product_update, name='product_update'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)