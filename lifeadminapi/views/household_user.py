"""View module for handling requests about categories"""

from lifeadminapi.models.household import Household
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lifeadminapi.models import HouseholdUser


class HouseholdUserView(ViewSet):
    """life admin category types"""


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        household_user = HouseholdUser()

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        household_user.user = User.objects.get(pk=request.data["user"])
        household_user.household = Household.objects.get(pk= request.data["household"])

        # Try to save the new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
        try:
            household_user.save()
            serializer = HouseholdUserSerializer(household_user, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single household users
        Returns:
            Response -- JSON serialized category
        """
        
        try:
            household_user = HouseholdUser.objects.get(pk=pk)
            user = User.objects.get(pk=pk)
            household_user.user = user
            serializer = HouseholdUserSerializer(household_user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        household_user = HouseholdUser.objects.get(user=request.auth.user)

        user = User.objects.get(pk=pk)
       

        household_user.user = user
        household_user.household = Household.objects.get(pk=request.data["household"])

        household_user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            household_user = HouseholdUser.objects.get(pk=pk)
            household_user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except HouseholdUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        household_users = HouseholdUser.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = HouseholdUserSerializer(
            household_users, many=True, context={'request': request})
        return Response(serializer.data)

class HouseholdUserSerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = HouseholdUser
        fields = ('id', 'user', 'household',)