###########################################
# Main file, includes multiple classes and all relevant functions, which may under other 
# circumstances store separately, however for ease of use for this test, decided to keep
# everything in the same file
###########################################

## Main object classes, users (payers), transactions, and transaction lists (of which there should just be one)

class User:
    def __init__(self,name,points):
        self.name = name
        self.points = points

class Transaction:
    def __init__(self,payer,points,timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp

    def processInput(inputString):
        # Transaction should be a list of 3 strings, payer, points, and timestamp
        payer = inputString[0]
        points = inputString[1]
        timestamp = inputString[2]

        # String processing - removing extra characters around relevant info
        payer = cleanInput(payer)
        points = int(cleanInput(points))
        timestamp = cleanInput(timestamp)

        return Transaction(payer,points,timestamp)

class TransList:
    def __init__(self):
        self.translist = []
        self.userlist = []

    def addTransaction(self,transaction):
        newTransaction = Transaction.processInput(transaction) # Cleans strings and returns a transaction object
        self.translist.append(newTransaction) # Adds to transaction list
        
        # If user is new, add user and give them points, if old user, update points
        isNew = True
        for i in range(len(self.userlist)):
            if newTransaction.payer == self.userlist[i].name:
                self.userlist[i].points += newTransaction.points
                isNew = False
        if isNew == True:
            self.userlist.append(User(newTransaction.payer,newTransaction.points))

        # Sort by date whenever transactions are added
        self.translist.sort(key=sortDate)


    def spendPoints(self,points):
        pointsspent = int(cleanInput(points)) # Cleans string input
        sortlist = self.sortList() # Negative transactions are applied to oldest transactions from the same payer

        # Goes forward through transaction list sorted by date
        # Spends points from oldest transactions first, future negative transactions
        # have been taken into account so points never go negative.
        for i in range(len(sortlist)):
            # sortlist[i] is transaction in question
            if sortlist[i].points <= 0:
                dif = 0
            elif sortlist[i].points < pointsspent:
                dif = -sortlist[i].points
                pointsspent += dif
                sortlist[i].points == 0
            elif sortlist[i].points >= pointsspent:
                dif = -pointsspent
                sortlist[i].points += dif
                pointsspent = 0
                
            if dif != 0:
                print( '     { "payer": ', sortlist[i].payer, "points: ", dif, " },")

            # Applies change in points to account/user list
            for j in range(len(self.userlist)):
                if sortlist[i].payer == self.userlist[j].name:
                    self.userlist[j].points += dif
                    
            # When all spent points are accounted for, break
            if pointsspent <= 0:
                break

        # Updates transaction list for simplicity. Will lose records but simplify
        # data for the functions.
        self.translist = sortlist

    def getAccounts(self):
        # Print account numbers
        print("{")
        for i in range(len(self.userlist)):
            ulist = self.userlist[i]
            print("    ", ulist.name, ": ", ulist.points, ",")
        print("}")

    def sortList(self):
        # if transactions that subtract points are present for some payer at any point,
        # subtract those points from earlier transactions, in order from oldest to newest,
        # by the same payer.
        # Used only when spending points, does not activate automatically in case of calls
        # being out of order chronologically
        
        sortlist = self.translist
        for j in range(len(self.translist)):
            if sortlist[j].points < 0:
                negpoints = sortlist[j].points
                for k in range(j):
                   if sortlist[k].payer == sortlist[j].payer and negpoints < 0:
                       if sortlist[k].points >= negpoints:
                           sortlist[k].points += negpoints
                           negpoints = 0
                       elif sortlist[k].points < negpoints:
                           negpoints += sortlist[k].points
                           sortlist[k].points = 0
                if negpoints > 0:
                    print("Error: negative points for payer ", sortlist[j].payer)
                else: sortlist[j].points = 0
        return sortlist


## A handful of general functions, for use outside of objects

def cleanInput(string):
    # Takes out extraneous characters from input strings
    stringPair = string.split(':',1)
    string = stringPair[1]
    for i in range(10):
        string = string.strip(' {}()[]" ')
    return string

def sortDate(transaction): # Key for sorting transactions by date
    return transaction.timestamp

def intro():
    print("Hello, please enter calls below.")
    print("")
    print("For adding a transaction, enter a list of the format: '{ 'payer': <string>, 'points': <integer> }, 'timestamp': <timestamp> }'.")
    print("")
    print("To spend points, enter a list of the format:  '{ 'points': <points> }'. ")
    print("")
    print("To see account balances, enter the number '1' or the string 'get accounts'.")
    print("")
    print("If you would like these instructions repeated, enter the number '2' or the string 'info'. ")
    print("")


intro()
transList = TransList()

while True:
    # Check for input
    x = input('Input call here: ')

    # Check for Point Balance path
    if x.find("1",0,4) != -1 or x.find("get accounts",0,15) != -1:
        transList.getAccounts()
    elif x.find("2",0,4) != -1 or x.find("info",0,6) != -1:
        intro()

    # Otherwise, parse string and call function based on length
    else:
        xsplit = x.split(',')
        if len(xsplit) == 1: # If input is a single item, treat as a spend points call
            transList.spendPoints(x)
        elif len(xsplit) == 3:
            transList.addTransaction(xsplit)
        else: # Exception handling
            print("Input reading error; did not understand input. See instructions for input formats")
        








