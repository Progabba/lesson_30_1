from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class LessonCRUDTests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.moderator = User.objects.create_user(email='moderator@test.com', password='password', is_moderator=True)
        self.user = User.objects.create_user(email='user@test.com', password='password')

        # Создаем тестовый курс
        self.course = Course.objects.create(title="Test Course", description="Description", user=self.moderator)

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(title="Lesson 1", description="Description", course=self.course, user=self.moderator)

        # Настраиваем клиента
        self.client = APIClient()

    def test_lesson_creation_by_moderator(self):
        """Проверка создания урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post('/lessons/', {
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_creation_by_user(self):
        """Проверка, что обычный пользователь не может создать урок"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lessons/', {
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_retrieval(self):
        """Проверка получения урока"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_lesson_update(self):
        """Проверка обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(f'/lessons/{self.lesson.id}/', {
            'title': 'Updated Lesson'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson')

    def test_lesson_deletion(self):
        """Проверка удаления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f'/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CourseSubscriptionTests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(email='user@test.com', password='password')

        # Создаем тестовый курс
        self.course = Course.objects.create(title="Test Course", description="Description", user=self.user)

        # Настраиваем клиента
        self.client = APIClient()

    def test_subscribe_to_course(self):
        """Проверка подписки на курс"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """Проверка отписки от курса"""
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)  # Предварительно подписываем
        response = self.client.post(f'/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
