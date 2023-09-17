# Creates class for packages
class Package:
    # Initialize package object. O(1)
    def __init__(self, id, address, city, state, zipcode, deadline, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # Prints package object information. O(1)
    def __str__(self):
        return f'{self.id}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.deadline}, {self.delivery_time}'