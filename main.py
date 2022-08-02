from tkinter import *
from tkinter.ttk import Frame, Notebook, Combobox, Radiobutton
import urllib.request
import xml.dom.minidom
import datetime
from datetime import timedelta
import matplotlib
import matplotlib.pyplot as plt

day = datetime.date.today().strftime('%d/%m/%Y')
response = urllib.request.urlopen(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}")
dom = xml.dom.minidom.parse(response)
dom.normalize()
name=[]
value=[]
week=[]
month=[]
quarter=[]
year=[]

#Getting date
a = datetime.date.today()
for i in range(5):
    b = (a - timedelta(days = 6))
    week.append(f"{b.strftime('%d.%m.%Y')} - {a.strftime('%d.%m.%Y')}")
    a = (b - timedelta(days = 1))
    
a = datetime.date.today() - timedelta(days=3)
for i in range(5):
    if a.month<2:
        b = datetime.date(a.year-1, 12, a.day)
    else:
        b = datetime.date(a.year, a.month, a.day)
    month.append(f"{b.strftime('%d.%m.%Y')} - {a.strftime('%d.%m.%Y')}")
    a = b

a = datetime.date.today() - timedelta(days=3)
for i in range(5):
    if a.month<4:
        b = datetime.date(a.year-1, 9+a.month, a.day)
    else:
        b = datetime.date(a.year, a.month-3, a.day)
    quarter.append(f"{b.strftime('%d.%m.%Y')} - {a.strftime('%d.%m.%Y')}")
    a = b

a = datetime.date.today()
for i in range(5):
    b = datetime.date(a.year-1, a.month, a.day)
    year.append(f"{b.strftime('%d.%m.%Y')} - {a.strftime('%d.%m.%Y')}")
    a = b

#Parcing XML page from Central Bank of Russia
elem_1 = dom.getElementsByTagName("Valute")
for i in elem_1:
    name_1 = i.getElementsByTagName("Name")[0]
    name.append(name_1.childNodes[0].data)
    value_1 = i.getElementsByTagName("Value")[0]
    nominal_1 = i.getElementsByTagName("Nominal")[0]
    value.append(float(value_1.childNodes[0].data.replace(",", "."))/float(nominal_1.childNodes[0].data.replace(",",".")))
name.append("Рубль")
value.append(float(1))

#Fuction for convert:
def button_click():
    for i in range (len(name)):
        if (name[i] == combobox_1.get()):
            combobox_1_index = i
        if (name[i] == combobox_2.get()):
            combobox_2_index = i
    label["text"]=(value[combobox_1_index]*float(enter_1.get())/value[combobox_2_index])

# Function buttons
def period():
    if r_state.get()==1:
        combobox_4.grid(row=1, column=2, padx = 10)
        combobox_4["values"]=week
    elif r_state.get()==2:
        combobox_4.grid(row=2, column=2, padx = 10)
        combobox_4["values"]=month
    elif r_state.get()==3:
        combobox_4.grid(row=3, column=2, padx = 10)
        combobox_4["values"]=quarter
    elif r_state.get()==4:
        combobox_4.grid(row=4, column=2, padx = 10)
        combobox_4["values"]=year

#Function drawing graph
def draw():
    matplotlib.pyplot.clf()
    day_1=[1, 2, 3]
    day_2=[1, 2, 3]
    day=combobox_4.get()
    day_1[2]=int(day[0]+day[1])
    day_1[1]=int(day[3]+day[4])
    day_1[0]=int(day[6]+day[7]+day[8]+day[9])
    y1 = datetime.date(day_1[0], day_1[1], day_1[2])
    days = []
    tag = []
    y = []
    if r_state.get()==1:
        delta_1 = 1
        delta_2 = 7
    elif r_state.get()==2:
        delta_1 = 3
        delta_2 = 9
    elif r_state.get()==3:
        delta_1 = 9
        delta_2 = 9
    elif r_state.get()==4:
        delta_1 = 30
        delta_2 = 12
    for i in range(delta_2):
        days.append((y1+timedelta(days = delta_1*i)).strftime('%d/%m/%Y'))
    for i in range(delta_2):
        response = urllib.request.urlopen(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={days[i]}")
        tag = getting(tag, response)
    for i in days:
        y.append( i[:2])
    if r_state.get()==1:                  
        plt.plot(y, tag)
    elif r_state.get()==2:
        plt.plot(y, tag)
    elif r_state.get()==3:
        plt.plot(y, tag)
    elif r_state.get()==4:
        plt.plot(["май", "июнь", "июль", "авг", "сен", "окт", "ноя", "дек", "янв", "фев", "март", "апр"], tag)
    canvas.draw()
    
# Function getting values
def getting(tag, response):
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    elem_1 = dom.getElementsByTagName("Valute")
    for i in elem_1:
        a = i.getElementsByTagName("Name")[0]
        if a.childNodes[0].data == combobox_3.get():
            b = i.getElementsByTagName("Value")[0]
            c = i.getElementsByTagName("Nominal")[0]
            tag.append(float(b.childNodes[0].data.replace(',', '.'))/float(c.childNodes[0].data))
    return (tag)
        
    
    

app = Tk()
app.title("Конвертер валют")
app.geometry("720x480")


tabs = Notebook(app)
tab_1 = Frame(tabs)
tab_2 = Frame(tabs)
tabs.add(tab_1, text="Калькулятор валют")
tabs.add(tab_2, text="Динамика курса")
tabs.pack(expand = True, fill = BOTH)

######## FIRST PART

combobox_1 = Combobox(tab_1)
combobox_2 = Combobox(tab_1)
combobox_1["values"]=name
combobox_2["values"]=name
combobox_1.grid(row=0, column=0, padx = 10, pady = 15)
combobox_2.grid(row=1, column=0, padx = 10, pady = 15)


enter_1 = Entry(tab_1)
enter_1.grid(row=0, column=1, padx=10, pady=15)
enter_1.focus()


button_1 = Button(tab_1, text="Конвертировать", command =
button_click)
button_1.grid(row=0, column=3, padx=10, pady=15)


label = Label(tab_1)
label.grid(row=1, column=1, padx=10, pady=15)

#Создание элементов второй вкладки:

#Поля с текстом
text_1 = Label(tab_2, text = "Валюта")
text_2 = Label(tab_2, text = "Период")
text_3 = Label(tab_2, text = "Выбор периода")
text_1.grid(row=0, column=0, padx=10, pady=15)
text_2.grid(row=0, column=1, padx=10, pady=15)
text_3.grid(row=0, column=2, padx=10, pady=15)

#########   Button draw Graph
button_2 = Button(tab_2, text="Построить график", command = draw)
button_2.grid(row=4, column=0, padx=10, pady=15)

#Listing
combobox_3 = Combobox(tab_2)
combobox_4 = Combobox(tab_2)
combobox_3["values"]=name
combobox_3.grid(row=1, column=0, padx = 10)

#Button with dates
r_state = IntVar()
radiobutton_1 = Radiobutton(tab_2, text = "Неделя", value = 1, variable = r_state, command = period)
radiobutton_2 = Radiobutton(tab_2, text = "Месяц", value = 2, variable = r_state, command = period)
radiobutton_3 = Radiobutton(tab_2, text = "Квартал", value = 3, variable = r_state, command = period)
radiobutton_4 = Radiobutton(tab_2, text = "Год", value = 4, variable = r_state, command = period)
radiobutton_1.grid(row=1, column=1, padx = 10)
radiobutton_2.grid(row=2, column=1, padx = 10)
radiobutton_3.grid(row=3, column=1, padx = 10)
radiobutton_4.grid(row=4, column=1, padx = 10)

#Graph
matplotlib.use("TkAgg")
fig = plt.figure()
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab_2)
plot_widget = canvas.get_tk_widget()
plt.grid()
plot_widget.grid(row=5, column=3)



app.mainloop()
