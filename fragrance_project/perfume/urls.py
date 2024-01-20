from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    PerfumeListView, 
    PerfumeDetailView, 
    PerfumeDeleteView,
    # UserPerfumeListView,
)
from .views import (
    about, 
    perfume_create_view, 
    perfume_update_view, 
    fragrance_view,
    # download
)


urlpatterns = [
    # path('', views.home, name='perfume-home'),
    path('', PerfumeListView.as_view(), name='perfume-home'),
    # path('user/<str:username>', UserPerfumeListView.as_view(), name='user-perfume'),
    path('perfume/<int:pk>/', PerfumeDetailView.as_view(), name='perfume-detail'),
    path('perfume/new/', perfume_create_view, name='perfume-create'),
    path('perfume/<int:pk>/update/', perfume_update_view, name='perfume-update'),
    # path('download/', download, name='download'),
    path('perfume/<int:pk>/delete/', PerfumeDeleteView.as_view(), name='perfume-delete'),
    path('fragrances/', fragrance_view, name='perfume-fragrance'),
    path('about/', about, name='perfume-about'),
    
]

if settings.DEBUG:  # allow our media to be accessed from browser
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
