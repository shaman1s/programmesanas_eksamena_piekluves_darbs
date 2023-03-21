from tkinter import *
import math
import sqlite3
import uuid

conn = sqlite3.connect('vesture.db') 
c = conn.cursor()
# Datubāzes izveide, ja tādas nav 
c.execute('''
          CREATE TABLE IF NOT EXISTS pirma_formula
          ([ieraksta_id] TEXT, [E] TEXT, [F] TEXT, [S] TEXT, [REZ] TEXT)
          ''')
          
c.execute('''
          CREATE TABLE IF NOT EXISTS otra_formula
          ([ieraksta_id] TEXT, [E] INTEGER, [I] INTEGER, [R] INTEGER, [REZ] TEXT)
          ''')
                     
conn.commit()

# Galvenā loga izveide
window = Tk()
window.title('Fizikas apgaismojuma formulu kalkulators') # Nosaukuma piešķiršana galvenajam logam.
window.geometry("400x470") # Izmēru iestatīšana logam. 
window.resizable(False, False) 

# mainīgo deklarēšana
num1 = IntVar() 
num2 = IntVar() 
num3 = IntVar()
num4 = IntVar()
num5 = IntVar()
num6 = IntVar()

# Tekstuālās informācijas pievienošana grafiskajam logam
mainTitle = Label(window, text="Rēķinot nezināmo, neatstājiet tukšus lielumus!", font=("Courier", 10))
mainTitle.place(x=10, y=10) 

type1 = Label(window, text="E - Apgaismojums", font=("Courier", 10))
type1.place(x=10, y=30)

type2 = Label(window, text="Φ - Gaismas plūsma", font=("Courier", 10))
type2.place(x=10, y=50)

type3 = Label(window, text="S - Virsmas laukums", font=("Courier", 10))
type3.place(x=10, y=70)

resultLabel = Label(window, text="Rezultāts - ", font=("Courier", 10))
resultLabel.place(x=10, y=110)

type4 = Label(window, text="E - Apgaismojums", font=("Courier", 10))
type4.place(x=10, y=140)

type5 = Label(window, text="I - Gaism. av. stiprums", font=("Courier", 10))
type5.place(x=10, y=160)

type6 = Label(window, text="R - Gaism. av. atr. att.", font=("Courier", 10))
type6.place(x=10, y=180)


resultLabel1 = Label(window, text="Rezultāts - ", font=("Courier", 10))
resultLabel1.place(x=10, y=220)

paskaidrojums = Label(window, text="Pirmā formula  -  E=Φ/S", font=("Courier", 10))
paskaidrojums.place(x=10, y=350)
paskaidrojums2 = Label(window, text="Otrā formula  -  E=I/(R^2)", font=("Courier", 10))
paskaidrojums2.place(x=10, y=380)
paskaidrojums3 = Label(window, text="Nezināmo lielumu aizstājiet ar '0'!", font=("Courier", 10))
paskaidrojums3.place(x=10, y=410)
paskaidrojums4 = Label(window, text="Gadījumā, ja aprēķinu dotais lielums ir 0,", font=("Courier", 10))
paskaidrojums4.place(x=10, y=430)
paskaidrojums5 = Label(window, text="aprēķiniem nav fizikālās jēgas.", font=("Courier", 10))
paskaidrojums5.place(x=10, y=450)




 # funkcijas nezināmā aprēķināšanai, datu izvadei un ierakstīšanai datubāzē 
def pirma_formula():
    if num1.get()==0 and num2.get()!=0 and num3.get()!=0:
        rezultats = num2.get() / num3.get()
    elif num1.get()!=0 and num2.get()==0 and num3.get()!=0:
        rezultats = num1.get() * num3.get()
    elif num1.get()!=0 and num2.get()!=0 and num3.get()==0:
        rezultats = num2.get() / num1.get()
    else:
        rezultats = "nepareizi ievaddati" # Šis if-elif-else bloks pārbauda, kurš lielums jāaprēķina
    ieraksta_id=str(uuid.uuid4()) # identifikatora piešķiršana jaunam ierakstam datubāzē
    E = str(num1.get()) # Vērtību pielāgošana datubāzes prasītajam formātam
    F = str(num2.get())
    S = str(num3.get())
    REZ = str(rezultats)
    sql = '''INSERT INTO pirma_formula 
    VALUES(?, ?, ?, ?, ?) '''
    c.execute(sql, (ieraksta_id, E, F, S, REZ)) # vērtību ierakstīšana datubāzē
    conn.commit()
    resultEntry.delete(0, END)
    resultEntry.insert(0, str(rezultats)) # rezultāta ievietošana grafiskajā logā

def otra_formula():
    if num4.get()==0 and num5.get()!=0 and num6.get()!=0:
        rezultats = num5.get() / (num6.get()*num6.get())
    elif num4.get()!=0 and num5.get()==0 and num6.get()!=0:
        rezultats = num4.get() * num6.get() * num6.get()
    elif num4.get()!=0 and num5.get()!=0 and num6.get()==0:
        rezultats = math.sqrt( num5.get() / num4.get())
    else:
        rezultats = "nepareizi ievaddati"
    ieraksta_id=str(uuid.uuid4())
    E = str(num4.get())
    I = str(num5.get())
    R = str(num6.get())
    REZ = str(rezultats)
    sql = '''INSERT INTO otra_formula 
    VALUES(?, ?, ?, ?, ?) '''
    c.execute(sql, (ieraksta_id, E, I, R, REZ))
    conn.commit()
    resultEntry1.delete(0, END)
    resultEntry1.insert(0, str(rezultats))

def vestures_tabula(): # jauna grafiska loga izveide un datu izvads
    newWindow = Toplevel(window) # jauna loga definēšana
    newWindow.title("Vēsture pirmajai formulai")
    newWindow.geometry("400x400")
    res = c.execute("SELECT * FROM pirma_formula") # datubāzes datu izlasīšana
    vesture = res.fetchall()
    paskaidrojums_v = Label(newWindow, text="Ar komatiem atdalīti E, Φ, S un rezultāts", font=("Courier", 10))
    paskaidrojums_v.place(x=10, y=10)
    paskaidrojums_v2 = Label(newWindow, text="Ar 0 norādīts rēķināmais lielums", font=("Courier", 10))
    paskaidrojums_v2.place(x=10, y=30)
    for i in range (len(vesture)-1,-1,-1): # datu izvade grafiskajā logā
        vertiba1 = Label(newWindow, text=f"{vesture[i][1]} , {vesture[i][2]} , {vesture[i][3]} , {vesture[i][4]}", font=("Courier", 10))
        vertiba1.place(x=10, y=((len(vesture)-i)+2)*20)

def vestures_tabula2():
    newWindow2 = Toplevel(window)
    newWindow2.title("Vēsture otrajai formulai")
    newWindow2.geometry("400x400")

    res = c.execute("SELECT * FROM otra_formula")
    vesture = res.fetchall()
    paskaidrojums_v3 = Label(newWindow2, text="Ar komatiem atdalīti E, I, R un rezultāts", font=("Courier", 10))
    paskaidrojums_v3.place(x=10, y=10)
    paskaidrojums_v4 = Label(newWindow2, text="Ar 0 norādīts rēķināmais lielums", font=("Courier", 10))
    paskaidrojums_v4.place(x=10, y=30)
    for i in range (len(vesture)-1,-1,-1):
        vertiba1 = Label(newWindow2, text=f"{vesture[i][1]} , {vesture[i][2]} , {vesture[i][3]} , {vesture[i][4]}", font=("Courier", 10))
        vertiba1.place(x=10, y=((len(vesture)-i)+2)*20)
        

    

# Ievadu sintakse
entry1 = Entry(window, textvariable=num1)
entry1.place(x=200, y=30, height=20, width=143)

entry2 = Entry(window, textvariable=num2)
entry2.place(x=200, y=50, height=20, width=143)

entry3 = Entry(window, textvariable=num3)
entry3.place(x=200, y=70, height=20, width=143)

entry4 = Entry(window, textvariable=num4)
entry4.place(x=200, y=140, height=20, width=143)

entry5 = Entry(window, textvariable=num5)
entry5.place(x=200, y=160, height=20, width=143)

entry6 = Entry(window, textvariable=num6)
entry6.place(x=200, y=180, height=20, width=143)

resultEntry = Entry(window, bg = "orange")
resultEntry.place(x=200, y=110, height=20, width=143)

resultEntry1 = Entry(window, bg = "orange")
resultEntry1.place(x=200, y=220, height=20, width=143)

# Pogu sintakse
button_1f = Button(window, text="Aprēķināt nezināmo", fg="black", font=("Courier", 10), command=pirma_formula) # Use command to call the functions.
button_1f.place(x=10, y=90, height=20, width=150)

button_2f = Button(window, text="Aprēķināt nezināmo", fg="black", font=("Courier", 10), command=otra_formula) # Use command to call the functions.
button_2f.place(x=10, y=200, height=20, width=150)

button_vest = Button(window, text="Pirmās formulas vēsture", fg="black", font=("Courier", 10), command=vestures_tabula)
button_vest.place(x=10, y=250, height=20, width=200)

button_vest2 = Button(window, text="Otrās formulas vēsture", fg="black", font=("Courier", 10), command=vestures_tabula2)
button_vest2.place(x=10, y=290, height=20, width=200)



window.mainloop() # Cikls, kas uztur grafisko logu
