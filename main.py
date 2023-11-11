#
# Shehriar Burney
# Pat Troy - CS341
# Project 1: Analyzing CTA2 L data in Python
#
# This program will output data about the CTA using the CTA2_L_daily_ridership database depending on user input. There are 9 commands, each will output different data about the CTA, ie. total ridership, ridership per month, etc...


import sqlite3
import matplotlib.pyplot as plt

##################################################################  
#
# Command One
#
# Output all stations that correspond with the input string
#
def commandOne(dbConn):
  print()
  dbCursor = dbConn.cursor()
  userInput = input("Enter partial station name (wildcards _ and %): ");
  sql = "SELECT Station_id, Station_name FROM Stations WHERE Station_name LIKE '"+userInput+"' group by station_name order by station_name;"

  dbCursor.execute(sql)
  
  rows = dbCursor.fetchall();

  running = True
  
  if len(rows) == 0:
    print("**No stations found...", end = "\n")
    running = False
    
  if running:
    for x in rows:
      id = x[0]
      name = x[1]
      print(id, ":", name)


  dbCursor.close()

##################################################################  
#
# Command Two
#
# Output all stations and their total number of riders
#
def commandTwo(dbConn):
  print("** ridership all stations **", end = "\n")
  
  dbCursor = dbConn.cursor()
  sql = "SELECT station_name, sum(ridership.num_riders), (SELECT sum(num_riders) from ridership) from stations join ridership where stations.station_id = ridership.station_id group by station_name order by station_name asc;"

  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  running = True
  
  if len(rows) == 0:
    print("**No stations found...", end = "\n")
    running = False

  if running:
    for x in rows:
      name = x[0]
      num_riders = x[1]
      percentage = num_riders*100 / x[2]
      print(name, ":", f"{num_riders:,}", f"({percentage:.2f}%)")
    
  dbCursor.close()

##################################################################  
#
# Command Three
#
# Output the top 10 busiest stations by total number of riders
#
def commandThree(dbConn):
  print("** top-10 stations **", end = "\n")
  dbCursor = dbConn.cursor()
  sql = "SELECT station_name, sum(ridership.num_riders) as totRiders, (SELECT sum(num_riders) from ridership) from stations join ridership where stations.station_id = ridership.station_id group by station_name order by totRiders desc limit 10;"

  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  for x in rows:
    name = x[0]
    num_riders = x[1]
    percentage = num_riders*100 / x[2]
    print(name, ":", f"{num_riders:,}", f"({percentage:.2f}%)")
  
  dbCursor.close()

##################################################################  
#
# Command Four
#
# Output the top 10 least busiest stations by total number of riders
#
def commandFour(dbConn):
  print("** least-10 stations **", end = "\n")
  dbCursor = dbConn.cursor()
  sql = "SELECT station_name, sum(ridership.num_riders) as totRiders, (SELECT sum(num_riders) from ridership) from stations join ridership where stations.station_id = ridership.station_id group by station_name order by totRiders asc limit 10;"

  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  for x in rows:
    name = x[0]
    num_riders = x[1]
    percentage = num_riders*100 / x[2]
    print(name, ":", f"{num_riders:,}", f"({percentage:.2f}%)")
  
  dbCursor.close()

##################################################################  
#
# Command Five
#
# Output the top 10 least busiest stations by total number of riders
#
def commandFive(dbConn):
  print()
  dbCursor = dbConn.cursor()
  userInput = input("Enter a line color (e.g. Red or Yellow): ").lower().capitalize()
  if userInput == 'Purple-express':
    userInput = "Purple-Express"
  sql = "SELECT stop_name, direction, ada from Stops join stopDetails join Lines where stops.stop_id = stopDetails.stop_id AND stopDetails.line_id = lines.line_id AND lines.color = '"+userInput+"' group by stop_name order by stop_name;"
  
  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  if len(rows) == 0:
    print("**No such line...", end = "\n")
    return
  
  for x in rows:
    stop_name = x[0]
    direction = x[1]
    if x[2] == 1:
      accessibleBool = "yes"
    else:
      accessibleBool = "no"

    print(stop_name, ": direction =", direction, "(accessible? " + accessibleBool+")")
    
  dbCursor.close()

##################################################################  
#
# Command Six
#
# Output number of riders by month and plotting it's graph
#
def commandSix(dbConn):
  print("** ridership by month **")
  dbCursor = dbConn.cursor()
  sql = "SELECT strftime('%m', ride_date) as months, sum(num_riders) from ridership group by months order by months;"
  
  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  ridersList = []
  monthList = []
  for x in rows:
    month = x[0]
    num_riders = x[1]
    
    print(month, ":", f"{num_riders:,}")
    ridersList.append(num_riders)
    monthList.append(month)

  print()
  userPlot = input("Plot? (y/n) ")
  if userPlot == "y":
    plt.xlabel("Month")
    plt.ylabel("Number of riders (x * 10^8)")
  
    plt.title("monthly ridership")
  
    plt.plot(monthList, ridersList)
  
    plt.show()
  
  dbCursor.close()


##################################################################  
#
# Command Seven
#
# Output number of riders by month and plotting it's graph
#
def commandSeven(dbConn):
  print("** ridership by year **")
  dbCursor = dbConn.cursor()
  sql = "SELECT strftime('%Y', ride_date) as yr, sum(num_riders) from ridership group by yr order by yr;"
  
  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  ridersList = []
  yearList = []
  for x in rows:
    year = x[0]
    num_riders = x[1]
    
    print(year, ":", f"{num_riders:,}")
    ridersList.append(num_riders)
    yearList.append(str(int(year)-2000))

  for i in range(len(yearList)):
    if len(yearList[i]) == 1:
      yearList[i] = "0"+yearList[i]
  
  print()
  userPlot = input("Plot? (y/n) ")
  if userPlot == "y":
    plt.xlabel("Year")
    plt.ylabel("Number of riders (x * 10^8)")
  
    plt.title("yearly ridership")
  
    plt.plot(yearList, ridersList)
  
    plt.show()
  
  dbCursor.close()


##################################################################  
#
# Command Eight
#
# Output number of riders per day for 2 stations and comparing them. This can also plot the graphs of the 2 stations against each other
#
def commandEight(dbConn):
  print()
  dbCursor = dbConn.cursor()

  userYear = input("Year to compare against? ") #Input year
  print()
  userStation1 = input("Enter station 1 (wildcards _ and %): ") #Input station 1
  running = True # keeps track of if the code should continue running based on userInput

  #Query to find all stations that have name like user Input. This checks for if there are multiple/no stations
  sql = "SELECT station_name, station_id from stations where station_name like '"+userStation1+"';"
  dbCursor.execute(sql) #Execute sql query
  rows = dbCursor.fetchall() # Fetch all rows of output from SQL query

  if len(rows) == 0:
    print("**No station found...", end = "\n")
    running = False #If no stations are found, end program
  if len(rows) > 1:
    print("**Multiple stations found...")
    running = False #If multiple stations are found, end program

  dbCursor.close()

  if running:
    dbCursor = dbConn.cursor()
    print()
    userStation2 = input("Enter station 2 (wildcards _ and %): ") # Input the station 2
    
    #Query to find all stations that have name like user Input. This checks for if there are multiple/no stations
    sql = "SELECT station_name, station_id from stations where station_name like '"+userStation2+"';"
    dbCursor.execute(sql) #Execute sql query
    rows = dbCursor.fetchall() # Fetch all rows of output from SQL query

    #Checking if station 2 is a good input
    if len(rows) == 0:
      print("**No station found...", end = "\n")
      running = False
    if len(rows) > 1:
      print("**Multiple stations found...")
      running = False

    dbCursor.close()
      
    if running:
      dbCursor = dbConn.cursor()
      sql = "SELECT stations.station_name, stations.station_id, strftime('%Y-%m-%d', ridership.ride_date) as dates, strftime('%Y', ridership.ride_date) as yr, ridership.num_riders from Stations join ridership where stations.station_id = ridership.station_id and station_name like '"+userStation1+"' and yr = '"+userYear+"' order by dates;"
      
      dbCursor.execute(sql) #Execute sql query
      rows = dbCursor.fetchall() # Fetch all rows of output from SQL query
    
      Dates = []
      station1_riders = []
      
      for x in rows:
        station1_name = x[0] #Store station 1 name
        station1_ID = x[1] #Store station 1 ID
      
        Dates.append(x[2]) # Add all dates from station 1
        station1_riders.append(x[4]) # Add all ridership of station 1
    
        
      dbCursor.close()
    
      
      dbCursor = dbConn.cursor()
      sql = "SELECT stations.station_name, stations.station_id, strftime('%Y-%m-%d', ridership.ride_date) as dates, strftime('%Y', ridership.ride_date) as yr, ridership.num_riders from Stations join ridership where stations.station_id = ridership.station_id and station_name like '"+userStation2+"' and yr = '"+userYear+"' order by dates;" #Query for station 2
    
      dbCursor.execute(sql)
    
      station2_riders = []
    
      rows = dbCursor.fetchall()
      for x in rows:
        station2_name = x[0] #Store name and ID of station
        station2_ID = x[1]
        
        station2_riders.append(x[4]) # Append the number of riders to list
    
    
      #Printing values
      print("Station 1:", station1_ID, station1_name, end = "\n")
      #Print first 5 values of station 1
      for i in range (0, 5):
        print(Dates[i], station1_riders[i], end = "\n")
    
      #Print last 5 values of station 1
      dateSize = len(Dates)
      for i in range(dateSize - 5, dateSize):
        print(Dates[i], station1_riders[i], end = "\n")
    
      
      print("Station 2:",station2_ID, station2_name, end = "\n")
      #Print first 5 values of station 2
      for i in range (0, 5):
        print(Dates[i], station2_riders[i], end = "\n")
    
      #Print last 5 values of station 2
      for i in range(dateSize - 5, dateSize):
        print(Dates[i], station2_riders[i], end = "\n")
    
      dbCursor.close()
    
      #Plotting values
      print()
      userPlot = input("Plot? (y/n) ")
      if userPlot == "y":
        plt.xlabel("Day")
        plt.ylabel("Number of riders")
      
        plt.title("Riders each day of "+userYear)
       
    
        #day = list(range(1, 366))
        plt.plot(list(range(0, len(Dates))), station1_riders, label = station1_name)
        plt.plot(list(range(0, len(Dates))), station2_riders, label = station2_name)
        plt.legend(loc = "upper right")
      
        plt.show()  
  

##################################################################  
#
# Command Nine
#
# Output number of riders by month and plotting it's graph
#
def commandNine(dbConn):
  print()
  dbCursor = dbConn.cursor()

  userColor = input("Enter a line color (e.g. Red or Yellow): ").lower().capitalize()

  if userColor == "Purple-express":
    userColor = "Purple-Express"
  #Query to find all stations that have name like user Input. This checks for if there are multiple/no stations
  sql = "SELECT distinct station_name, b.latitude, b.longitude FROM Stations as a JOIN Stops as b JOIN StopDetails as c JOIN Lines as d WHERE a.station_id = b.station_id AND b.stop_id = c.stop_id AND c.line_id = d.line_id AND d.color = '"+userColor+"' GROUP BY a.station_name ORDER BY a.station_name asc;"

  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  running = True
  if len(rows) == 0:
    print("**No such line...")
    running = False

  if running:
    station_names = []
    latitudeList = []
    longitudeList = []
    
    for x in rows:
      station_names.append(x[0])
      latitudeList.append(float(x[1]))
      longitudeList.append(float(x[2]))
  
      print(x[0], ": (" + str(x[1])+", " +str(x[2])+")")
    
    print()
    userPlot = input("Plot? (y/n)")
    if userPlot:
      image = plt.imread("chicago.png")
      xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
      plt.imshow(image, extent = xydims)
  
      plt.title(userColor + " line")
  
      if userColor.lower() == "purple-express":
        userColor = "Purple"
  
      plt.plot(longitudeList, latitudeList, "o", c = userColor)
      
      for i in range(len(station_names)):
        plt.annotate(station_names[i], (longitudeList[i], latitudeList[i]))
  
      plt.xlim([-87.9277, -87.5569])
      plt.ylim([41.7012, 42.0868])
  
      plt.show()
  dbCursor.close()
        
##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) from Stops")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) from Ridership")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute("Select min(date(ride_date)) as startDate, max(date(ride_date)) as endDate from ridership")
    row = dbCursor.fetchone();
    print("  date range:", row[0], '-', row[1])

    dbCursor.execute("Select sum(num_riders) from ridership")
    row = dbCursor.fetchone();
    total_numRiders = row[0] #Required for percentages
    print("  Total ridership:", f"{total_numRiders:,}")

    dbCursor.execute("Select sum(num_riders) from ridership where type_of_day = 'W'")
    row = dbCursor.fetchone();
    print("  Weekday ridership:", f"{row[0]:,}", f"({row[0]*100/total_numRiders:.2f}%)")
  
    dbCursor.execute("Select sum(num_riders) from ridership where type_of_day = 'A'")
    row = dbCursor.fetchone();
    print("  Saturday ridership:", f"{row[0]:,}", f"({row[0]*100/total_numRiders:.2f}%)")
  
    dbCursor.execute("Select sum(num_riders) from ridership where type_of_day = 'U'")
    row = dbCursor.fetchone();
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({row[0]*100/total_numRiders:.2f}%)")
    dbCursor.close()
    print()

##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

command = input("Please enter a command (1-9, x to exit): ")

while command != 'x':
  if command == '1':
    commandOne(dbConn)
  elif command == '2':
    commandTwo(dbConn)
  elif command == '3':
    commandThree(dbConn)
  elif command == '4':
    commandFour(dbConn)
  elif command == '5':
    commandFive(dbConn)
  elif command == '6':
    commandSix(dbConn)
  elif command == '7':
    commandSeven(dbConn)
  elif command == '8':
    commandEight(dbConn)
  elif command == '9':
    commandNine(dbConn)
  elif command == 'x':
    break
  else:
    print("**Error, unknown command, try again...")
  print()
  command = input("Please enter a command (1-9, x to exit): ")
  
dbConn.close()
#
# done
#
