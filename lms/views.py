from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsOwner
from .models import Course, Subscription
from .paginators import CoursePagination, LessonPagination
from .serializers import CourseSerializer, CourseDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from .models import Lesson
from .serializers import LessonSerializer

from rest_framework.permissions import IsAuthenticated



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CoursePagination  # Подключение пагинации

    def get_serializer_class(self):
        # Используем детальный сериализатор для отдельных объектов
        if self.action in ['retrieve']:
            return CourseDetailSerializer
        # Используем базовый сериализатор для списка объектов
        return CourseSerializer


    def get_permissions(self):
        # Используем детальный сериализатор для отдельных объектов
        if self.action in ['create']:
            self.permission_classes = (~IsModer, )
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action in ['destroy']:
            self.permission_classes = (~IsModer | IsOwner,)
        # Используем базовый сериализатор для списка объектов
        return super().get_permissions()



    def perform_create(self, serializer):
        course = serializer.save()
        course.user = self.request.user
        course.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """Подписаться или отписаться от курса."""
        course = get_object_or_404(Course, pk=pk)
        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)

        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message}, status=HTTP_200_OK)


class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer, IsAuthenticated]
    pagination_class = LessonPagination  # Подключение пагинации

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        lesson.save()


class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message}, status=HTTP_200_OK)

