from rest_framework.routers import DefaultRouter

from .api_views import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)