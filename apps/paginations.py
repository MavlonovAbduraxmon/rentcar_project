from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response



class CustomCursorPagination(CursorPagination):
    ordering = '-created_at'


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = 'page_number'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'data': data,
        })