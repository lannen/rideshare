from helper import helper
# from db_operations import db_operations
import random

# import MySQL
import mysql.connector

# make connection
conn = mysql.connector.connect(host = "localhost", 
                               user = "root",
                               password = "cpsc408!",
                               auth_plugin = 'mysql_native_password',
                               database = "Rideshare")

# create cursor object
cur_obj = conn.cursor()

# create database schema
# print("Creating database schema...")
# cur_obj.execute("CREATE SCHEMA RideShare;")

# # create user table               
# cur_obj.execute('''
#     CREATE TABLE user(
#         userID INT NOT NULL PRIMARY KEY,
#         userType VARCHAR(40) NOT NULL
#     );
# ''')
                
# insert user data
# insertQuery = '''
# INSERT INTO user
# VALUES (%s, %s);
# '''
# values = [(2,"Rider")]  
# cur_obj.executemany(insertQuery, values)
# conn.commit()

# create rider table               
# cur_obj.execute('''
#     CREATE TABLE rider(
#         riderID INT NOT NULL PRIMARY KEY
#     );
# ''')

# # insert rider data
# insertQuery = '''
# INSERT INTO rider
# VALUES (%s);
# '''
# values = [(11,),(22,),(33,)]  
# cur_obj.executemany(insertQuery, values)
# conn.commit()

# create driver table          
# cur_obj.execute('''
#     CREATE TABLE driver(
#         driverID INT NOT NULL PRIMARY KEY,
#         Rating VARCHAR(40) NOT NULL,
#         isActive BOOL NOT NULL
#     );
# ''') 

# # insert driver data
# insertQuery = '''
# INSERT INTO driver
# VALUES (%s, %s, %s);
# '''
# values = [(55,4,1),(66,3,0)]  
# cur_obj.executemany(insertQuery, values)
# conn.commit()

# create ride table
# cur_obj.execute('''
#     CREATE TABLE ride(
#         rideID INT NOT NULL,
#         driverID INT NOT NULL,
#         riderID INT NOT NULL,
#         pick_up VARCHAR(40) NOT NULL,
#         drop_off VARCHAR(40) NOT NULL,
#         PRIMARY KEY (rideID),
#         FOREIGN KEY (riderID) REFERENCES rider (riderID),
#         FOREIGN KEY (driverID) REFERENCES driver (driverID)
#      );
# ''')

# insert ride data
# insertQuery = '''
# INSERT INTO ride
# VALUES (%s, %s, %s, %s, %s);
# '''
# values = [(1234, 5, 11, "chapman grand", "chapman u"),(5678, 6, 22, "subway", "qdoba"), (1432, 55, 3, "home", "party")]  
# cur_obj.executemany(insertQuery, values)
# conn.commit()

# show all databases
# cur_obj.execute("SHOW DATABASES;")
# print("\nList of Databases:")
# for row in cur_obj:
#     helper.prettier_print(row)

# select RideShare database
cur_obj.execute("USE RideShare;")   # should say 'Database Changed' ???
# for row in cur_obj:
#     print(row)

# show all tables in RideShare
# cur_obj.execute("SHOW FULL TABLES;")
# print("\nList of Tables:")
# for row in cur_obj:
#     helper.prettier_print(row)

# print out connection to verify and close
# print("\nConnection made to", conn)

# connect to RideShare database ???
# db_ops = db_operations(conn)
# rider_data = helper.data_cleaner("rider.csv")
# driver_data = helper.data_cleaner("driver.csv")
# ride_data = helper.data_cleaner("ride.csv")

# checks to see if any table is empty
# def is_empty():
#     # check rider table
#     query = '''
#     SELECT COUNT(*)
#     FROM tablename :=tablename
#     '''

#     result = db_ops.single_record(query)
#     return result == 0

# will fill tables if empty
# def pre_process():
#     # rider table is empty
#     if is_empty("drivers"):
#         attribute_count = len(driver_data[0])
#         placeholders = ("?,"*attribute_count)[:-1]
#         query = "INSERT INTO drivers VALUES("+placeholders+")"
#         db_ops.bulk_insert(query, driver_data)

#     if is_empty("riders"):
#         attribute_count = len(riders_data[0])
#         placeholders = ("?,"*attribute_count)[:-1]
#         query = "INSERT INTO riders VALUES("+placeholders+")"
#         db_ops.bulk_insert(query, riders_data)
#     if is_empty("rides"):
#         attribute_count = len(rides_data[0])
#         placeholders = ("?,"*attribute_count)[:-1]
#         query = "INSERT INTO rides VALUES("+placeholders+")"
#         db_ops.bulk_insert(query, rides_data)

# welcome page
def startScreen():
    print('''\nWelcome to RideShare!''')

    while True:
        # ask if new or returning user
        print('''\nAre you a New or Returning User?
        1. New
        2. Returning
        ''')
        num = helper.get_choice([1,2])

        # new user
        if num == 1:
            create_new_user()
            startScreen()

        # returning user
        else:
            # get ID number to see if user is a rider or driver
            userID = input("Provide userID: ")

            # check if userID exists ???
            query = '''
            SELECT COUNT(*) from user
            WHERE userID = %s;
            '''
            cur_obj.execute(query, (userID,))
            result = cur_obj.fetchone()
            user_count = result[0]

            # user doesn't exist
            if user_count == 0:
                print("\nUser ID does not exist. Try Again.")

            else:
                # check user type in user table
                query = '''
                        SELECT userType from user
                        WHERE userID = %s;
                        '''
                cur_obj.execute(query, (userID,))
                result = cur_obj.fetchall()
                userType = result[0][0]

                # user is a rider
                if userType == "Rider":
                    print("\nWelcome back Rider " + userID + "!")
                    rider_options(userID)
                    break

                # user is a driver
                elif userType == "Driver":
                    print("\nWelcome back Driver " + userID + "!")
                    driver_options(userID)
                    break

# create a new user
def create_new_user():
    # driver or rider
    print('''\nCreate a new Rider or Driver account?
    1. Rider
    2. Driver
    ''') 
    num = helper.get_choice([1,2])

    if num == 1:
        create_rider()
    else:
        create_driver()

# create a new rider
def create_rider():
    # Generate a random 3-digit number for the rider ID
    rider_id = str(random.randint(100, 999))

    # Check if the generated rider ID already exists in the database
    cur_obj.execute("SELECT COUNT(*) FROM rider WHERE riderID = %s", (rider_id,))
    result = cur_obj.fetchone()

    # If the rider ID already exists, generate a new one until it is unique
    while result[0] > 0:
        rider_id = str(random.randint(100, 999))
        cur_obj.execute("SELECT COUNT(*) FROM rider WHERE riderID = %s", (rider_id,))
        result = cur_obj.fetchone()

    # Insert the new rider with the generated rider ID into the database
    cur_obj.execute("INSERT INTO rider (riderID) VALUES (%s)", (rider_id,))
    conn.commit()

    cur_obj.execute("INSERT INTO user (userID, userType) VALUES (%s, %s)", (rider_id, "Rider",))
    conn.commit()

    print(f"New rider created with riderID: {rider_id}")

# create a new driver
def create_driver():
     # Generate a random 3-digit number for the driver ID
    driver_id = str(random.randint(100, 999))

    # Check if the generated driver ID already exists in the database
    cur_obj.execute("SELECT COUNT(*) FROM driver WHERE driverID = %s", (driver_id,))
    result = cur_obj.fetchone()

    # If the driver ID already exists, generate a new one until it is unique
    while result[0] > 0:
        driver_id = str(random.randint(100, 999))
        cur_obj.execute("SELECT COUNT(*) FROM driver WHERE driverID = %s", (driver_id,))
        result = cur_obj.fetchone()

    # Insert the new driver with the generated driver ID into the database
    cur_obj.execute("INSERT INTO driver (driverID, Rating, isActive) VALUES (%s,%s,%s)", (driver_id,5,1))
    conn.commit()

    # Insert the new driver with the generated driver ID into the database
    cur_obj.execute("INSERT INTO user (userID, userType) VALUES (%s,%s)", (driver_id,"Driver"))
    conn.commit()

    print(f"New driver created with driverID: {driver_id}")

# rider options ???
def rider_options(userID):
    while True:
        riderID = userID
        # output options to user
        print('''\nSelect from the following rider options:
        1. View Rides
        2. Find a Driver
        3. Rate my Driver
        4. Exit
        ''')

        # get user choice
        choice = helper.get_choice([1,2,3,4])

        # rider choices
        if choice == 1:
            view_rides(riderID)
        if choice == 2:
            find_a_driver(riderID)
        if choice == 3:
            rate_my_driver(riderID)
        if choice == 4:
            print("Goodbye!")
            break


# driver options ???
def driver_options(userID):
    while True:
        driverID = userID

        # output options to user
        print('''\nSelect from the following driver options:
        1. View Rating
        2. View Rides
        3. Activate/Deactive Driver Mode
        4. Exit
        ''')

        # get user choice
        choice = helper.get_choice([1,2,3,4])

        # driver choices
        if choice == 1:
            view_rating(driverID)
        if choice == 2:
            view_Rides(driverID)
        if choice == 3:
            activate_deactivate(driverID)
        if choice == 4:
            print("Goodbye!")
            break

# display a list of all rides
def view_rides(riderID):
    print("\nHere is a list of all past ride information!")

    # select ride from riderID
    query = '''
    SELECT *
    FROM ride
    WHERE riderID = %s
    '''
    cur_obj.execute(query, (riderID,))
    results = cur_obj.fetchall()

    # to print out ride information
    cols = ['rideID','driverID','riderID','pickUp','dropOff']
    for row in results:
        for col in cols:
            value = row[cols.index(col)]
            print("    "+f'{col}: {value}')

# match rider with a driver that has driver mode activated
def find_a_driver(riderID):
    # rider provides pick up and drop off location
    pickUp = input("Enter your pick up location: ")
    dropOff = input("Enter your drop off location: ")

    # provide rider with rideID
    query = '''
    SELECT COUNT(*)
    FROM ride
    '''
    cur_obj.execute(query)
    results =  cur_obj.fetchall()
    ride_count_int = int(results[0][0])
    rideID = ride_count_int + 1
    print("\nYour ride ID is:", rideID)

    # select active driver
    query = '''
        SELECT driverID
        FROM Driver
        WHERE isActive = 1
    '''
    cur_obj.execute(query)
    result = cur_obj.fetchall()
    driverID = result[0][0]
    print("Now connecting to driver:", driverID)

    # add info to ride table
    query = '''
        INSERT INTO Ride
        VALUES (%s, %s, %s, %s, %s)
    '''
    values = [(rideID,driverID,riderID,pickUp,dropOff)]  
    cur_obj.executemany(query, values)
    conn.commit()

    # send rider back to options menu ???

# rider can rate their last driver
def rate_my_driver(riderID):
    # look up rider's last ride
    query = '''
        SELECT MIN(rideID)
        FROM ride
        WHERE riderID = %s
    '''
    cur_obj.execute(query, (riderID,))
    result = cur_obj.fetchall()
    minID = result[0][0]
    print("minID ", minID)

    # get the driver's ID
    query = '''
        SELECT driverID
        FROM ride
        WHERE rideID = %s
    '''
    cur_obj.execute(query, (minID,))
    result = cur_obj.fetchall()
    driverID = result[0][0]
    print("\nYour last ride was with Driver", driverID)
    
    while True:
        query = '''
        SELECT *
        FROM ride
        WHERE rideID = %s
        '''
        cur_obj.execute(query, (minID,))
        results = cur_obj.fetchall()

        # print info to user
        cols = ['rideID','driverID','riderID','pickUp','dropOff']
        for row in results:
            for col in cols:
                value = row[cols.index(col)]
                print("    "+f'{col}: {value}')
        
        # ask if it is the correct ride
        print('''\nIs this the correct ride? 
        1. Yes
        2. No
        ''')
        num = helper.get_choice([1,2])

        if num == 1:
            query = '''
            SELECT Rating
            FROM driver
            WHERE driverID = %s
            '''
            cur_obj.execute(query, (driverID,))
            result = cur_obj.fetchall()
            current = result[0][0]
            current_int = float(current)
            
            # calculate driver's new rating by taking current rating + new rating / 2
            print("\nRate Driver", driverID, "on a scale of 0-5 below. ")
            while True:
                new = input("Enter new rating: ")
                new_int = int(new)
                if new_int < 0 or new_int 6> 5:
                    print("Invalid rating. Please enter a number between 0 and 5.")
                else:
                    break            
            updated = (current_int + new_int)/2

            query = '''
            UPDATE driver
            SET Rating = %s
            WHERE driverID = %s
            '''
            cur_obj.execute(query, (updated, driverID,))
            conn.commit()
            break

         # if not correct ride, user enters rideID of ride they want to rate
        if num == 2:
            minID = input("Enter the rideID you would like to rate: ")

            # confirm rideID information ???


# show the driver their current rating
def view_rating(driverID):
    query = '''
    SELECT Rating
    FROM driver
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (driverID,))
    result = cur_obj.fetchall()
    rating = result[0][0]

    print("\nYour current rating is", rating, "out of 5.")

# display a list of all rides
def view_Rides(driverID):
    print("\nHere is a list of all past ride information!")

    query = '''
    SELECT *
    FROM ride
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (driverID,))
    results = cur_obj.fetchall()

    cols = ['rideID','driverID','riderID','pickUp','dropOff']
    for row in results:
        for col in cols:
            value = row[cols.index(col)]
            print("    "+f'{col}: {value}')

# updates a flag on their record that they are able 
# to drive and are now accepting ride requests
def activate_deactivate(driverID):
    query = '''
    SELECT isActive
    FROM driver
    WHERE driverID = %s
    '''
    cur_obj.execute(query, (driverID,))
    result = cur_obj.fetchall()
    isActive = result[0][0]

    while True:
        if isActive == 1:
            text = "active"
            opposite = 0
            opp_txt = "not active"

        else:
            text = "not active"
            opposite = 1
            opp_txt = "active"

        print("\nDo you want to change your " + text + " driver status to " + opp_txt + "?")
        print('''    1. Yes\n    2. No''')
        update = helper.get_choice([1,2])

        # user wants to change isActive
        if update == 1:
            query = '''
            UPDATE driver
            SET isActive = %s
            WHERE driverID = %s
            '''
            cur_obj.execute(query, (opposite, driverID,))
            conn.commit()

            # output results
            print("\nYour driver status is now " + opp_txt + ".")
            break

        else:
        # driver doesn't want to change isActive
            print("\nYour driver status is still " + text + ".")
            break    

# Main Program
startScreen()
# pre_process()
# print("is empty?", is_empty()) - debug

# close connection
conn.close()
