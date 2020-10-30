from random import sample
from random import randint
from alpha import alpha
from alpha import symbs
from flask import *
import os
from bs4 import BeautifulSoup as bs
import requests

#JINJA2
# <div id='info_section'>
#     {% for data in data %}
#         <p>{{ data }}</p>
#     {% endfor %}
# </div>

#GENERATING PASSPHRASE
def pphrase(inp):
    c=inp.count(' ')
    print(c)
    for _ in range(randint(1,c)):
        symb=sample(symbs,1)
        symb=''.join(symb)
        inp = inp.replace(' ', symb, 1)
    inp=inp.replace(' ','')
    return inp

#GENERATING PASSWORD
def generate(input):
    inp=input.lower()
    phl=inp.split(' ')
    first=[]
    passwd=""
    for i in phl:
        if i:
            first.append(i.strip('."-\'')[0])
    for i in first:
        passwd+=sample(alpha[i],1)[0]
    return passwd

#SCRAPING PHRASE
def getphrase():
    loop=1
    while(loop):
        link='https://www.phrases.com/random.php'
        page=requests.get(link)
        soup=bs(page.content,'html.parser')
        name=soup.find('p',class_="example")
        ph=name.get_text().strip('."-\'‘—')
        phl=ph.split(' ')
        first=[]
        for i in phl:
            if i:
                first.append(i[0])
        if(len(first)>=10 and len(first)<=15):
            loop=0
    return ph

#SCRAPING FOR STRENGTH
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def haslower(inputString):
    return any(char.islower() for char in inputString)

def hasupper(inputString):
    return any(char.isupper() for char in inputString)

def hasspecial(inputString):
    return any(char in '`~!@#$%^&*()-_=;:\'",<.>?\\/' for char in inputString)

def getstr(inp):
    url='http://passwordstrengthcalculator.com/index.php'

    data=dict()
    data['plength']=str(len(inp))
    data['calcbutton']='Calculate'

    if(hasNumbers(inp)):
        data['decimal']='yes'
    
    if(haslower(inp)):
        data['lowercase']='yes'
    
    if(hasupper(inp)):
        data['uppercase']='yes'

    if(hasspecial(inp)):    
        data['specialchar']='yes'
        data['additionalspecialchar']='yes'
    
    page=requests.post(url, data)
    soup=bs(page.content,'html.parser')
    
    scomp=soup.find('div',class_='superbox').text.split("\n")
    scomp=[i for i in scomp if(i and i!=' ')]
    scomp=" ".join(scomp)

    pcomp=soup.find('div',class_='pcbox').text.split("\n")
    pcomp=[i for i in pcomp if(i and i!=' ')]
    pcomp=" ".join(pcomp)

    return (scomp,pcomp)


# W E B    A P P
app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True


@app.errorhandler(404) 
def not_found(e): 
	return render_template("404.html")


@app.route('/', methods=['GET','POST'])
def home():
    if (request.method == 'GET'):
        return(render_template('index.html', phrase="phrase", passwd="PassPhrase", sc="Time Super Computer takes to crack the password : 0s", pc="Time a Computer with GPU takes to crack the password : 0s"))
    
    elif (request.method == 'POST'):
        ph=getphrase()

        if('pph' in dict(request.form)):
            pwd=pphrase(ph)
            sc='A Super Computer cannot crack it'
            pc='A PC with GPU cannot crack it'
        else:
            pwd=generate(ph)
            sc,pc=getstr(pwd)
        
        return(render_template('index.html', phrase=ph, passwd=pwd, sc=sc, pc=pc))


@app.route('/about', methods=['GET','POST'])
def page1():
	if (request.method == 'GET'):
		return(render_template('about.html'))


app.run(port='8000')

