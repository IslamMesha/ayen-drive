from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drive.views import DocumentViewSet, DocumentSearch, HomePageView, login_view, logout_view

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', HomePageView.as_view(), name='home'),
    path('search/', DocumentSearch.as_view(), name='search'),
]
