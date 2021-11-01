from rest_framework import serializers
from .models import Drone, DroneCategory, Pilot, Competition
import drones.views
from django.contrib.auth.models import User


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    # drones = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='drone-detail')

    class Meta:
        model = DroneCategory
        fields = ('url', 'pk', 'name', 'drones')


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    # Display the category name
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')
    # Display the owner's username (read-only)
    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Drone
        fields = (
            'url',
            'name',
            'owner',
            'drone_category',
            'manufacturing_date',
            'has_it_competed',
            'inserted_timestamp')


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    # Display all the details for the related drone
    drone = DroneSerializer()

    class Meta:
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'drone')

    """The CompetitionSerializer class is a subclass of the HyperlinkedModelSerializer
class. We will use the CompetitionSerializer class to serialize Competition
instances related to a Pilot, that is, to display all the competitions in which
a specific Pilot has participated when we serialize a Pilot. We want to
display all the details for the related Drone, but we don't include the related
Pilot because the Pilot will use this CompetitionSerializer serializer."""


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Pilot
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'races_count',
            'inserted_timestamp',
            'competitions')

    """The PilotSerializer class declares a competitions attribute that holds and
instance of the previously coded CompetitionSerializer class. The many
argument is set to True because it is a one-to-many relationship (one Pilot
has many related Competition instances).
"""


class PilotCompetitionSerializer(serializers.ModelSerializer):
    # Display the pilot's name
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name')
    # Display the drone's name
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name')

    class Meta:
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'pilot',
            'drone')


class UserDroneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Drone
        fields = (
            'url',
            'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    drones = UserDroneSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'drone')
