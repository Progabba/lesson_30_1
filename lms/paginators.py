from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = "page_size"  # Параметр для изменения количества элементов
    max_page_size = 100  # Максимальное количество элементов на странице


class LessonPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50
