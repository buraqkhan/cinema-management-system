

from abc import ABC, abstractmethod

# Class for a particular movie with its description
class Movie:
    def __init__(self, name):
        self.name = name;
        #self.desc;
        #self.director;
        #self.runtime;

# Class for a specific seat
class Seat:
    def __init__(self, num, row, col):    
        self.seat_no = num;
        self.row = row;
        self.col = col;
     
# Class for Halls
class Hall:
    def __init__(self, hallnum, seats):
        self.hall_no = hallnum;
        self.seats = seats; # list of object seats
        self.capacity = len(seats)

    
# An instance of a show
class Show:
    def __init__(self, ts, movie, hall): 
        self.time_slot = ts;
        self.movie = movie; # object of class Movie
        self.hall = hall; # object of hall


# Showtimes / Movie catalogue
class Showtimes:
    def __init__(self, shows):
        self.shows = shows;

    def display(self):
        for i in range(len(self.shows)):
            print("Show: "+ self.shows[i].movie.name+", Time: "+ self.shows[i].time_slot)
            

# Individual account
class Account:
    def __init__(self,name,email,psw):
        self.name = name
        self.email = email
        self.psw = psw
        
    def DisplayAccount(self):
        print(self.name + " " + self.email+ " "+ self.psw)


# Contains all the user's accounts
class Users:
    def __init__(self, pers_handler):
        self.accounts = []       
        self.pers_handler = pers_handler
        
    def CreateAccount(self,name,email,psw):
        acc = Account(name,email,psw)
        self.accounts.append(acc)
        self.save(acc)
        
    def DisplayAccounts(self):
        for i in range(len(self.accounts)):
            print(self.accounts[i].DisplayAccount())
        
    def save(self, account): # call this function in createaccount once the account object is created
        self.pers_handler.saveAccount(account)    
    
    


# Cinema class [Controller]
class Cinema:
    def __init__(self, handler):
        self.show_times = None # This will either be a list or an object of showtime
        self.hall_1 = None
        self.hall_2 = None
        self.hall_3 = None
        self.pers_handler = handler
        self.users = Users(self.pers_handler)
        
    def browseMovies(self, showtime):
        self.show_times = showtime
    
    def createAccount(self, name, email, psw):
       self.users.CreateAccount(name, email, psw)


# Abstract Class for DBHandler
class PersistentHandler(ABC):
    @abstractmethod
    def saveAccount(self):pass

# Oracle DB Class
class OracleHandler(PersistentHandler):
    def saveAccount(self, account):
         #implementation of Oracle db here
         print(account.name + " saved to oracle database")

# File handling class
class FileHandler(PersistentHandler):
    def saveAccount(self, account):
        #implementation of saving to a file here
        print(account.name + " saved to file")
        
        
###############################################
# main functionality 

save = input("Enter DB name!!\n")
if(save == "oracle"):
    pers_handler = OracleHandler()
elif(save == "file"):
    pers_handler = FileHandler()


seat1 = Seat(1, 1, 1)
seat2 = Seat(2, 1, 2)

seats = []
seats.append(seat1)
seats.append(seat2)

h1 = Hall(1, seats)

a = Movie("a")
b = Movie("b")
c = Movie("c")

s1 = Show("7:30-8:30", a, h1)
s2 = Show("1:30-3:00", b, h1)
s3 = Show("12:00-1:30", c, h1)

shows = []
shows.append(s1)
shows.append(s2)
shows.append(s3)

st = Showtimes(shows)


print("Shows Available")
Cin = Cinema(pers_handler)
Cin.browseMovies(st)
Cin.show_times.display()
Cin.createAccount("Omer","foo@foolish.com","bye")
Cin.createAccount("Hayat","foo@foolish.com","foo")
Cin.createAccount("buraq","foo@foolish.com","foo")

            

