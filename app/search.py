# -*- coding: utf8 -*-
from app import models, app, db

words = ["Unal","Medellin","UdeA","Universidad","EAFIT","UPB"]

def searchFor(b):
    ret ="Lo sentimos, no se encontraron resultados"
    found = False
    for u in db.session.query(models.OtherName).filter(models.OtherName.name.ilike('%'+b+'%')):
        #ret = "<span>"+str(u.name)+" - "+(u.university.name).encode('utf-8')+"</span><br/>"
        return u.university
        found = True
    if(not found):
        #opciones = [[0 for x in range(2)] for x in range(10)]
        options = []
        i = 0
        for word in words:
            d = levenshteinDistance(word.lower(),b.lower())
            if(d<5):
                #opciones[i][0] = word
                #opciones[i][1] = d
                options.append((word,d))
                i += 1
        ret = "Quizás quiso decir: "
        options.sort(key=lambda times: times [1])
        for l in range(i):
            #ret += "Word = "+opciones[l][0]+" d= "+ str(opciones[l][1])+"<br>"
            if (l==0):
                ret += "<a href='/buscar/"+options.__getitem__(l)[0]+"'>"+options.__getitem__(l)[0]+"</a>"
            if(l-1 >= 0):
                if (options.__getitem__(l)[1] == options.__getitem__(l-1)[1]):
                    ret += " o <a href='/buscar/"+options.__getitem__(l)[0]+"'>"+options.__getitem__(l)[0]+"</a>"
                else:
                    break
    return ret

def levenshteinDistance(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]