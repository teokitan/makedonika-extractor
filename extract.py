import requests
import pdfkit
import os
import wget
import shutil

urlStart = input("Input start URL    ")
imeAcc = input("Input filename     ")
imeLat = "nNTuvlfQe0ai"
urlFull = "http://makedonika.mk/Upload/EpubExtract/" + urlStart + "/OEBPS/"

os.mkdir(imeLat)
os.mkdir(imeLat+"\\Text")
os.mkdir(imeLat+"\\Images")

urlContentOPF = urlFull + "content.opf"
urlContentNCX = urlFull + "toc.ncx"
fileNameOPF = imeLat+"\\"+'content.opf'
fileNameNCX = imeLat+"\\"+'toc.ncx'

wget.download(urlContentOPF, fileNameOPF)
wget.download(urlContentNCX, fileNameNCX)

ctr = 0

for i in range(1, 800):
    brStr = str(i)
    full = "Section"
    
    for j in range(0,4-len(brStr)):
        full += "0"
        
    full += brStr + ".xhtml"
    
    req = requests.get(urlFull+"Text/"+full)
    
    if req.status_code == 404:
        ctr += 1
        
        if ctr > 50:
            break
        
        continue
    
    wget.download(urlFull+"Text/"+full, imeLat+"\\Text\\"+full)
    
    fullXH = req.text
    fullIMG = fullXH.split("src=\"../Images/")
    
    for j in range(1,len(fullIMG)):
        ime = fullIMG[j].split(".png")[0] + ".png"
        imeURL = urlFull + "Images/" + ime
        wget.download(imeURL, imeLat+"\\Images\\"+ime)
        
shutil.make_archive(imeLat, 'zip', imeLat)
os.rename(imeLat+".zip", imeAcc+".epub")

shutil.rmtree(imeLat)