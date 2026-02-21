from rest_framework import serializers


### LESSONS
class LessonResponseDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField()
    html_content = serializers.CharField()
    course_id = serializers.IntegerField()
    author_id = serializers.IntegerField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class LessonCreateUpdateDTO(serializers.Serializer):
    topic = serializers.CharField(max_length=127, required=False)
    html_content = serializers.CharField(required=False)


### COURSE
class CourseResponseDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    is_active = serializers.BooleanField()
    author_id = serializers.IntegerField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    lessons = LessonResponseDTO(many=True, read_only=True)


class CourseCreateUpdateDTO(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
