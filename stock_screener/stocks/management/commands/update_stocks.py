from django.core.management.base import BaseCommand
from stocks.views import get_realtime_stock_data


class Command(BaseCommand):
    help = 'Update stock data from Yahoo Finance (Real-time)'

    def handle(self, *args, **options):
        self.stdout.write('Fetching real-time stock data...')
        
        try:
            stocks_data = get_realtime_stock_data()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully fetched real-time data for {len(stocks_data)} stocks!')
            )
            
            for stock in stocks_data:
                self.stdout.write(
                    f"  📈 {stock['ticker']}: ${stock['current_price']} "
                    f"({stock['price_change_percent']:+.2f}%) - {stock['last_fetched']}"
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fetching real-time data: {e}')
            )