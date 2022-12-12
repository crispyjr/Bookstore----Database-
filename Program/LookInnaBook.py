import psycopg2

UserData={'UserId':'0',
          'Username': '000',
          'Role':'0',
          'Billing':'0',
          'Address':'0'} 
bookData={'quit':0}

def login():
    #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    u = input("Enter Username: ")
    p = input("Enter Password: ")
    #execute the query
    cur.execute("select * from users")

    rows = cur.fetchall()

    userExists = 0
    for r in rows:
        if u.lower()==r[1].lower():
            if p == r[2]:
                userExists = 1
                user=r


    if(userExists):
        UserData["UserId"]=user[0]
        UserData["Username"]=user[1]
        UserData["Role"]=user[6]
        UserData["Billing"]=user[4]
        UserData["Address"]=user[5]
        print("Welcome back "+UserData["Username"]+"!")

    else:
        print("User/Password incorrect. Try again")

    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def register():
    user = input("enter username: ")
    pw = input("enter pass: ")
    email = input("enter email: ")
    f_name = input("Enter first name: ")
    l_name = input("Enter last name: ")
    card = input("Enter bank card number: ")
    exp = input("Enter expiration date: ")
    css = input("Enter security number: ")
    street = input("Enter street name: ")
    postal = input("Enter postal code: ")
    city = input("Enter city: ")
    country = input("Enter country: ")

    #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    cur.execute("select * from users where username=%s",(user,))
    rows = cur.fetchall()
    if(len(rows)>0):
        user = input("Username already exists, try again: ")

    cur.execute("select * from users where email=%s",(email,))
    rows = cur.fetchall()
    if(len(rows)>0):
        email = input("email already in use. Please enter a different one: ")


    #execute the query
    cur.execute("select * from billing")
    billingrows = cur.fetchall()
    billingId = int(billingrows[len(billingrows)-1][0])+1
    cur.execute("insert into billing (ID, Fname, Lname, CardNumber, SecurityNumber,ExpirationDate) values (%s, %s, %s, %s, %s, %s)", (str(billingId),f_name,l_name,card,css,exp))
   
    cur.execute("select * from address")
    addressRows = cur.fetchall()
    addressID = int(addressRows[len(addressRows)-1][0])+1
    cur.execute("insert into address (ID, Street, PostalCode, City, Country) values (%s,%s,%s,%s,%s)", (str(addressID),street,postal,city,country))
    
    cur.execute("select * from users")
    userRows = cur.fetchall()
    userID = int(userRows[len(userRows)-1][0])+1
    cur.execute("insert into users (ID, Username, Password, Email, BillingID, AddressID, Role) values (%s,%s,%s,%s,%s,%s,%s)", (str(userID),user, pw, email, str(billingId),str(addressID),"Customer"))
    #row = cur.fetchall()
    #print(row)
    cur.execute("select * from users")
    userRows = cur.fetchall()
    #print(userRows)
    
    #Commit changes to the actual database
    con.commit()
    #close the cursor
    cur.close()
    #Close the connection
    con.close()
    print("Register successful! Try logging in with your new account!")

def addBook():
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()
    if(UserData["Role"]!='Owner'):
        print("You don't have access to this command")
        return

    #get author name
    afname = input("Enter Author's first name: ")
    alname = input("Enter Author's last name: ")
     

    #find author
    cur.execute("select * from author")

    AUrows = cur.fetchall()
    AUexist = 0
    for r in AUrows:
        if afname.lower() == r[1].lower():
            if alname.lower() == r[2].lower():
                AuthorID=r[0]
                AUexist = 1
                break
    if(not AUexist):
        print("author not found")
        AuthorID =  int(AUrows[len(AUrows)-1][0])+1
        cur.execute("insert into author (ID, Fname, Lname) values (%s,%s,%s)", (str(AuthorID),afname,alname))


        

    #get publisher name
    pname = input("Enter Publisher's name: ")
    #find publisher
    cur.execute("select * from publishers")
    pubRows = cur.fetchall()
    pubExist = 0
    for r in pubRows:
        if pname.lower() == r[0].lower():
            pubExist=1
    if(not pubExist):
        pemail = input("Enter Publisher's email: ")
        pnumber = input("Enter Publisher's phone number: ")
        cur.execute("insert into publishers (Name, Email, phonenumber, BankAccount) values (%s,%s,%s,%s)", (pname, pemail, pnumber,0))

    #Find book
    cur.execute("select * from books")

    isbn = input("Enter ISBN: ")
    
    bookRows = cur.fetchall()
    bookExists = 0

    for r in bookRows:
        if(isbn == r[0]):
            bookExists = 1

    if(bookExists==1):
        print("book already exists")
        return

    #If book doesnt exist, proceed
    book = input("Enter Book Name: ")
    pages = input("Enter amount of pages: ")
    price = input("Enter price: ")

    #add to tables
    cur.execute("insert into books (isbn, bookName, pages, price, quantity, pubname) values (%s,%s,%s,%s,%s,%s)", (isbn, book, int(pages), float(price), 20, pname))
    cur.execute("insert into writes (ISBN, AuthorID) values (%s,%s)",(isbn,AuthorID))
    
    nOfGens = int(input("How many genres are there?: "))
    #nOfGens = int(nOfGens)
    for i in range(nOfGens):
        genre = input("Enter the genre: ")
        cur.execute("insert into genbook (ISBN, Genre) values (%s,%s)", (isbn, genre))

    print(book+" has been successfully added")

    
    
    

    

    con.commit()
    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def searchBookByGenre():
    #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    #execute the query
    #cur.execute("select * from author, writes, books where  writes.AuthorID = author.id and writes.isbn = books.isbn")
    
    #cur.execute("select * from genbook, books where  genbook.genre = {} and genbook.isbn=books.isbn".format(genre))
    cur.execute("select * from genBook")
    genre = input("enter genre: ")
    genrerows = cur.fetchall()
    isbnSet = {*()}
    for r in genrerows:
        if(genre.lower()==r[1].lower()):
            isbnSet.add(r[0])
           # print(r)
    #print(isbnSet)

    cur.execute("select * from books")
    bookRows = cur.fetchall()
    print("Results for books with the "+genre+" tag: ")
    for r in bookRows:
        for x in isbnSet:
            if (x==r[0]):
                print(x+" "+r[1])
                



    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def searchBookByAuthor():
    print("aa")
    afname = input("Enter Author's first name: ")
    alname = input("Enter Author's last name: ")
    #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    #find author id first
    cur.execute("select * from author")
    AUrows = cur.fetchall()
    AUexist = 0
    for r in AUrows:
        if afname.lower() == r[1].lower():
            if alname.lower() == r[2].lower():
                AuthorID=r[0]
                AUexist = 1
                break
    if(not AUexist):
        print("author not found")
        return
    #execute the query
    cur.execute("select * from author, writes, books where  writes.AuthorID = author.id and writes.isbn = books.isbn")
    
    rows = cur.fetchall()
    #set = {*()}
    #print(rows)
    print("Books made by "+afname+" "+alname+ ": ")
    for r in rows:
        if(r[0]==AuthorID):
            print(r[5]+" "+r[6])
            #print(r[1],r[2],r[6])

   # print("Books made by "+afname+" "+alname+ ": ")
    #for x in set:
     #   print(x)



    #cur.execute("select * from genbook, books where  genbook.genre = {} and genbook.isbn=books.isbn".format(genre))
    
    #print(isbnSet)

    
    #print(bookSet)

    

    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def searchBookByName():
    #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    book = input("Enter book name: ")

    cur.execute("select isbn,bookname from books")

    bookrows = cur.fetchall()

    print("Books with the title "+book+": ")
    for r in bookrows:
        if book.lower() in r[1].lower():
            print(r[0]+" "+r[1])




    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def searchBookByISBN():
        #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    isbn = input("Enter isbn: ")

    cur.execute("select isbn,bookname from books")

    bookrows = cur.fetchall()

    print("Isbn book "+isbn+": ")
    for r in bookrows:
        if isbn == r[0]:
            print(r[0]+" "+r[1])




    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def deleteBook():
    if(UserData["Role"]!='Owner'):
        print("You do not have permission to use this command!")
        return

    #Connect to the database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    isbn = input("Enter isbn: ")
    ahh = "delete from writes where isbn=%s"
    cur.execute(ahh,(isbn,))
    cur.execute("delete from shoppingCart where isbn=%s",(isbn,))
    cur.execute("delete from genbook where isbn=%s",(isbn,))
    cur.execute("delete from books where isbn=%s",(isbn,))

    cur.execute("select bookname from books")
    bookrows = cur.fetchall()

    print("The book has been removed. Author and Publisher both remain")




    con.commit()
    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def viewCart():
    if(UserData["UserId"]=='0'):
        print("Login first!")
        return

    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()
    cur.execute("select * from shoppingcart where userid=%s and sold=false",(UserData["UserId"],))
    
    srows=cur.fetchall()
    if(len(srows)==0):
        print("there is nothing in your cart")
        #close the cursor
        cur.close()
        #Close the connection
        con.close()
        return 0
    
    print("*********"+UserData["Username"]+"'s Cart********")
    for r in srows:
        cur.execute("select bookname from books where isbn=%s",(r[2],))
        b=cur.fetchall()
        print(r[2]+" "+b[0][0]+" | Quantity: "+str(r[3]))
        
       #

    #for r in srows:
    #    if(r[4]==False):
    #        print("its false!")
    #print(srows)
    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def addtoShoppingCart():

    if(UserData["UserId"]=='0'):
        print("Login first!")
        return
    
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()
    #enter the isbn
    #enter the quantity
    isbn = input("Enter isbn: ")
    
    cur.execute("select bookname,quantity from books where isbn=%s",(isbn,))

    brows = cur.fetchall()

    if(len(brows)==0):
        print("Book does not exist.")
        return

    print(brows[0][0])
    #if book stock is lower than 10, automatically checkout book. 
    quantity = input("Enter Quantity: ")

    if(int(quantity)<int(brows[0][1])):
        print("good to go")
    
    else:
        print("Quantity out of bounds")
        #close the cursor
        cur.close()
        #Close the connection
        con.close()
        return

    #Check if book is already in shopping cart
    cur.execute("select * from shoppingcart where userid=%s",(UserData["UserId"],))
    srows = cur.fetchall()
    shopID = 0
    for r in srows:
        if(r[2]==isbn):
                shopID=r[0]
                shopQuan=r[3]
                print("found")
                break

    if(int(shopID)>0):
        shopQuan=int(shopQuan)+int(quantity)
        cur.execute("update shoppingcart set quantity=%s where userid=%s and isbn=%s",(shopQuan,UserData["UserId"],isbn,))
        cur.execute("select * from shoppingcart")
        #print(cur.fetchall())
        #print("touch**********************************************8")
        print("Book found. Updated quantity")
    else:
        cur.execute("select * from shoppingcart order by id")
        srows = cur.fetchall()
        sID = int(srows[len(srows)-1][0])+1
        #print(sID)
        cur.execute("insert into shoppingcart (ID,UserID, ISBN, Quantity, Sold) values (%s,%s,%s,%s,%s)",(sID,UserData["UserId"],isbn,quantity,False))

        #cur.execute("select * from shoppingcart")
        #print(cur.fetchall())
        print("Book added!")
    
    con.commit()
    #close the cursor
    cur.close()
    #Close the connection
    con.close()

def checkout():
    if(UserData["UserId"]=='0'):
        print("Login first!")
        return
    print("Reminder, this is what's inside your cart: ")
    
    #if they have nothing in cart, return
    c = viewCart()
    if(c==0):
        return
    
    n = input("Would you like to check out?")
    if(n.lower()=="yes"):
        print("Proceeding to checkout. ")
    else:
        print("Checkout cancelled")
        return
    #Connect to Database
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    #get items from cart where sold=false
    cur.execute("select isbn,quantity from shoppingcart where userid=%s and sold=%s",(UserData["UserId"],False,))

    srows = cur.fetchall()
    #print(srows)
    total = 0
    cur.execute("select isbn,bookname,quantity,price from books")
    brows = cur.fetchall()
    #print(brows)

    for r in brows:
        for x in srows:
            if(x[0]==r[0]):
                #quantity x price
                p = x[1] * r[3]
                print(r[0]+" "+r[1]+" | Quantity: "+str(x[1])+" x "+str(r[3])+" = "+str(p))
                
                total=total+p
    print("Total: "+str(total))
    n = input("Would you like to purchase?")
    if(n.lower()=="yes"):
        print("Okay great!")
    else:
        print("Checkout cancelled.")
        #close the cursor
        cur.close()
        #Close the connection
        con.close()
        return

    #put new order in table
    cur.execute("select * from orders order by ordernum")
    oRows=cur.fetchall()
    orderID=int(oRows[len(oRows)-1][0])+1
    #print(orderID)
    trackingnum="000000000000"
    deliverystatus="Processing"
    cur.execute("insert into orders (OrderNum, UserID, BillingID, AddressID, trackingnumber, deliverystatus) values (%s,%s,%s,%s,%s,%s)",(str(orderID),UserData["UserId"],UserData["Billing"],UserData["Address"],trackingnum,deliverystatus))
    cur.execute("select * from orders")
    #print(cur.fetchall())

    #change shopping cart sold to true
    cur.execute("update shoppingcart set sold=true where userid=%s",(UserData["UserId"],))

    cur.execute("select * from shoppingcart")
    print(cur.fetchall())
    #Decrease book quantity
    for r in brows:
        for x in srows:
            if(x[0]==r[0]):
                q=int(r[2]) - int(x[1])
                #update shoppingcart set sold=true where userid='103';
                cur.execute("update books set quantity=%s where isbn=%s",(q,x[0]))
                #quantity x price

    cur.execute("select * from books")
    #print(cur.fetchall())    

    print("Purchase successful! Order Number: "+str(orderID))
                
    con.commit()
    #close the cursor
    cur.close()
    #Close the connection
    con.close()
    
def getOrderStatus():
    con = psycopg2.connect(
        host = "localhost",
        database = "Project",
        user = "postgres",
        password = "Meleshia14")

    #cursor
    cur = con.cursor()

    print("******|"+UserData["Username"]+" Orders |********")
    print("Order Num__________Tracking Number_______________Delivery Status")
    cur.execute("select OrderNum, TrackingNumber, DeliveryStatus from orders where userid=%s",(UserData["UserId"],))
    oRows = cur.fetchall()
    if(len(oRows)==0):
        print("You have no orders")
    else:
        for r in oRows:
            print(r[0]+"          "+r[1]+"           "+r[2])

    #close the cursor
    cur.close()
    #Close the connection
    con.close()



def main():
    print("Hello! Welcome to Look Inna Book!")
    print("If you'd like a list of the commands, simply say 'Commands'")
    while not bookData["quit"]:
        handleInput()
        print(quit)
    

def handleInput():
    word = input('>')
    if("QUIT" in word.upper()):
        bookData["quit"]=1
    
    elif("COMMANDS" in word.upper()):
        commands()
       
    elif("LOGIN" in word.upper()):
        login()

    elif("REGISTER" in word.upper()):
        register()

    elif("ADD BOOK" in word.upper()):
        addBook()
    
    elif("DELETE BOOK" in word.upper()):
        deleteBook()
    
    elif("SEARCH" in word.upper()):
        print("Search by Genre, ISBN, Author, or Book Name?")
        word = input('>') 
        if("GENRE" in word.upper()):
            searchBookByGenre()
        elif("BOOK NAME" in word.upper()):
            searchBookByName()
        elif("AUTHOR" in word.upper()):
            searchBookByAuthor()
        elif("ISBN" in word.upper()):
            searchBookByISBN()
        else:
            print("Invalid command.")
            return
    
    elif("VIEW CART" in word.upper()):
        viewCart()

    elif("ORDER STATUS" in word.upper()):
        getOrderStatus()

    elif("ADD TO CART" in word.upper()):
        addtoShoppingCart()

    elif("CHECKOUT" in word.upper()):
        checkout()
    else:
        return
    
def commands():
    print("LOGIN")
    print("REGISTER")
    print("SEARCH")
    print("VIEW CART")
    print("ORDER STATUS")
    print("ADD TO CART")
    print("CHECKOUT")
    if(UserData["Role"]=="Owner"):
        print("ADD BOOK")
        print("DELETE BOOK")


main()
