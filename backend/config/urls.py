from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, UserViewSet, me
from courses.views import CourseViewSet, EnrollmentViewSet, LearningPathViewSet, LessonProgressViewSet
from organizations.views import OrganizationViewSet, TeamViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("teams", TeamViewSet, basename="teams")
router.register("learning-paths", LearningPathViewSet, basename="learning-paths")
router.register("courses", CourseViewSet, basename="courses")
router.register("enrollments", EnrollmentViewSet, basename="enrollments")
router.register("progress", LessonProgressViewSet, basename="progress")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/me/", me, name="me"),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
