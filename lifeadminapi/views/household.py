from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from lifeadminapi.models import Household, HouseholdUser


class HouseholdView(ViewSet):
    """life admin category types"""


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        household_user = HouseholdUser.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        household = Household()
        household.name = request.data["name"]
        household.description = request.data["description"]

        # Try to save the new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
        try:
            household.save()
            serializer = HouseholdSerializer(household, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single categories
        Returns:
            Response -- JSON serialized category
        """
        try:
            household = Household.objects.get(pk=pk)
            serializer = HouseholdSerializer(household, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            household = Household.objects.get(pk=pk)
            household.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Household.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        households = Household.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = HouseholdSerializer(
            households, many=True, context={'request': request})
        return Response(serializer.data)

class HouseholdSerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Household
        fields = ('id','name', 'description',)