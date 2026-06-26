from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Person
from .mixins import FamilyTreeCacheMixin


class PersonFamilyTreeListView(FamilyTreeCacheMixin, APIView):

    def get(self, request, identity_number, *args, **kwargs):
        max_gen = int(request.query_params.get("max_generation", 10))

        person = (
            Person.objects.filter(identity_number=identity_number)
            .values("identity_number")
            .first()
        )
        if not person:
            return Response(
                {"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND
            )

        person_identity_number = person["identity_number"]

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
        result = [
            {
                "id": p.id,
                "name": p.name,
                "surname": p.surname,
                "identity_number": p.identity_number,
                "birth_date": p.birth_date.isoformat() if p.birth_date else None,
                "father_id": p.father_id,
                "mother_id": p.mother_id,
                "generation": p.generation,
            }
            for p in raw_results
        ]
        return Response(result, status=status.HTTP_200_OK)


class PersonRootAscendantView(FamilyTreeCacheMixin, APIView):
    def get(self, request, identity_number, *args, **kwargs):
        person = (
            Person.objects.filter(identity_number=identity_number)
            .values("identity_number")
            .first()
        )
        if not person:
            return Response(
                {"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND
            )

        person_identity_number = person["identity_number"]

        # Upstream tracking parents/ancestors where parent ID matches previous row's FatherId or MotherId
        query = """
            WITH RECURSIVE upstream_lineage AS (
                -- Start with the target individual
                SELECT "Id", "Name", "Surname", "IdentityNumber", "BirthDate", "FatherId", "MotherId", 1 AS generation
                FROM site_person 
                WHERE "IdentityNumber" = %s
                
                UNION ALL

                -- Move upwards to ancestors
                SELECT p."Id", p."Name", p."Surname", p."IdentityNumber", p."BirthDate", p."FatherId", p."MotherId", ul.generation + 1
                FROM site_person p
                INNER JOIN upstream_lineage ul ON p."IdentityNumber" = ul."FatherId" OR p."IdentityNumber" = ul."MotherId"
            ),
            max_generation AS (
                SELECT MAX(generation) AS max_gen FROM upstream_lineage
            )
            SELECT DISTINCT ul.*
            FROM upstream_lineage ul
            CROSS JOIN max_generation mg
            WHERE ul.generation = mg.max_gen;
        """
        raw_results = Person.objects.raw(query, [person_identity_number])

        roots = [
            {
                "id": p.id,
                "name": p.name,
                "surname": p.surname,
                "identity_number": p.identity_number,
                "birth_date": p.birth_date.isoformat() if p.birth_date else None,
                "generations": p.generation,
            }
            for p in raw_results
        ]
        return Response(
            {
                "max_depth_reached": roots[0]["generations"] if roots else 0,
                "root_ascendants": roots,
            },
            status=status.HTTP_200_OK,
        )
