from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Person
from .mixins import FamilyTreeCacheMixin
from .serializers import FamilyTreeSerializer, RootAscendantSerializer


class PersonFamilyTreeListView(FamilyTreeCacheMixin, APIView):

    def get(self, request, *args, **kwargs):
        max_gen = int(request.query_params.get("max-generation", 10))
        identity_number = request.query_params.get("identity-number")

        if identity_number:
            start_condition = 'WHERE "IdentityNumber" = %s'
            params = [identity_number, max_gen]
        else:
            # Root people, with no parents defined
            start_condition = 'WHERE "FatherId" IS NULL AND "MotherId" IS NULL'
            params = [max_gen]

        query = f"""
            WITH RECURSIVE lineage AS (
                -- Start with the target individual
                SELECT 
                    p."Id", p."Name", p."Surname", p."IdentityNumber", p."BirthDate", p."FatherId", p."MotherId", 1 AS generation
                FROM site_person p
                {start_condition}
                
                UNION ALL
                
                -- Recursive step: Step up through ancestral lines
                SELECT 
                    p."Id",
                    p."Name",
                    p."Surname",
                    p."IdentityNumber",
                    p."BirthDate",
                    p."FatherId",
                    p."MotherId",
                    l.generation + 1
                FROM site_person p 
                INNER JOIN lineage l ON l."IdentityNumber" IN (p."FatherId", p."MotherId")
                WHERE l.generation < %s
            )
            SELECT DISTINCT ON (l."IdentityNumber") 
                l."Id",
                l."Name", 
                l."Surname",
                l."IdentityNumber",
                l."BirthDate",
                l."FatherId",
                l."MotherId",
                l.generation AS generation
            FROM lineage l
            ORDER BY l."IdentityNumber", generation ASC;
        """
        raw_results = Person.objects.raw(query, params)
        gen_count = max((p.generation for p in raw_results), default=0)
        serializer = FamilyTreeSerializer(raw_results, many=True)
        return Response(
            {
                "people": serializer.data,
                "generations": gen_count,
            }, 
            status=status.HTTP_200_OK
        )


class PersonRootAscendantView(FamilyTreeCacheMixin, APIView):
    def get(self, request, identity_number, *args, **kwargs):
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
        raw_results = Person.objects.raw(query, [identity_number])

        max_depth = raw_results[0].generation if raw_results else 0
        serializer = RootAscendantSerializer(raw_results, many=True)
        return Response(
            {
                "max_depth_reached": max_depth,
                "root_ascendants": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
