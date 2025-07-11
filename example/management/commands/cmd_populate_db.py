import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
# Make sure to change 'example' to your app's name!
from example.models import Category, Product


class Command(BaseCommand):
    help = 'Populates the database with test categories and products to simulate load.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_categories',
            type=int,
            default=5,
            help='Number of categories to create.'
        )
        parser.add_argument(
            '--products_per_category',
            type=int,
            default=5000,  # A high number to generate many products
            help='Number of products to create per category.'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Deletes all existing data before populating.'
        )

    def handle(self, *args, **options):
        num_categories = options['num_categories']
        products_per_category = options['products_per_category']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write(self.style.WARNING(
                'Deleting all existing products and categories...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data deleted.'))

        self.stdout.write(self.style.SUCCESS(
            f'Starting data population process: {num_categories} categories, '
            f'{products_per_category} products per category.'
        ))

        categories = []
        for i in range(num_categories):
            category_name = f'Category_{i+1}'
            if i == 0:  # Ensure "Electronics" exists and is the first
                category_name = 'Electronics'
            elif i == 1:  # Another common category for testing
                category_name = 'Books'

            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'Description for {category_name}'}
            )
            categories.append(category)
            self.stdout.write(f'  Created/Retrieved category: {category.name}')

        products_to_create = []
        with transaction.atomic():  # Use an atomic transaction for better performance
            for category in categories:
                self.stdout.write(
                    f'  Creating products for category: {category.name}...')
                for i in range(products_per_category):
                    product_name = f'{category.name}_Product_{i+1}'
                    # To ensure variety and meaningful filters
                    price = Decimal(random.uniform(
                        10.00, 1000.00)).quantize(Decimal('0.01'))
                    stock = random.randint(0, 500)
                    is_active = random.choice([True, False])

                    products_to_create.append(
                        Product(
                            name=product_name,
                            category=category,
                            price=price,
                            stock=stock,
                            is_active=is_active
                        )
                    )
                # Bulk create every 1000 products for efficiency
                if len(products_to_create) >= 1000:
                    Product.objects.bulk_create(products_to_create)
                    products_to_create = []  # Clear the list

            # Create any remaining products
            if products_to_create:
                Product.objects.bulk_create(products_to_create)

        self.stdout.write(self.style.SUCCESS(
            'Database successfully populated!'))
        total_products = Product.objects.count()
        self.stdout.write(self.style.HTTP_INFO(
            f'Total products created: {total_products}'))
