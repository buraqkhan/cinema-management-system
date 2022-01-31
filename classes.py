from abc import ABC, abstractmethod
import pickle
import os

# Class for a particular movie with its description
class Movie:
    def __init__(self, name):
        self.name = name

    def displayMovie(self):
        print(self.name)

# Class for a specific seat
class Seat:
    def __init__(self, num):    
        self.seat_no = num
    
    def displaySeat(self):
        print(self.seat_no)
     
# Class for Halls
class Hall:
    def __init__(self,hallnum):
        self.hall_no = hallnum
        self.seats = ServiceFactory().getInstance().getPersistentHandler().loadSeatList()
        self.capacity = len(self.seats)

    def displaySeatList(self):
        for i in range(len(self.seats)):
            self.seats[i].displaySeat()
        print(self.capacity)


# An instance of a show
class Show:
    def __init__(self, ts, movie, hall): 
        self.time_slot = ts
        self.movie = movie # object of class Movie
        self.hall = hall # object of hall
        self.availableSeats = self.hall.seats

    def getAvailableSeats(self):
        return self.availableSeats

    def getSeat(self, num):
        for i in range(len(self.availableSeats)):
            if self.availableSeats[i].seat_no == num:
                temp = self.availableSeats[i]
                self.availableSeats.pop(i)                
                break
        return temp
        
    def displayShow(self):
        print(self.time_slot +" " + self.movie.name+" " + self.hall.hall_no)
        for i in range(len(self.availableSeats)):
            self.availableSeats[i].displaySeat()
        


# Showtimes / Movie catalogue
class Showtimes:
    def __init__(self):
        self.currentShows = ServiceFactory().getInstance().getPersistentHandler().loadCurrentShows()

    def display(self):
        for i in range(len(self.currentShows)):
            print("Show: "+ self.currentShows[i].movie.name+", Time: "+ self.currentShows[i].time_slot)
            
    def getCurrentShows(self):
        return self.currentShows

    def updateShowSeats(self,show):
        for i in range(len(self.currentShows)):
            if show.movie.name == self.currentShows[i].movie.name:
                self.currentShows[i].availableSeats = show.availableSeats
                break
             
        ServiceFactory().getInstance().getPersistentHandler().saveCurrentShows(self.currentShows)


    #Problem here
    def selectShow(self, movie, time):
        num = -1
        for i in range(len(self.currentShows)):
            if self.currentShows[i].movie.name == movie and self.currentShows[i].time_slot == time:
                num = i
                break
        return self.currentShows[num]

    def displayCurrentShows(self):
        for i in range(len(self.currentShows)):
            self.currentShows[i].displayShow()

# Contains all the user's accounts
class Users:
    def __init__(self):
        self.accounts = []
        self.accounts = ServiceFactory().getInstance().getPersistentHandler().loadAccountList()       
        
    def CreateAccount(self,name,email,psw):
        acc = Account(name,email,psw)
        self.accounts.append(acc)
        self.save()
        
    def updateAccount(self,name,email,psw,user_acc):
        for i in range(len(self.accounts)):
            if self.accounts[i].name == user_acc.name:
                if self.accounts[i].psw == user_acc.psw:
                    self.accounts[i].name = name
                    self.accounts[i].email = email
                    self.accounts[i].psw = psw
                    break
        ServiceFactory().getInstance().getPersistentHandler().saveAccount(self.accounts)
        return "yes"
    
    def deleteAccount(self,user_acc):
        for i in range(len(self.accounts)):
            if self.accounts[i].name == user_acc.name:
                if self.accounts[i].psw == user_acc.psw:
                    self.accounts.pop(i)                  
                    break
        ServiceFactory().getInstance().getPersistentHandler().saveAccount(self.accounts)
        return "yes"
        
    def DisplayAccounts(self):
        for i in range(len(self.accounts)):
            print(self.accounts[i].DisplayAccount())
            
                
    def save(self,user_acc): 
        for i in range(len(self.accounts)):
            if self.accounts[i].name == user_acc.name:
                if self.accounts[i].psw == user_acc.psw:
                    self.accounts[i].saved_tickets = user_acc.saved_tickets
        ServiceFactory().getInstance().getPersistentHandler().saveAccount(self.accounts)   
    
    def findAcc(self, name, psw):
        for i in range(len(self.accounts)):
            if self.accounts[i].name == name:
                if self.accounts[i].psw == psw:
                    return i
        return -1
    
    def getAcc(self, name, psw):
        num = self.findAcc(name, psw)
        if(num != -1):
            return self.accounts[num] 
        else:
            return None
        
    def updateMemberAccount(self,user_acc):
        for i in range(len(self.accounts)):
            if self.accounts[i].name == user_acc.name:
                if self.accounts[i].psw == user_acc.psw:
                    self.accounts[i] = user_acc
                    break
        ServiceFactory().getInstance().getPersistentHandler().saveAccount(self.accounts)
        

class Membership:
    def __init__(self):
        self.member_dues = 500
        self.remaining_days = 30
        
    def getDues(self):
        return self.member_dues


# Individual account
class Account:
    def __init__(self,name,email,psw):
        self.name = name
        self.email = email
        self.psw = psw
        self.due_tickets = []
        self.saved_tickets = []
        self.is_member = False
        self.acc_membership = None

    def DisplayAccount(self):
        print(self.name + " " + self.email+ " "+ self.psw)

    def addTicket(self, ticket):
        self.due_tickets.append(ticket)

    def payDues(self,method,bank_acc):
        self.saved_tickets += self.due_tickets
        self.due_tickets.clear()
        if ServiceFactory().getInstance().getPaymentHandler(method).payDues(bank_acc) == "yes":
            return self.saved_tickets

    def upgradeToMember(self):
        if self.is_member == False:
            self.acc_membership = Membership()
            self.is_member = True
            return "yes"
        else:
            return "no"
        
    def registerPayment(self,method,bank_acc):
        return ServiceFactory().getInstance().getPaymentHandler(method).payDues(bank_acc)
        
    #
    def getMemberDues(self):
        return self.acc_membership.getDues()
    
    def payMemberDues(self, method,bank_acc):     
        check = ServiceFactory().getInstance().getPaymentHandler(method).payDues(bank_acc)
        if check == "yes":
            self.acc_membership.member_dues = 0
            self.acc_membership.remaining_days += 30
        return "yes"



class Ticket:
    def __init__(self, show, seat):
        self.show = show
        self.seat = seat
        
        

class Booking:
    def __init__(self,user_acc):
        self.user_account = user_acc
        self.show = None
        self.due_ammount = 0

    def setAccount(self, user):
        self.user_account = user

    def setShow(self, show):
        self.show = show  
    
    def selectSeat(self, seat_num):
        seat = self.show.getSeat(seat_num)
        ticket = Ticket(self.show, seat)
        self.user_account.addTicket(ticket)
        self.due_ammount += 500
        return self.due_ammount

    def payDues(self, method, bank_acc):
        return self.user_account.payDues(method, bank_acc)
        


# Cinema class [Controller]
class Cinema:
    def __init__(self):
        self.show_times = None
        self.hall_1 = Hall(1)
        self.hall_2 = Hall(2)        
        self.users = Users()
        self.booking = None
        self.user_acc = None #session
        self.upcoming_movies = None

    def Login(self, name, psw):
        self.user_acc = self.users.getAcc(name,psw)
        if self.user_acc != None:
            return "yes" 
        else:
            return "no"
            
    def browseMovies(self):
        self.upcoming_movies = ServiceFactory().getInstance().getPersistentHandler().loadUpcomingList()
        return self.upcoming_movies
    
    # Create Account
    def createAccount(self, name, email, psw):
       verify = self.users.getAcc(name,psw)       
       if verify == None:      
           self.users.CreateAccount(name, email, psw)
           return "yes"
       else:
           return "no"
       
        
    # Update Account
    def updateAccount(self,name,email,psw):
        verify =  self.users.updateAccount(name,email,psw,self.user_acc)
        
        if(verify == "yes"):
            self.user_acc.name=name
            self.user_acc.email = email
            self.user_acc.psw = psw
            return "yes"
        else:
            return "no"

    # Delete Account
    def deleteAccount(self):
        return self.users.deleteAccount(self.user_acc)
        
    # Book Ticket starts here      
    def intitaiteBooking(self):
        self.show_times = Showtimes()
        self.booking = Booking(self.user_acc)
        self.current_shows = self.show_times.getCurrentShows()
        return self.current_shows

    def selectShow(self, movie, time): 
        show = self.show_times.selectShow(movie, time)      
        self.booking.setShow(show)
        self.available_seats = show.getAvailableSeats()
        return self.available_seats

    def selectSeat(self, seat_num):
        dues = self.booking.selectSeat(seat_num)
        self.show_times.updateShowSeats(self.booking.show)
        return dues  
        
    def payDues(self, method, bank_acc):
        user_tickets = self.booking.payDues(method, bank_acc)
        self.user_acc.saved_tickets = user_tickets
        self.users.save(self.user_acc)       
        return user_tickets
        
        
    # Upgrade To Member Account
    def upgradeToMember(self,method,bank_acc):
        check1 = self.user_acc.upgradeToMember()
        if check1 == "yes":
            self.users.updateMemberAccount(self.user_acc)
            return self.user_acc.registerPayment(method,bank_acc)           
        else:
            return "no"
            
    # Pay Member Dues
    def initiateMemberDues(self):
        if self.user_acc.is_member == True:
            return self.user_acc.getMemberDues()
        else:
            return -1
    
    def payMemberDues(self, method, bank_acc):
        return self.user_acc.payMemberDues(method,bank_acc)

#Factory and handlers
class ServiceFactory():
    service_factory = None  #Static instance of Service Factory
    def __init__(self):
        self.pers_handler = None
        self.payment_handler = None
    
    def getPersistentHandler(self):
        if self.pers_handler == None:
            if save_type ==  "pickle":
                self.pers_handler = PickleHandler()
            elif save_type == "mysql":
                self.pers_handler = MySqlHandler()
            elif save_type == "oracle":
                self.pers_handler = OracleHandler()
        return self.pers_handler

    def getPaymentHandler(self,method):
        if self.payment_handler == None:
            if method ==  "credit":
                self.payment_handler = CreditHandler()
            elif method == "debit":
                self.payment_handler = DebitHandler()
        return self.payment_handler

    @staticmethod
    def getInstance():  #Static method to get the instance of Service Factory
        if ServiceFactory.service_factory == None:
            ServiceFactory.service_factory = ServiceFactory()
        return ServiceFactory.service_factory
    

# Abstract Class for DBHandler
class PersistentHandler(ABC):
    @abstractmethod
    def saveAccount(self):pass
    def loadAccountList(self):pass

# Oracle DB Class
class OracleHandler(PersistentHandler):
    def saveAccount(self, account):
         #implementation of Oracle db here
         print(account.name + " saved to oracle database")

# File handling class
class MySqlHandler(PersistentHandler):
    def saveAccount(self, account):
        #implementation of saving to a file here
        print(account.name + " saved to file")

class PickleHandler(PersistentHandler):
    
    def saveAccount(self, accounts):
        with open('Accounts.pkl', 'wb') as output:
            pickle.dump(accounts, output, pickle.HIGHEST_PROTOCOL)
            print("Successfully saved to pickle file")
        
    def loadAccountList(self):
        read_data = []
        if os.path.getsize('Accounts.pkl') != 0:
            with open('Accounts.pkl', 'rb') as input:
                read_data = pickle.load(input)
        return read_data 

    def loadSeatList(self):
        read_data = []
        if os.path.getsize('Seats.pkl') != 0:
            with open('Seats.pkl', 'rb') as input:
                read_data = pickle.load(input)
        return read_data   

    def loadUpcomingList(self):
        read_data = []
        if os.path.getsize('UpcomingMovies.pkl') != 0:
            with open('UpcomingMovies.pkl', 'rb') as input:
                read_data = pickle.load(input)
        return read_data    

    def loadCurrentShows(self):
        read_data = []
        if os.path.getsize('CurrentShows.pkl') != 0:
            with open('CurrentShows.pkl', 'rb') as input:
                read_data = pickle.load(input)
        return read_data

    def saveCurrentShows(self,cur_shows):       
        with open('CurrentShows.pkl', 'wb') as output:
            pickle.dump(cur_shows, output, pickle.HIGHEST_PROTOCOL)
            print("Successfully saved to pickle file")   

    def loadBookedTickets(self):
        read_data = {}
        if os.path.getsize('TicketDictionary.pkl') != 0:
            with open('TicketDictionary.pkl', 'rb') as input:
                read_data = pickle.load(input)
        return read_data

    def saveTickets(self, booked_tickets):
        with open('TicketDictionary.pkl', 'wb') as output:
            pickle.dump(booked_tickets, output, pickle.HIGHEST_PROTOCOL)
            print("Saved to pickle file")


# Abstract Class for Payment Handler
class PaymentHandler(ABC):
    @abstractmethod
    def payDues(self):pass

class CreditHandler(PaymentHandler):
    def payDues(self, account):
        print("Credit Transaction from "+ account)
        return "yes"

class DebitHandler(PaymentHandler):
    def payDues(self, account):
        print("Debit Transaction from "+ account)
        return "yes"
            


save_type = "pickle"#put this in file




#save_handler = ServiceFactory().getInstance().getPersistentHandler()
#save_handler.saveAccount("hello")



# main functionality 

# save = ""
# pers_handler = None
# input(save)
# if(save == "oracle"):
#     pers_handler = OracleHandler()
# elif(save == "file"):
#     pers_handler = FileHandler()



# seat1 = Seat(1, 1, 1)
# seat2 = Seat(2, 1, 2)

# seats = []
# seats.append(seat1)
# seats.append(seat2)

# h1 = Hall(1, seats)

# a = Movie("a")
# b = Movie("b")
# c = Movie("c")

# s1 = Show("7:30-8:30", a, h1)
# s2 = Show("1:30-3:00", b, h1)
# s3 = Show("12:00-1:30", c, h1)

# shows = []
# shows.append(s1)
# shows.append(s2)
# shows.append(s3)

# st = Showtimes(shows)



# print("Shows Available")
# Cin = Cinema(pers_handler)
# Cin.browseMovies(st)
# Cin.show_times.display()
# Cin.createAccount("Omer","foo@foolish.com","php")
# Cin.createAccount("Hayat","foo@foolish.com","diana")
# Cin.createAccount("buraq","foo@foolish.com","nofaith")

            


