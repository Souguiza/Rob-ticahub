from django.contrib import admin

from courses.models import (
    Course,
    CourseCategory,
    CourseInstructor,
    CourseModule,
    Enrollment,
    LearningPath,
    Lesson,
    LessonProgress,
)

admin.site.register(CourseCategory)
admin.site.register(LearningPath)
admin.site.register(Course)
admin.site.register(CourseInstructor)
admin.site.register(CourseModule)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
