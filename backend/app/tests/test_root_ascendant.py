from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Person


class PersonRootAscendantTestCase(APITestCase):
    def setUp(self):
        """
        Set up a mock lineage tree to test get root ascendant.
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
        # Reverse URL name assumption: 'root-ascendant' matching your URL conf path
        self.url = reverse(
            "api-root-ascendant",
            kwargs={"identity_number": self.target_person.identity_number},
        )

    def test_person_not_found_returns_404(self):
        """Test looking up an invalid or missing identity number returns a clean 404."""
        url = reverse(
            "api-root-ascendant", kwargs={"identity_number": "DOES-NOT-EXIST"}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['root_ascendants'], [])

    def test_get_root_ascendant_success(self):
        """Test fetching a root ascendant"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["root_ascendants"]), 1)
        # Linkage preserved, find our target person node in the flat array
        target_node = response.data["root_ascendants"][0]

        # Check that parents collection references his actual father and mother
        self.assertEqual(self.grandpa.identity_number, target_node["identity_number"])
        self.assertEqual(self.grandpa.name, target_node["name"])
        self.assertEqual(self.grandpa.surname, target_node["surname"])
