"""func_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from options_func import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = routers.DefaultRouter()
router.register(r'test', views.TestViewSet, basename="test")
router.register(r'quotes', views.QuotesSet, basename="quotes")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('usFunc2/admin/', admin.site.urls),
    path('usFunc2/', include(router.urls)),
    path('usFunc2/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # token method
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

