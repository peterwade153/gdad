import random
from datetime import date

from faker import Faker

from django.core.management.base import BaseCommand

from app.models import Person

# Initialize the default English generator
fake = Faker()


class Command(BaseCommand):
    help = "Seed 15-generation lineage dataset"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Family tree data...")

        Person.objects.all().delete()
        generations = []

        # Initialize a global counter to guarantee absolute uniqueness across generations
        global_counter = 1

        will = Person.objects.create(
            name="Will",
            surname="Smith",
            birth_date=date(1900, 1, 1),
            identity_number=f"GEN1-{global_counter:04d}",
        )
        global_counter += 1

        jane = Person.objects.create(
            name="Jane",
            surname="Smith",
            birth_date=date(1902, 1, 1),
            identity_number=f"GEN1-{global_counter:04d}",
        )
        global_counter += 1

        generations.append(([will], [jane]))

        for gen in range(2, 16):
            prev_gen_fathers, prev_gen_mothers = generations[-1]
            current_gen_fathers = []
            current_gen_mothers = []

            # Adding two people per generation, avoid explosions
            for i in ["father", "mother"]:
                father = random.choice(prev_gen_fathers)
                mother = random.choice(prev_gen_mothers)

                is_father = i == "father"
                name_suffix = "Father" if is_father else "Mother"

                person = Person.objects.create(
                    name=f"{fake.first_name_male() if is_father else fake.first_name_female() }",
                    surname=f"{fake.last_name()}-Smith",
                    birth_date=date(1900 + gen * 10, 1, 1),
                    identity_number=f"GEN{gen}-{global_counter:04d}",
                    father=father,
                    mother=mother,
                )
                global_counter += 1

                if is_father:
                    current_gen_fathers.append(person)
                else:
                    current_gen_mothers.append(person)
            # Append the current generation's split pools
            generations.append((current_gen_fathers, current_gen_mothers))

        self.stdout.write(self.style.SUCCESS("Family tree seeding complete."))
