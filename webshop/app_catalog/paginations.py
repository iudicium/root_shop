from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class CatalogItemPagination(PageNumberPagination):
    page_query_param = "currentPage"
    default_limit = 5
    max_limit = 60
    page_size = 20  # Set the desired page size
    page_size_query_param = "page_size"
    max_page_size = 60

    # # This function is used for debug only
    # def get_page_number(self, request, paginator):
    #     page_number = request.query_params.get(self.page_query_param)
    #     print("Raw page number:", page_number)
    #     print("All query parameters:", request.query_params)
    #
    #     try:
    #         page_number = int(page_number)
    #     except (TypeError, ValueError):
    #         page_number = 1
    #
    #     print("Processed page number:", page_number)
    #     # print(self.get_page_number(self.request, self.page.paginator))
    #     return page_number

    def get_paginated_response(self, data):
        last_page_number = self.page.paginator.num_pages
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": last_page_number,
            }
        )
