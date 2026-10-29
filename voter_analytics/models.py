import csv
from datetime import datetime

from django.db import models

# Create your models here.
class Voter(models.Model):
    '''Model for a single registered voter, loaded from newton_voters.csv.'''

    voter_id = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True)
    date_of_registration = models.DateField(null=True)
    party_affiliation = models.CharField(max_length=10)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.voter_id})'


def _parse_date(value):
    '''Parse a YYYY-MM-DD date, returning None for malformed placeholders like 1900-01-00.'''
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def load_data(csv_path='voter_analytics/newton_voters.csv'):
    '''Load voter records from newton_voters.csv into the database.'''

    Voter.objects.all().delete()

    voters = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            voters.append(Voter(
                voter_id=row['Voter ID Number'],
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'],
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=_parse_date(row['Date of Birth']),
                date_of_registration=_parse_date(row['Date of Registration']),
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],
                v20state=row['v20state'].strip().upper() == 'TRUE',
                v21town=row['v21town'].strip().upper() == 'TRUE',
                v21primary=row['v21primary'].strip().upper() == 'TRUE',
                v22general=row['v22general'].strip().upper() == 'TRUE',
                v23town=row['v23town'].strip().upper() == 'TRUE',
                voter_score=int(row['voter_score']),
            ))

    Voter.objects.bulk_create(voters)
    print(f'Loaded {len(voters)} voters.')
