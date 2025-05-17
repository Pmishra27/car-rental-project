import datetime

class CarRental:
    def __init__(self, stock):
        self.stock = stock  # Total cars available
        self.rates = {
            'hourly': 10,  # Rs. 10 per hour per car
            'daily': 50,   # Rs. 50 per day per car
            'weekly': 300  # Rs. 300 per week per car
        }

    def display_available_cars(self):
        """Display current inventory."""
        print(f"Available cars: {self.stock}")
        return self.stock

    def _rent_cars(self, mode, n_cars):
        """Helper method to validate and process rentals."""
        if n_cars <= 0:
            print("Number of cars must be positive.")
            return None
        if n_cars > self.stock:
            print(f"Only {self.stock} cars available.")
            return None
        self.stock -= n_cars
        return datetime.datetime.now()

    def rent_hourly(self, n_cars):
        return self._rent_cars('hourly', n_cars)

    def rent_daily(self, n_cars):
        return self._rent_cars('daily', n_cars)

    def rent_weekly(self, n_cars):
        return self._rent_cars('weekly', n_cars)

    def return_car(self, request):
        """Calculate bill and restock cars."""
        rental_time, mode, n_cars = request
        if not all([rental_time, mode, n_cars]):
            print("Invalid return request.")
            return 0

        # Calculate rental duration
        duration = datetime.datetime.now() - rental_time
        hours = duration.total_seconds() / 3600  # Total hours
        days = hours / 24  # Total days
        weeks = days / 7   # Total weeks

        # Calculate bill based on mode
        rate = self.rates[mode]
        if mode == 'hourly':
            bill = rate * hours * n_cars
        elif mode == 'daily':
            bill = rate * days * n_cars
        elif mode == 'weekly':
            bill = rate * weeks * n_cars

        # Restock cars
        self.stock += n_cars
        return round(bill, 2)

class Customer:
    def __init__(self, rental_shop):
        self.rental_shop = rental_shop
        self.rental_info = None  # (mode, n_cars, start_time)

    def request_car(self, mode, n_cars):
        """Request cars from the rental shop."""
        if mode not in self.rental_shop.rates:
            print("Invalid rental mode.")
            return False

        # Rent cars based on mode
        if mode == 'hourly':
            start_time = self.rental_shop.rent_hourly(n_cars)
        elif mode == 'daily':
            start_time = self.rental_shop.rent_daily(n_cars)
        elif mode == 'weekly':
            start_time = self.rental_shop.rent_weekly(n_cars)

        if start_time:
            self.rental_info = (mode, n_cars, start_time)
            return True
        return False

    def return_car(self):
        """Return cars and generate bill."""
        if not self.rental_info:
            print("No cars to return.")
            return 0
        mode, n_cars, start_time = self.rental_info
        bill = self.rental_shop.return_car((start_time, mode, n_cars))
        self.rental_info = None
        return bill