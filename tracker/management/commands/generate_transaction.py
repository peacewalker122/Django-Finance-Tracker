import random

from django.core.management import BaseCommand

from tracker.models import Transaction,User,Category
from faker import Faker


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        # Create Categories
        categories = ['Bills','Food','Clothes','Medical','Housing','Salary','Social','Transportation','Lifestyle']

        for category in categories:
            Category.objects.get_or_create(name=category)

        user = User.objects.filter(username='peacewalker').first()
        if not user:
            user = User.objects.create_superuser(username='peacewalker', password='test')

        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_CHOICES]
        for i in range(1,20):
            Transaction.objects.create(
                category=random.choice(categories),
                user=user,
                amount=random.uniform(1,2500),
                date=fake.date_between(start_date='-1y', end_date='now'),
                type=random.choice(types)
            )
