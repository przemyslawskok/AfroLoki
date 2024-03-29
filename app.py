from flask import Flask,render_template,session,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
import shutil
import dane







app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posty.sqlite3'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'asdas978er32nkj4h2n9 dfjkdsf hoi21kl3m,.'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=1)



db = SQLAlchemy(app)





class licznik_strony():
   licznik=0
   def __init__(self):
      file=open("ilosc_wejsc.txt","r+")
      self.licznik=int(file.read())
      file.close()
   def dodaj_wejscie(self):
      self.licznik=self.licznik+1
      file=open("ilosc_wejsc.txt","w+")
      file.write(str(self.licznik))
      file.close()

ilosc_wejsc=licznik_strony()


class test():
   bledne=False

logowanie=test()





def uzytkownik_zalogowany():
   try:
      test=session['sjnsda8i3j2k4a,mSDAlk*@nb2']
      return True
   except:
      return False





class posty(db.Model):
   post_id = db.Column('post_id', db.Integer, primary_key = True)
   zdjecia = db.Column(db.String(200))
   opis = db.Column(db.String(500))


   def __init__(self, zdjecia, opis):
      self.zdjecia = zdjecia
      self.opis = opis

class ceny(db.Model):
   cena_id = db.Column('cena_id', db.Integer, primary_key = True)
   cena = db.Column(db.Integer())
   tytul = db.Column(db.String(100))
   opis = db.Column(db.String(500))
   czy_cena_zmienna = db.Column(db.String(100))



   def __init__(self,cena,tytul,opis,czy_cena_zmienna):
      self.cena = cena
      self.tytul = tytul
      self.opis = opis
      self.czy_cena_zmienna = czy_cena_zmienna

   

db.create_all()

@app.route('/')
def glowna():
   ilosc_wejsc.dodaj_wejscie()
   rekordy=posty.query.order_by(posty.post_id.desc()).all()
   slownik={}
    
   for rekord in rekordy:
      napis=rekord.zdjecia
      tablica=napis.split('~')
      for zdjecie in tablica:
         


         if str(zdjecie)=="":
            tablica.remove(zdjecie)


      slownik[rekord.post_id]=[tablica,rekord.opis]
         

   rekordy=ceny.query.order_by(ceny.cena_id).all()
   lista=[]
   for rekord in rekordy:
         lista.append([rekord.cena_id,rekord.cena,rekord.tytul,rekord.opis,rekord.czy_cena_zmienna])
      



   return render_template("/glowna.html",
   slownik=slownik,
   lista=lista,
   liczba_postow=str(len(rekordy)))


@app.route('/panel')
def panel():
   if uzytkownik_zalogowany():
      
      rekordy=posty.query.order_by(posty.post_id.desc()).all()
      slownik={}
    
      for rekord in rekordy:
         napis=rekord.zdjecia
         tablica=napis.split('~')
         for zdjecie in tablica:
           


            if str(zdjecie)=="":
               tablica.remove(zdjecie)


         slownik[rekord.post_id]=[tablica,rekord.opis]
         







      rekordy=ceny.query.order_by(ceny.cena_id.desc()).all()
      lista=[]
    
      for rekord in rekordy:
         lista.append([rekord.cena_id,rekord.cena,rekord.tytul,rekord.opis,rekord.czy_cena_zmienna])

         
 
      return render_template("/panel.html",
      slownik=slownik,
      lista=lista,
      wejscia=ilosc_wejsc.licznik,
      liczba_postow=str(len(rekordy)))
   else:
      return redirect("/panel_logowanie")


@app.route('/dodaj_usluge',methods=["POST"])
def dodaj_usluge():
   if uzytkownik_zalogowany():
      cena=request.form['cena']
      tytul=request.form['tytul']
      opis=request.form['opis']
      czy_cena_zmienna=request.form.getlist('czy_cena_zmienna')
      if czy_cena_zmienna==[]:
         czy_cena_zmienna="NIE"
      else:
         czy_cena_zmienna=czy_cena_zmienna[0]
      

      rekord=ceny(str(cena),str(tytul),str(opis),str(czy_cena_zmienna))
      db.session.add(rekord)
      db.session.commit()
      return redirect("/panel")


@app.route('/zaktualizuj_ceny',methods=["POST"])
def zaktualizuj_ceny():
   if uzytkownik_zalogowany():

      rekordy=ceny.query.order_by(ceny.cena_id.desc()).all()
      try:
         for n in range(1,int(rekordy[0].cena_id)+2):
            print(n)
            try:
               cena=request.form['cena'+str(n)]
               tytul=request.form['tytul'+str(n)]
               opis=request.form['opis'+str(n)]
               czy_cena_zmienna=request.form.getlist('czy_cena_zmienna'+str(n))
               if czy_cena_zmienna==[]:
                  czy_cena_zmienna="NIE"
               else:
                  czy_cena_zmienna=czy_cena_zmienna[0]
               for rekord in rekordy:
                  if rekord.cena_id==n:
                     rekord.cena=cena
                     rekord.tytul=tytul
                     rekord.opis=opis
                     rekord.czy_cena_zmienna=czy_cena_zmienna
                     
                     db.session.commit()
            except:
               print("Nie znaleziono rekordu o id "+str(n))
      except:
         print("Nie ma rekordów")

      # cena_1=request.form.get("cena_1")
      # cena_2=request.form.get("cena_2")
      # cena_3=request.form.get("cena_3")

      # print(rekordy)
      # for rekord in rekordy:
      #    if rekord.cena_id==3:
      #       rekord.cena=int(cena_3)
      #       db.session.commit()
      #    if rekord.cena_id==2:
      #       rekord.cena=int(cena_2)
      #       db.session.commit()
      #    if rekord.cena_id==1:
      #       rekord.cena=int(cena_1)
      #       db.session.commit()



      return redirect("/panel")
@app.route('/dodaj_post',methods=["POST"])
def dodaj_post():
   if uzytkownik_zalogowany():

      posortowane=posty.query.order_by(posty.post_id.desc()).all()
      ostatnie_id=0
      for post in posortowane:
         ostatnie_id=int(post.post_id)
         break
     

      aktualne_id=ostatnie_id+1
      try:
         os.mkdir("static/posty/post"+str(aktualne_id))
      except:
         print()
      zdjecia=request.files.getlist("zdjecia")
      opis=request.form.get("opis")
      zdjecia_ids=[]
      for zdjecie in zdjecia:

         file=open("licznik.txt","r+")
         licznik=int(file.read())
         file.close()

         zdjecie.save(str("static/posty/post"+str(aktualne_id)+"/zdjecie"+str(licznik)+".jpg"))
         zdjecia_ids.append(licznik)

         file=open("licznik.txt","w+")
         file.write(str(licznik+1))
         file.close()
      napis=""
      for id in zdjecia_ids:
         napis+=str(id)+"~"



      rekord=posty(zdjecia=napis,opis=str(opis))
      db.session.add(rekord)
      db.session.commit()


      return redirect("/panel")
      
   else:
      return redirect("/login")

@app.route('/usun_post',methods=["POST"])
def usun_post_post():
   if uzytkownik_zalogowany():
      post_id=request.form.get("id")
      



      posty.query.filter_by(post_id=post_id).delete()
      db.session.commit()

      shutil.rmtree("static/posty/post"+str(post_id))




      return redirect ("/panel")
   else:
      return redirect ("/panel")

@app.route('/usun_usluge_<id>')
def usun_usluge(id):
   print(id)
   ceny.query.filter_by(cena_id=id).delete()
   db.session.commit()
   return redirect("/panel")










@app.route('/login')
def login():
   if uzytkownik_zalogowany():
      return redirect("/panel")
   else:
      if logowanie.bledne:
         logowanie.bledne=False
         return render_template("panel_zle.html")
      else:

         return render_template("panel_logowanie.html")



@app.route("/zaloguj_sie_postownik",methods=["POST"])
def zaloguj_sie_postowink():
   login=request.form['login']
   password=request.form['password']
   
   password=str(password)
   login=str(login)
   if login==dane.ADMIN_LOGIN and password==dane.ADMIN_PASSWORD:
      session['sjnsda8i3j2k4a,mSDAlk*@nb2']="87ashknm2afm,cxvnxc"
      return redirect("/panel")
   else:
      logowanie.bledne=True
      return redirect('/login')
   






if __name__ == '__main__':
    
    app.run('0.0.0.0',port=230,debug=True)






