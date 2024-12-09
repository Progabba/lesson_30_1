from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsOwner
from .models import Course
from .serializers import CourseSerializer, CourseDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Lesson
from .serializers import LessonSerializer

from rest_framework.permissions import IsAuthenticated



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

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


class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer, IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        lesson.save()


class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

