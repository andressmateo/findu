# -*- coding: utf8 -*-
from app import models, app, db

def search_for(b):
    ret = []
    found = False
    for u in db.session.query(models.OtherName).filter(models.OtherName.name.ilike(b+"%")):
        ret.append(u.university)
        found = True

    if (not found):
        for c in db.session.query(models.Career).filter(models.Career.name.ilike(b+"%")):
            ret.append(c)
            found = True

    if(not found):
        options = []
        words = []
        i = 0
        ret.append(0)
        for n in db.session.query(models.OtherName).all():
            words.append(n.name)
        for n in db.session.query(models.Career).all():
            words.append(n.name)
        for word in words:
            d = levenshtein_distance(word.lower(),b.lower())
            if(d<5):
                options.append((word,d))
                i += 1
        options.sort(key=lambda times: times [1])
        for l in range(i):
            found = True
            if (l==0):
                #ret += "<a href='/buscar/"+options.__getitem__(l)[0]+"'>"+options.__getitem__(l)[0]+"</a>"
                ret.append(options.__getitem__(l)[0])
            if(l-1 >= 0):
                if (options.__getitem__(l)[1] == options.__getitem__(l-1)[1]):
                    #ret += " o <a href='/buscar/"+options.__getitem__(l)[0]+"'>"+options.__getitem__(l)[0]+"</a>"
                    ret.append(options.__getitem__(l)[0])
                else:
                    break
    if (not found):
        ret.__delitem__(0)
        ret.append(-1)
    return ret

def levenshtein_distance(str1, str2):
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