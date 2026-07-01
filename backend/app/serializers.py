from rest_framework import serializers

from .models import Person


class FamilyTreeSerializer(serializers.ModelSerializer):
    generation = serializers.IntegerField(read_only=True)

    class Meta:
        model = Person
        fields = [
            'id', 
            'name', 
            'surname', 
            'identity_number', 
            'birth_date', 
            'father_id', 
            'mother_id', 
            'generation'
        ]


class RootAscendantSerializer(serializers.ModelSerializer):
    generations = serializers.IntegerField(source="generation", read_only=True)

    class Meta:
        model = Person
        fields = [
            'id', 
            'name', 
            'surname', 
            'identity_number', 
            'birth_date', 
            'generations'
        ]
