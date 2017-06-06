import requests
from bs4.element import Tag
import pymysql

conn= pymysql.connect(
        host='databda.ddns.net',
        port = 3306,
        user='root',
        passwd='iiibda',
        db ='chenyu',
        charset='utf8',
        )     

cur = conn.cursor()


id=[]
i=0
cur.execute("SELECT id FROM stocklist WHERE id NOT in (SELECT DISTINCT id FROM stockprice)")
for row in cur.fetchall():
    id.append(row[0])
#i+=1

import time
#dd/mm/yyyy format
today = time.strftime("%Y/%m/%d")
#print (time.strftime("%d/%m/%Y"))

value=[]
for i in id:
    post_field ={'ctl00$ContentPlaceHolder1$startText': "2010/01/01",'ctl00$ContentPlaceHolder1$endText':today, 'ctl00$ContentPlaceHolder1$submitBut': '查詢','code':i,'pageTypeHidden':'3' }
    for error in range(5):
        try:
            r = requests.post("http://www.cnyes.com/twstock/ps_historyprice/"+i+".htm", post_field)
            break;
        except Exception as e:
            continue;
    #print(r.text)
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text.encode("utf-8"))
    html = soup.findAll('tr')
    
    for h in html:
        if isinstance(h.find('td',{'class','cr'}), Tag):
            #print(h.string)
            try:
                value = h.findAll('td',{'class','rt'})
                date = h.find('td',{'class','cr'}).string
                open = value[0].string
                high = value[1].string
                low = value[2].string
                price = value[3].string
                change = value[4].string
                ratio = value[5].string.replace("%","")
                quentity = value[6].string.replace(",","")
                
                print("INSERT IGNORE INTO stockprice (id,date,open,highest,lowest,close,price_change,ratio,quantity) VALUES ('"+i+"','"+date+"','"+open+"','"+high+"','"+low+"','"+price+"','"+change+"','"+ratio+"','"+quentity+"')")
                cur.execute("INSERT IGNORE INTO stockprice (id,date,open,highest,lowest,close,price_change,ratio,quantity) VALUES ('"+i+"','"+date+"','"+open+"','"+high+"','"+low+"','"+price+"','"+change+"','"+ratio+"','"+quentity+"')")
            except Exception as e:
                break
            
             #print(date+","+price)
         #else:
             #print(h.string)
         #except Exception as e:
             #date = ""
    
    print(i + " finish")

