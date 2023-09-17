# Leah Elkins
# Student ID: 008983922
# C950 Data Structures and Algorithms II
import datetime
import csv
from builtins import ValueError
from hash_table import HashTable
from package import Package

# Reads the address information from address_data.csv.
with open("address_data.csv") as csvfile_address:
    address_csv = csv.reader(csvfile_address, delimiter=',')
    address_csv = list(address_csv)


# Reads the distance information from distance_data.csv.
with open("distance_data.csv") as csvfile_distance:
    distance_csv = csv.reader(csvfile_distance, delimiter=',')
    distance_csv = list(distance_csv)


# Reads the package information from package_data.csv.
with open("package_data.csv") as csvfile_package:
    package_csv = csv.reader(csvfile_package, delimiter=',')
    package_csv = list(package_csv)


# Creates package objects from the package_data CSV file and loads them into the hash table. O(n)
def load_package_data(file_name):
    with open(file_name) as package_info:
        package_data = csv.reader(package_info, delimiter=',')

        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zipcode = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_status = "At Hub"

            # Package object
            package = Package(p_id, p_address, p_city, p_state, p_zipcode,
                              p_deadline, p_weight, p_status)

            # Inserts data into the hash table
            package_hash_table.insert(p_id, package)

# Method created to find the distance between two addresses. O(1)
def address_distance(x_value, y_value):
    distance = distance_csv[x_value][y_value]
    if distance == '':
        distance = distance_csv[y_value][x_value]

    return float(distance)

# Method to get the address number from string literal of address. O(n)
def get_address(address):
    for row in address_csv:
        if address in row[2]:
            return int(row[0])

# Manually loads each truck according to the deadlines and special notes.
# Truck mileage for each truck is 0.0 at start of day before leaving hub.
# Create truck object truck1
# IDs of packages that can leave early (8:00)
truck1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck1_mileage = 0.0
truck1_departure_time = datetime.timedelta(hours=8)

# Create truck object truck2
# IDs of packages that are delayed or required to leave on the second truck (9:10)
truck2_packages = [3, 6, 18, 25, 28, 32, 33, 35, 36, 38, 39]
truck2_mileage = 0.0
truck2_departure_time = datetime.timedelta(hours=9, minutes=10)

# Create truck object truck3
# IDs of packages that have the wrong address or are EOD deliveries (10:25)
truck3_packages = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27]
truck3_mileage = 0.0
truck3_departure_time = datetime.timedelta(hours=10, minutes=25)

# Create hash table
package_hash_table = HashTable()

# Load packages into hash table
load_package_data("package_data.csv")

# Method for ordering packages on a given truck using the nearest neighbor algorithm. O(n^3)
# Determines the delivery order by which package is closest to the current address.
# Algorithm runs until all packages are delivered.
def deliver_packages(truck, mileage, depart):
    # Initializes data -- truck's current address, mileage driven, and delivery time
    current_address = '4001 South 700 East'
    mileage_driven = mileage
    delivery_time = depart
    # Initializes the package departure_time from the hub with depart time of the truck.
    for packageID in truck:
        package = package_hash_table.search(packageID)
        package.departure_time = depart
    # Determines the order of delivery
    while len(truck) > 0:
        start_package = package_hash_table.search(truck[0])
        # Finds the address distance and gets the current address and the address the package needs delivered to.
        nearest_distance = float(address_distance(get_address(current_address), get_address(start_package.address)))
        nearest_packageID = truck[0]

        for package in truck:
            next_package = package_hash_table.search(package)
            # Finds the address distance and gets the current address and the address the next package needs delivered to.
            distance = float(address_distance(get_address(current_address), get_address(next_package.address)))
            # Nearest distance is determined
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_packageID = package
        # Searches the nearest package from the hash table
        nearest_package = package_hash_table.search(nearest_packageID)
        # Current address is updated to the nearest package address
        current_address = nearest_package.address
        # Updates the mileage driven
        mileage_driven += nearest_distance
        # Updates the time
        delivery_time += datetime.timedelta(hours=nearest_distance / 18)
        # Delivery time is kept track of as truck delivers packages to each address
        nearest_package.delivery_time = delivery_time
        # Removes the packages from the truck.
        truck.remove(nearest_packageID)

    return mileage_driven
# Gets the total mileage from each of the 3 trucks and adds them together to get the total_truck_mileage.
truck1_total = deliver_packages(truck1_packages, truck1_mileage, truck1_departure_time)
truck2_total = deliver_packages(truck2_packages, truck2_mileage, truck2_departure_time)
truck3_total = deliver_packages(truck3_packages, truck3_mileage, truck3_departure_time)
total_truck_mileage = truck1_total + truck2_total + truck3_total

# User interface displayed when running the program.
class Main:
    # Prompt displayed when user runs the program.
    # Welcomes the user and total mileage for the day's deliveries is displayed.
    # User is asked to select an option from the menu displayed below.
    print("\nWelcome to the WGUPS Package Tracking System!\n"
          f"The total mileage for today's deliveries is: {total_truck_mileage} miles\n"
          f"Please enter an option from below.\n")

    exit_program = True
    # Menu displayed to allow the user to select an option to view the status of packages.
    while exit_program:
        print('*' * 65)
        print('1. View the status of all packages at a specific time')
        print('2. View the status of an individual package at a specific time')
        print('3. Exit the program')
        print('*' * 65)

        # Takes in the user input. Error message is displayed if user does not select an available option.
        user_input = input('\nPlease enter a numeric option from above: ')

        # If the user enters the number '1', user is asked to enter a specific time to view status of all packages.
        if user_input == '1':
            try:
                input_time = input('\nEnter a time to check the status of all packages. (24 hour format: HH:MM:SS): ')
                print('')
                (h, m, s) = input_time.split(':')
                # User inputs a specific time
                user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                for packageID in range(1, 41):
                    # Package ID, address, city, state, zipcode, weight, deadline, delivery time, and departure time are searched in the hash table.
                    package_id = package_hash_table.search(packageID).id
                    package_address = package_hash_table.search(packageID).address
                    package_city = package_hash_table.search(packageID).city
                    package_state = package_hash_table.search(packageID).state
                    package_zipcode = package_hash_table.search(packageID).zipcode
                    package_weight = package_hash_table.search(packageID).weight
                    package_deadline_time = package_hash_table.search(packageID).deadline
                    package_delivery_time = package_hash_table.search(packageID).delivery_time
                    package_departure_time = package_hash_table.search(packageID).departure_time
                    # If departure time is less than user time, and user time is less than package delivery time -- package is EN ROUTE
                    if package_departure_time < user_time < package_delivery_time:
                        print(f'Package ID #{package_id} -- {package_address}, {package_city}, {package_state}'
                              f' {package_zipcode}, {package_weight} KILO, DEADLINE {package_deadline_time}, -- EN ROUTE.')
                    # If user time is less than departure time -- package is AT HUB
                    elif user_time < package_departure_time:
                        print(f'Package ID #{package_id} -- {package_address}, {package_city}, {package_state}'
                              f' {package_zipcode}, {package_weight} KILO, DEADLINE {package_deadline_time}, -- AT HUB.')
                    # If neither is true -- package is DELIVERED and the time delivered is displayed
                    else:
                        print(f'Package ID #{package_id} -- {package_address}, {package_city}, {package_state}'
                              f' {package_zipcode}, {package_weight} KILO, DEADLINE {package_deadline_time}, -- DELIVERED at {package_delivery_time}.')
                print('')
            except ValueError:
                print('INVALID ENTRY. Please enter a valid option.\n')

        # If the user enters the number '2', user is asked to enter a specific time to view status of an individual packages.
        elif user_input == '2':
            try:
                input_time = input('\nEnter a time to check the status of an individual package. (24 hour format: HH:MM:SS): ')
                (h, m, s) = input_time.split(':')
                # User inputs a specific time
                user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                # User is asked to enter the package ID number to view status of an individual package.
                get_package_id = int(input('\nEnter the package ID to view the status of the package: '))
                if 41 > get_package_id > 0:
                    # Package ID, address, city, state, zipcode, weight, deadline, delivery time, and departure time are searched in the hash table.
                    package_id = package_hash_table.search(get_package_id).id
                    package_address = package_hash_table.search(get_package_id).address
                    package_city = package_hash_table.search(get_package_id).city
                    package_state = package_hash_table.search(get_package_id).state
                    package_zipcode = package_hash_table.search(get_package_id).zipcode
                    package_weight = package_hash_table.search(get_package_id).weight
                    package_deadline_time = package_hash_table.search(get_package_id).deadline
                    package_delivery_time = package_hash_table.search(get_package_id).delivery_time
                    package_departure_time = package_hash_table.search(get_package_id).departure_time
                    # If departure time is less than user time, and user time is less than package delivery time -- package is EN ROUTE
                    if package_departure_time < user_time < package_delivery_time:
                        print(f'\nPackage ID #{package_id} -- {package_address}, {package_city}, {package_state}'
                              f' {package_zipcode}, {package_weight} KILO, DEADLINE {package_deadline_time}, -- EN ROUTE.\n')
                    # If user time is less than departure time -- package is AT HUB
                    elif user_time < package_departure_time:
                        print(f'\nPackage ID #{package_id} -- {package_address}, {package_city}, {package_state}'
                              f' {package_zipcode}, {package_weight} KILO, DEADLINE {package_deadline_time}, -- AT HUB.\n')
                    # If neither is true -- package is DELIVERED and the time delivered is displayed
                    else:
                        print(f'\nPackage ID #{package_id} -- {package_address}, {package_city}, {package_state}'
                              f' {package_zipcode}, {package_weight} KILO, DEADLINE {package_deadline_time}, -- DELIVERED at {package_delivery_time}.\n')
                else:
                    print('\nENTRY INVALID. Please enter a valid option.\n')
                    continue
            except ValueError:
                print('\nENTRY INVALID. Please enter a valid option.\n')

        # If the user enters the number '3', exits the program.
        elif user_input == '3':
            exit_program = False
            print('\nThank you for choosing WGUPS Package Tracking System. Goodbye!')
            exit()
        else:
            print('\nENTRY INVALID. Please enter a valid option.\n')