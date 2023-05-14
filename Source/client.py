import tkinter as tk
import socket
import json
from tkinter.constants import END, SINGLE, TRUE

HOST = "127.0.0.1"
SERVER_PORT = 63000
FORMAT = "utf8"

LIST = "list"
LOGIN = "login"
FAIL = 'fail'
SUCCESS = 'Successfull'
SIGNUP = 'signup'
INVALID = 'invalid'
FORMATPASS = 'wrong format pass'
FORMATUSERNAME = 'wrong format username'
FORMATBANKCODE = 'wrong format bankcode'
DUPLICATEUSER = 'duplicate user name'
FINDROOM = 'room information'
FINDROOMBOOK = 'room book'
FAILFINDROOM = 'fail find room'
BOOKROOM = 'book room'
checkboxlist=[]
listtHotelName = []
acc = {}
roomlist=[]
bedlist=[]
roomAvai = []
Bookedroom = []
curframee = None
ROOMBOOKED = 'room booked'
total = 0
def sendList(client,list):
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(2024)
    msg = "end"
    client.sendall(msg.encode(FORMAT))

def recvListt(client):
    list = []
    item = client.recv(2024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        client.sendall(item.encode(FORMAT))
        item = client.recv(2024).decode(FORMAT)
    return list

def inputhotel(hotellist):
    for i in listtHotelName:
        hotellist.insert(END, "hotel " + i)

def inputroom(roomlist):
    for i in range(20):
        roomlist.insert(END, "room " + i)

def clickEventHotellist(event):
    temp = app.hotellist.curselection()
    if temp:
        app.frames[HotelInfoPage].indexHotel = temp[0]
def checkDateEntryLeaving(DateEntry,DateLeaving):
    if(int(DateLeaving[0]) < int(DateEntry[0])):
        return False
    elif (int(DateLeaving[0]) == int(DateEntry[0])):
        if(int(DateLeaving[1]) < int(DateEntry[1])):
            return False
        elif(int(DateLeaving[1]) == int(DateEntry[1]) and int(DateLeaving[2]) < int(DateEntry[2])):
            return False
    return True
def changeframe(curfram):
    global curframee
    curframee = curfram
class RemoveRoom(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self,text="Remove booked room")
        notice = tk.Label(self,text="All room you have booked")
        self.price = tk.Label(self,text="")
        scrollbar = tk.Scrollbar(self,bg='white')
        
        app.canvas1=tk.Canvas(self,yscrollcommand=scrollbar.set)
        app.canvas1.create_window(1,1,window= tk.Frame())     

        Home= tk.Button(self,text="Go back",command=lambda: (app.showPage(HomePage),app.frames[HotelInfoPage].DeleteThing()))
        Enter= tk.Button(self,text="Enter",command=lambda: (app.showPage(RemoveRoom)))
        title.grid(row=0,column=0,columnspan=10)
        self.grid_columnconfigure(0,minsize=25)

        scrollbar.grid(row=2,column=2,sticky="sn")
        scrollbar.config(command=app.canvas1.yview)

        self.grid_columnconfigure(3,minsize=25)
        self.grid_rowconfigure(1,minsize=25)

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        app.canvas1.grid(row=2,column=1,sticky="wesn")
        notice.grid(row=3,column=1,sticky="w")
        self.price.grid(row=3,column=1,sticky="e")
              
        self.grid_rowconfigure(4,minsize=20)
        Home.grid(row=5,column=1,sticky="w")
        Enter.grid(row=5,column=1,sticky="e")

        self.grid_rowconfigure(6,minsize=25)

# def sendremovedlist(notice,price):
#     j=-1
#     Bookedroom.clear()
#     for i in roomAvai:
#         j+=1
#         if(checkboxlist[j].get() == 1):
#             Bookedroom.append(i["IDroom"])
#     print(Bookedroom)
#     notice.config(text="                    You have remove booked room")
#     price.config(text="Price: "+ str(total))
def roomBookedInfo(client):
    msg = ROOMBOOKED
    client.sendall(msg.encode(FORMAT))
    client.recv(1024)
    global acc
    if(len(acc['Booked room']) != 0):
        msg = 'ok'
        client.sendall(msg.encode(FORMAT))
        listt1 = []
        for booked in acc['Booked room']:
            rom = {'ID': booked['IDhotel'], 'listroomBooked' : booked['Booked']['Booked']}
            listt1.append(rom)
        listt1 = [json.dumps(i) for i in listt1]
        sendList(client,listt1)
        global roomAvai
        roomAvai = recvListt(client)
        roomAvai = [json.loads(i) for i in roomAvai]
    else:
        msg = 'no'
        client.sendall(msg.encode(FORMAT))

class BookRoom(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self,text=" Book hotel room")
        notice = tk.Label(self,text="")
        price = tk.Label(self,text="")
        scrollbar = tk.Scrollbar(self,bg='white')
        
        app.canvas=tk.Canvas(self,yscrollcommand=scrollbar.set)
        app.canvas.create_window(1,1,window= tk.Frame())     

        Home= tk.Button(self,text="Go back",command=lambda: (app.showPage(HomePage),app.frames[HotelInfoPage].DeleteThing(),notice.config(text=""),price.config(text="")))
        Enter= tk.Button(self,text="Enter",command=lambda: (app.showPage(BookRoom),sendbookedlist(),self.sendBookroomtoserver(client,notice,price)))
        title.grid(row=0,column=0,columnspan=10)
        self.grid_columnconfigure(0,minsize=25)

        scrollbar.grid(row=2,column=2,sticky="sn")
        scrollbar.config(command=app.canvas.yview)

        self.grid_columnconfigure(3,minsize=25)
        self.grid_rowconfigure(1,minsize=25)

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        app.canvas.grid(row=2,column=1,sticky="wesn")
        notice.grid(row=3,column=1,sticky="w")
        price.grid(row=3,column=1,sticky="e")
              
        self.grid_rowconfigure(4,minsize=20)
        Home.grid(row=5,column=1,sticky="w")
        Enter.grid(row=5,column=1,sticky="e")

        self.grid_rowconfigure(6,minsize=25) 
    def sendBookroomtoserver(self,client,notice,price):
        msg = BOOKROOM
        client.sendall(msg.encode(FORMAT))
        client.recv(1024)
        global Bookedroom
        if(len(Bookedroom) != 0):
            msg = 'ok'
            client.sendall(msg.encode(FORMAT))
            bookedrom = Bookedroom
            bookedrom = [str(i) for i in bookedrom]
            indexHotell = None
            sendList(client,bookedrom)
            client.sendall(acc['username'].encode(FORMAT))
            client.recv(1024)
            global curframee
            if(curframee == HotelInfoPage):
                indexHotell = str(app.frames[HotelInfoPage].indexHotel)
                client.sendall(indexHotell.encode(FORMAT))
                client.recv(1024)
                Dayentry = app.frames[HotelInfoPage].dayentry.get()
                Monthentry =app.frames[HotelInfoPage].monthentry.get()
                Yearentry =app.frames[HotelInfoPage].yearentry.get()
                Dayexit = app.frames[HotelInfoPage].dayexit.get()
                Monthexit =app.frames[HotelInfoPage].monthexit.get()
                Yearexit =app.frames[HotelInfoPage].yearexit.get()
                listentry = [Yearentry, Monthentry, Dayentry]
                listexit = [Yearexit, Monthexit, Dayexit]
                sendList(client,listentry)
                client.recv(1024)
                sendList(client,listexit)
                client.recv(1024)
            elif(curframee == BookingPage):
                indexHotell = app.frames[BookingPage].name.get()
                client.sendall(indexHotell.encode(FORMAT))
                client.recv(1024)
                dayEntry = app.frames[BookingPage].dayentry.get()
                monthEntry = app.frames[BookingPage].monthentry.get()
                yearEntry = app.frames[BookingPage].yearentry.get()
                dayLeaving = app.frames[BookingPage].dayexit.get()
                monthLeaving = app.frames[BookingPage].monthexit.get()
                yearLeaving = app.frames[BookingPage].yearexit.get()
                DateEntry = [yearEntry,monthEntry,dayEntry]
                DateLeaving = [yearLeaving,monthLeaving,dayLeaving]
                sendList(client,DateEntry)
                client.recv(1024) 
                sendList(client,DateLeaving)
                client.recv(1024)
            msg = 'ok'
            Bookedroomm = client.recv(1024).decode(FORMAT)
            client.sendall(msg.encode(FORMAT))
            acc['Booked room'].append(json.loads(Bookedroomm))
            Bookedroomm = json.loads(Bookedroomm)
            global total
            total = Bookedroomm['price']
            notice.config(text="                You have booked the room")
            price.config(text="Price: "+ str(total))
        else:
            msg = 'no'
            client.sendall(msg.encode(FORMAT))
def sendbookedlist():
    j=-1
    global Bookedroom
    Bookedroom.clear()
    for i in roomAvai:
        j+=1
        if(checkboxlist[j].get() == 1):
            Bookedroom.append(i["IDroom"])

def inputname(canvas,room):
    roomlist= tk.Frame(canvas,bg='white')
    roomlist.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  
    roomtype = tk.Label(roomlist,text="Room type",bg='white')
    bedtype = tk.Label(roomlist,text="Bed type",bg='white')
    Describe = tk.Label(roomlist,text="Describe",bg='white')
    Price = tk.Label(roomlist,text="Price",bg='white')
    image = tk.Label(roomlist,text="Image",bg='white')

    roomtype.grid(row=0,column=0,sticky='nwse')
    bedtype.grid(row=0,column=1,sticky='nwse')
    Describe.grid(row=0,column=2,sticky='nwse')
    Price.grid(row=0,column=3,sticky='nwse')
    image.grid(row=0,column=4,sticky='nwse')
    roomlist.grid_rowconfigure(1,minsize=20)
    for i in range(5):
            roomlist.grid_columnconfigure(i,minsize=146)
    checkboxlist.clear()
    for i in range(len(room)):
        var=tk.IntVar()
        check= tk.Checkbutton(roomlist,text=room[i]['TypeRoom'],variable=var,bg='yellow')
        checkboxlist.append(var)
        label= tk.Label(roomlist,text=room[i]["Bed"],bg='white')
        label1= tk.Label(roomlist,text=room[i]["Describe"],wraplength=150,bg='white')
        label2= tk.Label(roomlist,text=room[i]["Price"],bg='white')
        #label3= tk.Label(roomlist,bitmap=roomAvai[i]["Image"])
        check.grid(row=i+2,column=0,sticky='w')
        label.grid(row=i+2,column=1,sticky='w')
        label1.grid(row=i+2,column=2,sticky='w')
        label2.grid(row=i+2,column=3)
        #label3.grid(row=i+2,column=4,sticky='nwse')
    canvas.delete("all")
    canvas.create_window(1, 1, window= roomlist)
     
class BookingPage(tk.Frame):
    def __init__(self,parent,app,client):       
        tk.Frame.__init__(self,parent)
        self.notice = tk.Label(self,text='',bg='bisque')
        title = tk.Label(self,text=" Book a hotel room")
        hotelName = tk.Label(self,text="Hotel name/code: ")
        roomtype = tk.Label(self,text="Room type: ")
        bedtype = tk.Label(self,text="Bed type: ")
        DateOfEntry = tk.Label(self, text = 'Date of entry: ')
        DateOfExit = tk.Label(self,text="Date of exit: ")
        self.check1 = tk.IntVar()
        self.check2 = tk.IntVar()
        self.check3 = tk.IntVar()
        self.check4 = tk.IntVar()
        self.check5 = tk.IntVar()
        Stand = tk.Checkbutton(self,text="Standard Room",variable=self.check1)
        Super = tk.Checkbutton(self,text="Superior Room",variable=self.check2)
        Single = tk.Checkbutton(self,text="Single Bed",variable=self.check3)
        Twin = tk.Checkbutton(self,text="Twin Bed",variable=self.check4)
        Double = tk.Checkbutton(self,text="Double Bed",variable=self.check5)
        def RoomBedlist():
            roomlist.clear()
            bedlist.clear()
            if(self.check1.get()==1):
                roomlist.append("Standard Room")
            if(self.check2.get()==1):
                roomlist.append("Superior Room")
            if(self.check3.get()==1):
                bedlist.append("Single Bed")
            if(self.check4.get()==1):
                bedlist.append("Twin Bed")
            if(self.check5.get()==1):
                bedlist.append("Double Bed")
            for i in (self.check1,self.check2,self.check3,self.check4,self.check5):
                i.set(0)
            # check list
            #print(roomlist,bedlist)
        Home= tk.Button(self,text="Back to \n home page",command=lambda: app.showPage(HomePage))
        Enter= tk.Button(self,text="Enter",command=lambda: (RoomBedlist(),self.BookedRoomList(client),changeframe(BookingPage),inputname(app.canvas,roomAvai)))
        Note = tk.Label(self,text="Note: ")
        self.name = tk.Entry(self,bg='white',width=30)        
        self.Enote = tk.Entry(self,bg='white',width=30)
        Date = tk.Frame(self)

        slash = tk.Label(Date,text="/")
        slash1 = tk.Label(Date,text="/")
        slash2 = tk.Label(Date,text="/")
        slash3 = tk.Label(Date,text="/")

        self.dayentry = tk.Entry(Date,bg = 'white',width=2)
        self.monthentry = tk.Entry(Date,bg = 'white',width=2)
        self.yearentry = tk.Entry(Date,bg = 'white',width=4)

        self.dayexit = tk.Entry(Date,bg = 'white',width=2)
        self.monthexit = tk.Entry(Date,bg = 'white',width=2)
        self.yearexit = tk.Entry(Date,bg = 'white',width=4)

        self.grid_rowconfigure(1,weight =1)
        self.grid_rowconfigure(15,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(8,weight =1)

        title.grid(row=0,column=0,columnspan=10)
        self.notice.grid(row=1,column=0,columnspan=10,sticky='n')

        hotelName.grid(row=2,column=1,sticky="w")
        self.name.grid(row=2,column=2,columnspan=5)
        self.grid_rowconfigure(3,minsize=10)

        roomtype.grid(row=4,column=1,sticky="w")
        Stand.grid(row=4,column=2)
        Super.grid(row=4,column=3)
        self.grid_rowconfigure(5,minsize=10)

        bedtype.grid(row=6,column=1,sticky="w")
        Single.grid(row=6,column=2)
        Double.grid(row=6,column=3)
        Twin.grid(row=6,column=4)
        self.grid_rowconfigure(7,minsize=10)
        Date.grid(row=8,column=2,rowspan=3,columnspan=3)

        DateOfEntry.grid(row=8,column=1,sticky="w")
        self.grid_rowconfigure(9,minsize=10)
        DateOfExit.grid(row=10,column=1,sticky="w")
        
        self.dayentry.grid(row=8,column=2)
        self.dayexit.grid(row=10,column=2)
        slash.grid(row=8,column=3)
        slash1.grid(row=10,column=3)
                
        self.monthentry.grid(row=8,column=4)
        self.monthexit.grid(row=10,column=4)
        slash2.grid(row=8,column=5)
        slash3.grid(row=10,column=5)

        self.yearentry.grid(row=8,column=6)
        self.yearexit.grid(row=10,column=6)
        self.grid_rowconfigure(11,minsize=10)

        Note.grid(row=12,column=1,sticky="w")
        self.Enote.grid(row=12,column=2,columnspan=5)
        self.grid_rowconfigure(13,minsize=20)

        Home.grid(row=14,column=1,sticky="w")
        Enter.grid(row=14,column=7,sticky="e")
    def checkdate(self,day,month,year):
        day1 = 0
        if year < 0:
            self.notice["text"] = 'Year is invalid'
            return False
        else:
            if month < 0 or month > 12:
                self.notice["text"] = 'Month is invalid'
                return False
            else:
                if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                    day1 = 31
                elif month == 4 or month == 6 or month == 9 or month == 11:
                    day1 = 30
                else:
                    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                        day1 = 28
                    else:
                        day1 = 29
                if day <= 0 or day > day1:
                    self.notice["text"] = 'Day is invalid'
                    return False
                if(year < 2022):
                    self.notice["text"] = 'today is 1/1/2022'
                    return False
        return True
    def BookedRoomList(self,client):
        dayEntry = self.dayentry.get()
        monthEntry = self.monthentry.get()
        yearEntry = self.yearentry.get()
        dayLeaving = self.dayexit.get()
        monthLeaving = self.monthexit.get()
        yearLeaving = self.yearexit.get()
        hotelID = self.name.get()
        enote = self.Enote.get()
        if(dayEntry == '' or monthEntry =='' or yearEntry =='' or dayLeaving == '' or monthLeaving == '' or yearLeaving == '' or hotelID == '' or enote == ''):
            self.notice["text"] = 'fill your information in the blank field'
            return
        else:
            self.notice["text"] = ''
        if(dayEntry.isdigit() and monthEntry.isdigit() and yearEntry.isdigit() and dayLeaving.isdigit() and monthLeaving.isdigit() and yearLeaving.isdigit()):
            self.notice["text"] = ''
        else:
            self.notice["text"] = 'Date is digit'
            return
        if(self.checkdate(int(dayEntry),int(monthEntry),int(yearEntry)) == False):
            return
        else:
            self.notice["text"] = ''
        if(self.checkdate(int(dayLeaving),int(monthLeaving),int(yearLeaving)) == False):
            return
        else:
            self.notice["text"] = ''
        global roomlist
        global bedlist
        if(len(roomlist) == 0 or len(bedlist) == 0):
            self.notice["text"] = 'please choose type of room or type of bed you want'
            return
        else:
            self.notice["text"] = ''
        roomtype = roomlist
        bedtype = bedlist
        DateEntry = [yearEntry,monthEntry,dayEntry]
        DateLeaving = [yearLeaving,monthLeaving,dayLeaving]
        if(checkDateEntryLeaving(DateEntry,DateLeaving) == False):
            self.notice["text"] = 'error cause of leaving day and arrive day'
            return
        else:
            self.notice["text"] = ""
        msg = FINDROOMBOOK
        client.sendall(msg.encode(FORMAT)) 
        client.sendall(hotelID.encode(FORMAT))
        checkhotel = client.recv(1024).decode(FORMAT)
        client.sendall(checkhotel.encode(FORMAT))
        if(checkhotel == FAILFINDROOM):
            self.notice["text"] = 'There is no hotel'
            return
        else:
            self.notice["text"] = ''
        sendList(client,DateEntry)
        client.recv(1024) 
        sendList(client,DateLeaving)
        client.recv(1024)
        sendList(client,roomtype)
        client.recv(1024)
        sendList(client,bedtype)
        client.recv(1024)
        global roomAvai
        roomAvai = app.frames[HotelInfoPage].recvListroomAvailable(client)
        app.showPage(BookRoom)
        
class HotelInfoPage(tk.Frame):
    def __init__(self,parent,app,client):
        tk.Frame.__init__(self,parent)
        self.notice = tk.Label(self,text='Fill your information in the blank field',wraplength=150,bg='bisque')
        title = tk.Label(self,text="Finding hotel avaiable room")
        DateOfEntry = tk.Label(self, text = 'Date of entry: ')
        DateOfExit = tk.Label(self,text="Date of exit: ")
        scrollbar = tk.Scrollbar(self,bg='white')
        app.hotellist= tk.Listbox(self,bg='white',selectmode=SINGLE,height =15,width =30,exportselection=False,yscrollcommand = scrollbar.set)
        slash = tk.Label(self,text="/")
        slash1 = tk.Label(self,text="/")
        slash2 = tk.Label(self,text="/")
        slash3 = tk.Label(self,text="/")

        self.dayentry = tk.Entry(self,bg = 'white',width=2)
        self.monthentry = tk.Entry(self,bg = 'white',width=2)
        self.yearentry = tk.Entry(self,bg = 'white',width=4)

        self.dayexit = tk.Entry(self,bg = 'white',width=2)
        self.monthexit = tk.Entry(self,bg = 'white',width=2)
        self.yearexit = tk.Entry(self,bg = 'white',width=4)
        self.indexHotel = None
        app.hotellist.bind('<<ListboxSelect>>', clickEventHotellist)

        Home= tk.Button(self,text="Back to \n home page",command=lambda: (app.showPage(HomePage),self.DeleteThing()))
        Enter= tk.Button(self,text="Enter",command=lambda: (changeframe(HotelInfoPage),self.show(),inputname(app.canvas,roomAvai)))
        
        title.grid(row=0,column=0,columnspan=10,sticky="we")
        self.grid_rowconfigure(1,minsize=10)
        self.grid_columnconfigure(0,minsize=10)
              
        app.hotellist.grid(row=2,column=1,rowspan = 5)
        scrollbar.grid(row=2,column=2,rowspan = 5,ipady=95)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        DateOfEntry.grid(row=3,column=4)
        DateOfExit.grid(row=4,column=4)

        self.dayentry.grid(row=3,column=5)
        self.dayexit.grid(row=4,column=5)
        slash.grid(row=3,column=6)
        slash1.grid(row=4,column=6)
                
        self.monthentry.grid(row=3,column=7)
        self.monthexit.grid(row=4,column=7)
        slash2.grid(row=3 ,column=8)
        slash3.grid(row=4,column=8)

        self.yearentry.grid(row=3,column=9)
        self.yearexit.grid(row=4,column=9)
        self.notice.grid(row=5,column=4,columnspan=6)

        self.grid_columnconfigure(10, weight = 1)
        self.grid_rowconfigure(6, weight = 1)
        

        Home.grid(row=6,column=4)
        Enter.grid(row=6,column=9)
        self.grid_rowconfigure(7, weight = 1)
    def recvListroomAvailable(self,client):
        list = []
        item = client.recv(1024).decode(FORMAT)
        while(item != "end"):
            # item = json.loads(item)
            list.append(json.loads(item))
            client.sendall(item.encode(FORMAT))
            item = client.recv(1024).decode(FORMAT)
        return list
    def DeleteThing(self):
        app.hotellist.delete(0,END)
        app.frames[HotelInfoPage].indexHotel = None
        roomAvai.clear()
    def InputHotelName(self,hotellist):
        for i in listtHotelName:
            hotellist.insert(END, "hotel " + i)
    def checkdateInfo(self,day,month,year):
        day1 = 0
        if year < 0:
            self.notice["text"] = 'Year is invalid'
            return False
        else:
            if month < 0 or month > 12:
                self.notice["text"] = 'Month is invalid'
                return False
            else:
                if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                    day1 = 31
                elif month == 4 or month == 6 or month == 9 or month == 11:
                    day1 = 30
                else:
                    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                        day1 = 28
                    else:
                        day1 = 29
                if day <= 0 or day > day1:
                    self.notice["text"] = 'Day is invalid'
                    return False
                if(year < 2022):
                    self.notice["text"] = 'today is 1/1/2022'
                    return False
        return True
    def show(self):
        Dayentry =self.dayentry.get()
        Monthentry =self.monthentry.get()
        Yearentry =self.yearentry.get()

        Dayexit =self.dayexit.get()
        Monthexit =self.monthexit.get()
        Yearexit =self.yearexit.get()

        if(Dayentry == '' or Monthentry == '' or Yearentry == '' or Dayexit == '' or Monthexit == '' or Yearexit == ''):
            self.notice["text"] = "Fill your information in the blank field"
            return
        else:
            self.notice["text"] = ""
        if(Dayentry.isdigit() and Monthentry.isdigit() and Yearentry.isdigit() and Dayexit.isdigit() and Monthexit.isdigit() and Yearexit.isdigit()):
            self.notice["text"] = ''
        else:
            self.notice["text"] = 'Date is digit'
            return
        if(self.checkdateInfo(int(Dayentry),int(Monthentry),int(Yearentry)) == False):
            return
        else:
            self.notice["text"] = ''
        if(self.checkdateInfo(int(Dayexit),int(Monthexit),int(Yearexit)) == False):
            return
        else:
            self.notice["text"] = ''
        if(self.indexHotel == None):
            self.notice["text"] = "Choose hotel you want to see information"
            return
        else:
            self.notice["text"] = ""
        listentry = [Yearentry, Monthentry, Dayentry]
        listexit = [Yearexit, Monthexit, Dayexit]
        if(checkDateEntryLeaving(listentry,listexit) == False):
            self.notice["text"] = 'error cause of leaving day and arrive day'
            return
        else:
            self.notice["text"] = ""
        msg = FINDROOM
        client.sendall(msg.encode(FORMAT)) 
        sendList(client,listentry)
        client.recv(1024) 
        sendList(client,listexit)
        client.recv(1024)
        client.sendall(str(app.frames[HotelInfoPage].indexHotel).encode(FORMAT))
        client.recv(1024)
        global roomAvai
        roomAvai = self.recvListroomAvailable(client)
        app.showPage(BookRoom) 

class SignUpPage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)
        self.label_title = tk.Label(self, text = 'Sign up')
        self.label_notice = tk.Label(self,text='')
        self.label_username = tk.Label(self, text = 'Username: ')
        self.entry_username = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticeUsername = tk.Label(self,text='')
        self.label_password = tk.Label(self, text = 'Password: ')
        self.entry_password = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticePassword = tk.Label(self,text='')
        self.label_RetypePassword = tk.Label(self, text = 'Confirm password: ')
        self.entry_RetypePassword = tk.Entry(self,bg='light yellow',width=30)
        self.label_noticeRetypePassword = tk.Label(self,text='')
        self.label_BankCode = tk.Label(self, text = 'Bank Code: ')
        self.entry_BankCode = tk.Entry(self,bg='light yellow',width=30)
        self.btn_signup = tk.Button(self,text='Sign up',command=lambda: appController.Signup(self,client))
        self.btn_backlogin = tk.Button(self,text='Back to log in',command=lambda: appController.showPage(StartPage))

        self.grid_rowconfigure(1,weight =1)
        self.grid_rowconfigure(16,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(3,weight =1)

        self.label_title.grid(row=0,column=1,columnspan=2)       

        self.label_username.grid(row=3,column=1,sticky="w")
        self.entry_username.grid(row=3,column=2,padx=10)
        self.label_noticeUsername.grid(row=4,column=1,columnspan=2)
        
        self.label_password.grid(row=6,column=1,sticky="w")
        self.entry_password.grid(row=6,column=2,padx=10)
        self.label_noticePassword.grid(row=7,column=1,columnspan=2)

        self.label_RetypePassword.grid(row=9,column=1,sticky="w")
        self.entry_RetypePassword.grid(row=9,column=2,padx=10)
        self.label_noticeRetypePassword.grid(row=10,column=1,columnspan=2)

        self.label_BankCode.grid(row=12,column=1,sticky="w")
        self.entry_BankCode.grid(row=12,column=2,padx=10)
        self.label_notice.grid(row=13,column=1,columnspan=2)
        self.grid_rowconfigure(14,minsize=10)

        self.btn_backlogin.grid(row=15,column=1,sticky="w")
        self.btn_signup.grid(row=15,column=2,sticky="e")

class HomePage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)
        appController.geometry("800x500")
        label_login = tk.Label(self,text="You have logging successfully")
        label_title = tk.Label(self, text = 'HOME PAGE')
        hotel_info = tk.Button(self,text='Find hotel information',command=lambda:(appController.showPage(HotelInfoPage), app.frames[HotelInfoPage].InputHotelName(appController.hotellist)))
        hotel_book = tk.Button(self,text='Book a room in specific hotel',command=lambda:appController.showPage(BookingPage))
        hotel_removebooking = tk.Button(self,text='Remove booked hotel room',command=lambda: (self.countTotal(),app.frames[RemoveRoom].price.config(text= "Price " + str(total)),roomBookedInfo(client),appController.showPage(RemoveRoom),inputname(app.canvas1,roomAvai)))
        btn_logout = tk.Button(self,text='Log out',command=lambda:appController.showPage(StartPage))
        label_title.grid(row=0, column=0, columnspan=3)
        label_login.grid(row=1, column=0, columnspan=3)
        self.grid_rowconfigure(2,weight=1)
        self.grid_columnconfigure(0,weight=1)

        hotel_info.grid(row=3, column=1)
        self.grid_rowconfigure(4,weight=1)

        hotel_book.grid(row=5, column=1)
        self.grid_rowconfigure(6,weight=1)

        hotel_removebooking.grid(row=7, column=1)
        self.grid_rowconfigure(8,weight=1)

        btn_logout.grid(row=9, column=1)
        self.grid_rowconfigure(10,weight=1)
        self.grid_columnconfigure(2,weight=1)
    def countTotal(self):
        if(len(acc['Booked room']) != 0):
            global total
            total = 0
            for bok in acc['Booked room']:
                total = total + bok['price']
class StartPage(tk.Frame):
    def __init__(self,parent,appController,client):
        tk.Frame.__init__(self,parent)

        self.label_title = tk.Label(self, text = 'LOGIN')
        self.label_notice = tk.Label(self,text='',bg='bisque')
        self.label_username = tk.Label(self, text = 'username')
        self.entry_username = tk.Entry(self,bg='light yellow',width=30)
        self.label_password = tk.Label(self, text = 'password')
        self.entry_password = tk.Entry(self,bg='light yellow',width=30,show="*")
        self.btn_login = tk.Button(self,text='Login',command=lambda: appController.Login(self,client))
        self.btn_signup = tk.Button(self,text='Sign up',command=lambda: appController.showPage(SignUpPage))
        
        self.grid_rowconfigure(3,weight =1)
        self.grid_rowconfigure(9,weight =1)
        self.grid_columnconfigure(0,weight =1)
        self.grid_columnconfigure(3,weight =1)

        self.label_title.grid(row=0,column=1,columnspan=2)
        self.label_notice.grid(row=1,column=1,columnspan=2)

        self.label_username.grid(row=4,column=1)
        self.entry_username.grid(row=4,column=2,padx=10)
        self.grid_rowconfigure(5,minsize=20)
        
        self.label_password.grid(row=6,column=1)
        self.entry_password.grid(row=6,column=2,padx=10)
        self.grid_rowconfigure(7,minsize=30)

        self.btn_signup.grid(row=8,column=1,sticky='w')
        self.btn_login.grid(row=8,column=2,sticky='e')

class App(tk.Tk):
    def __init__(self,client):
        tk.Tk.__init__(self)
        self.title("My app")
        self.geometry("500x300")
        self.resizable(width=False, height=False)

        container = tk.Frame()

        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        for F in (StartPage,HomePage,SignUpPage,HotelInfoPage,BookingPage,BookRoom,RemoveRoom):
            frame = F(container,self,client)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.frames[StartPage].tkraise()
    def Login(self,curFrame,client):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()

        if (username == '' or password == ''):
            curFrame.label_notice["text"] = 'failed login'
            return
        else:
            msg = LOGIN
            client.sendall(msg.encode(FORMAT))
            client.sendall(username.encode(FORMAT))
            client.recv(1024)
            client.sendall(password.encode(FORMAT))
            client.recv(1024)
            msg = client.recv(1024).decode(FORMAT)
            if msg == SUCCESS:
                ms = 'ok'
                client.sendall(msg.encode(FORMAT))
                global acc
                temp = client.recv(12000).decode(FORMAT)
                client.sendall(ms.encode(FORMAT))
                acc = json.loads(temp)
                global listtHotelName
                listtHotelName = recvListt(client)
                self.showPage(HomePage)
                global total
                total = 0
            else:
                curFrame.label_notice["text"] = INVALID
    def Signup(self,curFrame,client):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()
        BankCode = curFrame.entry_BankCode.get()
        RetypePassword = curFrame.entry_RetypePassword.get()
        if(username == '' or password == '' or RetypePassword == '' or BankCode == ''):
            curFrame.label_noticeUsername["text"] = ''
            curFrame.label_noticePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = ''
            curFrame.label_notice["text"] = 'Fill your information in the blank fields'
            return
        else:
            curFrame.label_notice["text"] = ''
        if (RetypePassword != password):
            curFrame.label_noticeUsername["text"] = ''
            curFrame.label_noticePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = 'Wrong password'
            return
        else:
            curFrame.label_noticeRetypePassword["text"] = ''
        msg = SIGNUP
        client.sendall(msg.encode(FORMAT))
        client.sendall(username.encode(FORMAT))
        client.recv(1024)
        client.sendall(password.encode(FORMAT))
        client.recv(1024)
        client.sendall(BankCode.encode(FORMAT))
        client.recv(1024)
        msg = client.recv(1024).decode(FORMAT)
        if msg == SUCCESS:
            curFrame.label_noticeUsername["text"] = ''
            curFrame.label_noticePassword["text"] = ''
            curFrame.label_noticeRetypePassword["text"] = ''
            curFrame.label_notice["text"] = 'Sign up successfully !'
        else:
            curFrame.label_notice["text"] = ''
            client.sendall(msg.encode(FORMAT))
            msg2 = client.recv(1024).decode(FORMAT)
            client.sendall(msg2.encode(FORMAT))
            msg3 = client.recv(1024).decode(FORMAT)
            client.sendall(msg3.encode(FORMAT))
            msg4 = client.recv(1024).decode(FORMAT)
            client.sendall(msg4.encode(FORMAT))
            if(msg3 == DUPLICATEUSER):
                curFrame.label_noticeUsername["text"] = 'Already has this username'
            else:
                curFrame.label_noticeUsername["text"] = ''
                if(msg == FORMATUSERNAME):
                    curFrame.label_noticeUsername["text"] = 'Username must have at least 5 character (a-z)(0-9)'
                if(msg2 == FORMATPASS):
                    curFrame.label_noticePassword["text"] = 'Password must have at least 3 character'
                else:
                    curFrame.label_noticePassword["text"] = ''
                if(msg4 == FORMATBANKCODE):
                    curFrame.label_notice["text"] = 'Bank code must have 10 digit'
                else:
                    curFrame.label_notice["text"] = ''
    def showPage(self,frameName):
        self.frames[frameName].tkraise()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")
try:
    client.connect((HOST, SERVER_PORT))
except:
    print("error")
app = App(client)
app.mainloop()


