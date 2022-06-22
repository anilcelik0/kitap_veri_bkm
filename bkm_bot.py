from PIL import Image
from bs4 import BeautifulSoup
import requests  
import sqlite3

vt = sqlite3.connect("bkm.sqlite3")
fvt = vt.cursor()

page=1

while page<333:
    url = requests.get("https://www.bkmkitap.com/edebiyat-kitaplari?pg="+str(page))
    soup = BeautifulSoup(url.content, "html.parser")

    books_part = soup.find_all(class_="col col-3 col-md-4 col-sm-6 col-xs-6 p-right mb productItem zoom ease")
    
    for book in books_part:
        img_url = book.find(class_="stImage")["data-src"]
        try:
            yazar = book.find(id="productModelText").string
            yazar = yazar.replace("?","soru").replace(":","ikinokta").replace("/","slash") # Dosya oluştururken kullanamayacağımız bağızı karakterler
        except:
            yazar = "bulunamadı"
            
        isim = book.find(class_="fl col-12 text-description detailLink").string
        isim_url = book.find(class_="fl col-12 text-description detailLink")["href"]
        isim = isim.replace("?","soru").replace(":","ikinokta").replace("/","slash") # Dosya oluştururken kullanamayacağımız bağızı karakterler
        
        try:
            type=soup.find(class_="col cilt col-12").find("div").find_all("span")
            type = type[1].text
        except:
            type = "bulunamadı"
            
        try:
            contents = soup.find(id="productDetailTab").find("div").find_all("p")
            content=""
            for a in contents:
                content += str(a.text)
        except:
            content = "bulunamadı"

        try:
            img = Image.open(requests.get(img_url,stream=True).raw)
            img_name = isim+"_"+yazar+".jpg"
            img_name = "resimler/"+img_name.replace("\n","")
            img.save(img_name)
        except:
            img_name = "bulunamadı"
            url = requests.get("https://www.bkmkitap.com"+isim_url)
            soup = BeautifulSoup(url.content, "html.parser")
            
            #veritabanı kayıt
            fvt.execute("INSERT INTO kitap (name,yazar,type,content,img_url) VALUES (?,?,?,?,?)",(isim,yazar,type,content,"bulunamadı"))
            vt.commit()
            

    print(page)
    page+=1
        