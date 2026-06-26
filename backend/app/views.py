from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Person
from .mixins import FamilyTreeCacheMixin


class PersonFamilyTreeListView(FamilyTreeCacheMixin, APIView):

    def get(self, request, identity_number, *args, **kwargs):
        max_gen = int(request.query_params.get('max_generation', 10))

        person = Person.objects.filter(identity_number=identity_number).values("identity_number").first()
        if not person:
            return Response({"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND)

        person_identity_number = person['identity_number']

        query = """
            WITH RECURSIVE lineage AS (
                -- Start with the target individual
                SELECT "Id", "Name", "Surname", "IdentityNumber", "BirthDate", "FatherId", "MotherId", 1 AS generation
                FROM site_person 
                WHERE "IdentityNumber" = %s
                
                UNION ALL
                
                -- Recursive step: Step up through ancestral lines
                SELECT p."Id", p."Name", p."Surname", p."IdentityNumber", p."BirthDate", p."FatherId", p."MotherId", l.generation + 1
                FROM site_person p 
                INNER JOIN lineage l ON p."IdentityNumber" = l."FatherId" OR p."IdentityNumber" = l."MotherId"
                WHERE l.generation < %s
            ) 
            SELECT DISTINCT "Id", "Name", "Surname", "IdentityNumber", "BirthDate", "FatherId", "MotherId", generation 
            FROM lineage
            ORDER BY generation ASC;
        """
        raw_results = Person.objects.raw(query, [person_identity_number, max_gen])

        result = []
        for person in raw_results:
            result.append(
                {
                    "id": person.id,
                    "name": person.name,
                    "surname": person.surname,
                    "identity_number": person.identity_number,
                    "birth_date": person.birth_date.isoformat() if person.birth_date else None,
                    "father_id": person.father_id,  
                    "mother_id": person.mother_id,
                    "generation": person.generation,
                }
            )

        return Response(
            result,
            status=status.HTTP_200_OK
        )
