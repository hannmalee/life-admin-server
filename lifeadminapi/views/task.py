"""View module for handling requests about categories"""
from lifeadminapi.models.household_user import HouseholdUser
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lifeadminapi.models import Task, Category


class TaskView(ViewSet):
    """life admin task types"""


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        household_user = HouseholdUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        user_assigned = HouseholdUser.objects.get(pk=request.data["assigned_to"])

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        task = Task()
        task.title = request.data["title"]
        task.description = request.data["description"]
        task.is_completed = request.data["is_completed"]
        task.created_on = request.data["created_on"]
        task.due_date = request.data["due_date"]
        task.category = category
        task.assigned_to = user_assigned
        task.created_by = household_user

        # Try to save the new task to the database, then
        # serialize the task instance as JSON, and send the
        # JSON as a response to the client request
        try:
            task.save()
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tasks
        Returns:
            Response -- JSON serialized task
        """
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a task

        Returns:
            Response -- Empty body with 204 status code
        """
        household_user = HouseholdUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        user_assigned = HouseholdUser.objects.get(pk=request.data["assigned_to"])

        task = Task.objects.get(pk=pk)
        task.title = request.data["title"]
        task.description = request.data["description"]
        task.is_completed = request.data["is_completed"]
        task.created_on = request.data["created_on"]
        task.due_date = request.data["due_date"]
        task.category = category
        task.assigned_to = user_assigned
        task.created_by = household_user

        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single task

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            task = Task.objects.get(pk=pk)
            task.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        tasks = Task.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TaskSerializer(
            tasks, many=True, context={'request': request})
        return Response(serializer.data)

class TaskSerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'is_completed', 'created_on', 'due_date', 'category', 'assigned_to', 'created_by')