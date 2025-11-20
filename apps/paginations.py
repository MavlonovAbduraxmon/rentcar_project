from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
        })


# from rest_framework.pagination import CursorPagination

#
#
#
# class CustomCursorPagination(CursorPagination):
#     page_query_param = 'page_number'
#     page_size_query_param = 'page_size'
#     ordering = ('-created_at', '-id')
#
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,
#             'next_page': self.get_next_link(),
#             'previous_page': self.get_previous_link(),
#             'data': data,
#         })