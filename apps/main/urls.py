from rest_framework.routers import DefaultRouter
from apps.main import views


main_router = DefaultRouter()
main_router.register(r'posts', views.PostViewSet)
main_router.register(r'analytics', views.AnalyticViewSet)
