from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from rest_framework.schemas import get_schema_view

from apps.article.views import ArticleViewSet
from apps.event.views import EventViewSet
from apps.seating.views import AreaLayoutViewSet, SeatViewSet, SeatingViewSet
from apps.ticket.views import TicketTypeViewSet, TicketViewSet
from apps.user.views import UserViewSet

from authentication.views import LoginFailureView

from common.permissions import AllowAll
from common.routers import PublicDefaultRouter


admin.site.site_header = settings.SITE_NAME

schema_view = get_schema_view(title=settings.APP_NAME, permission_classes=[AllowAll])
router = PublicDefaultRouter()

# Article app
router.register(r"articles", ArticleViewSet)

# Event app
router.register(r"events", EventViewSet)

# Seating app
router.register(r"seatings", SeatingViewSet)
router.register(r"seating_area_layouts", AreaLayoutViewSet)
router.register(r"seats", SeatViewSet)

# Ticket app
router.register(r"ticket_types", TicketTypeViewSet)
router.register(r"tickets", TicketViewSet)

# User app
router.register(r"users", UserViewSet)

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"grappelli/", include("grappelli.urls")),
    path(r"schema/", schema_view, name="schema"),
    path(r"auth/", include("rest_framework.urls")),
    path(r"oidc/", include("mozilla_django_oidc.urls")),
    path(r"login_failure/", LoginFailureView.as_view()),
    path(r"v0/", include(router.urls)),
    # path(r"favicon.ico", RedirectView.as_view(url="/static/images/favicon.ico", permanent=True)),
    path(r"", RedirectView.as_view(url="/v0", permanent=False)),
]
