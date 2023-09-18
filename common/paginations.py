from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    A simple general purpose pagination class with default settings
    to reuse in list views.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
