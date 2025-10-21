from django.core.management.base import BaseCommand
from algorithms.models import TradingAlgorithm


class Command(BaseCommand):
    help = 'Creates sample trading algorithms'

    def handle(self, *args, **options):
        # Default algorithm (same as original)
        algo1, created = TradingAlgorithm.objects.get_or_create(
            name='Default Strategy',
            defaults={
                'description': 'The original Rayquasa algorithm: buys when stock drops ≥5% and sells when it rises ≥10%',
                'buy_threshold': -0.05,
                'sell_threshold': 0.10,
                'buy_amount': 5.0,
                'sell_amount': 10.0,
                'min_volatility': 0.01,
                'max_volatility': 0.5,
                'min_data_points': 30
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created algorithm: {algo1.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Algorithm already exists: {algo1.name}'))

        # Aggressive algorithm
        algo2, created = TradingAlgorithm.objects.get_or_create(
            name='Aggressive Trader',
            defaults={
                'description': 'More aggressive strategy with lower thresholds: buys on 3% drop, sells on 7% rise',
                'buy_threshold': -0.03,
                'sell_threshold': 0.07,
                'buy_amount': 10.0,
                'sell_amount': 15.0,
                'min_volatility': 0.01,
                'max_volatility': 0.5,
                'min_data_points': 30
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created algorithm: {algo2.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Algorithm already exists: {algo2.name}'))

        # Conservative algorithm
        algo3, created = TradingAlgorithm.objects.get_or_create(
            name='Conservative Strategy',
            defaults={
                'description': 'Conservative approach: waits for larger movements (7% drop, 15% rise)',
                'buy_threshold': -0.07,
                'sell_threshold': 0.15,
                'buy_amount': 3.0,
                'sell_amount': 8.0,
                'min_volatility': 0.01,
                'max_volatility': 0.3,
                'min_data_points': 30
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created algorithm: {algo3.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Algorithm already exists: {algo3.name}'))

        self.stdout.write(self.style.SUCCESS('\nSample algorithms created successfully!'))
