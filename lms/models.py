from django.db import models




class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField()

    def __str__(self):
        return self.title
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=True, null=True)

class Subscription(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="subscriptions", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions", blank=True, null=True)