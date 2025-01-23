from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()  # Добавляем новое поле
    is_subscribed = serializers.SerializerMethodField()  # Проверка подписки

    def get_lesson_count(self, obj):
        return obj.lessons.count()  # Возвращаем количество уроков, связанных с курсом

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "lesson_count",
            "user",
            "is_subscribed",
        ]  # Добавляем новое поле в вывод


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "video_url",
            "course",
            "user",
        ]

    def validate_course(self, value):
        if not Course.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Указанный курс не существует.")
        return value


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Вложенный сериализатор

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lesson_count", "lessons"]
