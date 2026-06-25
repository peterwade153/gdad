from django.db import models


class Person(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="Id")
    father = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="father_children",
        db_column="FatherId",
    )
    mother = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mother_children",
        db_column="MotherId",
    )
    name = models.CharField(max_length=100, db_column="Name")
    surname = models.CharField(max_length=100, db_column="Surname")
    birth_date = models.DateField(null=True, blank=True, db_column="BirthDate")
    identity_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        db_column="IdentityNumber",
    )
    class Meta:
        db_table = "site_person"
