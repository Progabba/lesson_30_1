from rest_framework.viewsets import ModelViewSet


from .models import Course
from .serializers import CourseSerializer, CourseDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Lesson
from .serializers import LessonSerializer



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        # Используем детальный сериализатор для отдельных объектов
        if self.action in ['retrieve']:
            return CourseDetailSerializer
        # Используем базовый сериализатор для списка объектов
        return CourseSerializer

class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

