def Scrap():
    def notifyme(title,message):
        plyer.notification.notify(
            title= title,
            message= message,
            app_icon='vv.ico',
            timeout=20
        )

    url= "https://www.worldometers.info/coronavirus/"
    r=requests.get(url) #scrapping the data
    soup=BeautifulSoup(r.content,'html.parser') #html.parser for converting data into html
    tablebody=soup.find('tbody') #one tabel so we use find if more then one table we will use find all
    tt=tablebody.find_all('tr') # to find all tr content from body
    notifycountry = countrydata.get()
    if (notifycountry == ''): #if notify country is null means nothing u r searching it will automatically give the data of India or default
        notifycountry= 'india'

    countries, total_case, new_case, total_deaths, new_deaths, total_recovered, active_case=[], [], [], [], [], [], []
    serious, toatlcases_permillion, totaldeths_permillion, totaltests,totaltests_permillion =[], [], [], [], []
    headers=['countries', 'total_case', 'new_case', 'total_deaths', 'new_deaths', 'total_recovered', 'active_case',
             'serious', 'totalcases_permillion', 'totaldeaths_permillion','totaltsts', 'totaltests_permillion']
    for i in tt:
        id= i.find_all('td')#to grab td data
        if (id[1].text.strip().lower() == notifycountry):
            totalcases1 = int(id[2].text.strip().replace(',', ''))
            totaldeaths1 = id[4].text.strip()
            newcases1 = id[3].text.strip()
            newdeaths1 = id[5].text.strip()


            notifyme('Corona Virus Details In {}'.format(notifycountry),
                     'Total Cases : {}\nTotal Deaths : {}\nNew Cases : {}\nNew Deaths : {}'.format(totalcases1,
                                                                                                   totaldeaths1,
                                                                                                   newcases1,
                                                                                                   newdeaths1))
        countries.append(id[1].text.strip())
        total_case.append(int(id[2].text.strip().replace(',','')))
        new_case.append(id[3].text.strip())
        new_deaths.append(id[4].text.strip())
        total_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_case.append(id[7].text.strip())
        serious.append(id[8].text.strip())
        toatlcases_permillion.append(id[9].text.strip())
        totaldeths_permillion.append(id[10].text.strip())
        totaltests.append(id[11].text.strip())
        totaltests_permillion.append(id[12].text.strip())
    df=pd.DataFrame(list(zip( countries, total_case, new_case, total_deaths, new_deaths, total_recovered, active_case,serious, toatlcases_permillion, totaldeths_permillion, totaltests,totaltests_permillion)),columns=headers)
    sor = df.sort_values('total_case', ascending=False)
    for k in formatlist:
        if(k=='html'):
            path2='{}/alldata.html'.format(path)
            sor.to_html(r'{}'.format(path2))
        if (k == 'json'):
            path2 = '{}/alldata.json'.format(path)
            sor.to_json(r'{}'.format(path2))
        if (k == 'csv'):
            path2 = '{}/alldata.csv'.format(path)
            sor.to_csv(r'{}'.format(path2))

    if(len(formatlist)!=0):
        messagebox.showinfo("Notification", 'Corona Record Is Saved{}'.format(path2),parent=root)


def download():
    global path
    if(len(formatlist)!=0):
        path=filedialog.askdirectory()
    else:
        pass
    Scrap()
    formatlist.clear()
    InHtml.configure(state='normal')
    InJson.configure(state='normal')
    InCsv.configure(state='normal')

#creating function to make button diabel
def inhtml():
    formatlist.append('html')
    InHtml.configure(state='disabled')

def incsv():
    formatlist.append('csv')
    InCsv.configure(state='disabled')

def injson():
    formatlist.append('json')
    InJson.configure(state='disabled')

import plyer # for the use of notifier
import requests #to get html data
from bs4 import BeautifulSoup #for formatting the data
import pandas as pd
from tkinter import *
from tkinter import  messagebox,filedialog
root= Tk()
root.title("Covid-19 Update")#giving the title of project
root.geometry("530x300+200+80") #setting the dimenssion(200+80 means to fix the screen at particular position)
root.configure(bg="plum2")#setting the background color
root.iconbitmap("vv.ico")#setting the icon
formatlist = []
path= '' #to store data
#creating Labels
IntroLabel1 =Label(root,text="Corona Virus Data",font=('new roman',30,'italic bold'),bg='red',width=22)# setting the font and color size and all
IntroLabel1.place(x=0,y=0)#setting the dimenssion

EntryLabel1=Label(root,text="Notify Country:",font=('arial',20,'italic bold'),bg='plum2')#setting entry label
EntryLabel1.place(x=10,y=70)#setting the dimenssion

FormatLabel=Label(root,text="Download In:",font=('arial',20,'italic bold'),bg='plum2')#setting entry label
FormatLabel.place(x=10,y=150)#setting the dimenssion
countrydata = StringVar()
ent1= Entry(root,textvariable=countrydata,font=('arial',20,'italic bold'),relief=RIDGE,bd=2,width=20)#entry box
ent1.place(x=220,y=70)#entry position

#creating Button
InHtml=Button(root,text="HTML",bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground="blue",activeforeground="white",bd=5,width=5,command=inhtml) #HTML Button creted
InHtml.place(x=210,y=150)

InJson=Button(root,text="JSON",bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground="blue",activeforeground="white",bd=5,width=5,command=injson) #Json Button creted
InJson.place(x=320,y=150)

InCsv=Button(root,text="CSV",bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground="blue",activeforeground="white",bd=5,width=5,command=incsv) #CSV Button creted
InCsv.place(x=430,y=150)

Submit=Button(root,text="Submit",bg='red',font=('arial',15,'italic bold'),relief=RIDGE,activebackground="blue",activeforeground="white",bd=5,width=25,command=download) #submit Button creted
Submit.place(x=110,y=250)

root.mainloop()