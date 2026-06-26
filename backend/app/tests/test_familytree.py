from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Person


class FamilyTreeTestCase(APITestCase):
    def setUp(self):
        """
        Set up a mock lineage tree to test tracking, deduplication, and generations.
        We will create a scenario where 'Grandpa' is linked through multiple paths.
        """
        # Generation 3 (Root Ancestor)
        self.grandpa = Person.objects.create(
            name="Arthur",
            surname="Smith",
            birth_date=date(1920, 1, 1),
            identity_number="GEN3-0001",
        )

        # Generation 2 (Parents' Era)
        self.father = Person.objects.create(
            name="Charles",
            surname="Smith",
            birth_date=date(1950, 1, 1),
            identity_number="GEN2-0001",
            father=self.grandpa,
        )
        self.mother = Person.objects.create(
            name="Jane",
            surname="Smith",
            birth_date=date(1952, 1, 1),
            identity_number="GEN2-0002",
        )

        # Generation 1 (Target Focus Individual)
        self.target_person = Person.objects.create(
            name="John",
            surname="Smith",
            birth_date=date(1980, 1, 1),
            identity_number="GEN1-0001",
            father=self.father,
            mother=self.mother,
        )

        # Reverse URL name assumption: 'family-tree' matching your URL conf path
        self.url = reverse(
            "api-family-tree",
            kwargs={"identity_number": self.target_person.identity_number},
        )

    def test_person_not_found_returns_404(self):
        """Test looking up an invalid or missing identity number returns a clean 404."""
        url = reverse("api-family-tree", kwargs={"identity_number": "DOES-NOT-EXIST"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_get_lineage_tree_success(self):
        """Test fetching a valid lineage tree"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        # We expect exactly 4 unique records in total
        self.assertEqual(len(response.data), 4)

        # Linkage preserved, find our target person node in the flat array
        target_node = next(
            node for node in response.data if node["id"] == self.target_person.id
        )

        # Check that parents collection references his actual father and mother
        self.assertEqual(self.father.identity_number, target_node["father_id"])
        self.assertEqual(self.mother.identity_number, target_node["mother_id"])
