from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()  # Добавляем новое поле

    def get_lesson_count(self, obj):
        return obj.lessons.count()  # Возвращаем количество уроков, связанных с курсом

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count']  # Добавляем новое поле в вывод

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview']

class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Вложенный сериализатор

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count', 'lessons']