from flask import Flask,render_template,session,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
import shutil








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
         print(rekord,zdjecie)


         if str(zdjecie)=="":
            tablica.remove(zdjecie)


      slownik[rekord.post_id]=[tablica,rekord.opis]
         





   return render_template("/glowna.html",
   slownik=slownik,
   liczba_postow=str(len(rekordy)))


@app.route('/dodaj_post')
def dodaj_post():
   if uzytkownik_zalogowany():
   
      rekordy=posty.query.order_by(posty.post_id.desc()).all()
      slownik={}
    
      for rekord in rekordy:
         napis=rekord.zdjecia
         tablica=napis.split('~')
         for zdjecie in tablica:
            print(rekord,zdjecie)


            if str(zdjecie)=="":
               tablica.remove(zdjecie)


         slownik[rekord.post_id]=[tablica,rekord.opis]
         






      return render_template("/dodaj_post.html",
      slownik=slownik,
      wejscia=ilosc_wejsc.licznik,
      liczba_postow=str(len(rekordy)))
   else:
      return redirect("/dodaj_post_logowanie")



@app.route('/dodaj_post',methods=["POST"])
def dodaj_post_post():
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


      return redirect("/dodaj_post")
      
   else:
      return redirect("/dodaj_post_logowanie")

@app.route('/usun_post',methods=["POST"])
def usun_post_post():
   if uzytkownik_zalogowany():
      post_id=request.form.get("id")
      



      posty.query.filter_by(post_id=post_id).delete()
      db.session.commit()

      shutil.rmtree("static/posty/post"+str(post_id))




      return redirect ("/dodaj_post")
   else:
      return redirect ("/dodaj_post")













@app.route('/dodaj_post_logowanie')
def dodaj_post_logowanie():
   if uzytkownik_zalogowany():
      return redirect("/dodaj_post")
   else:
      if logowanie.bledne:
         logowanie.bledne=False
         return render_template("dodaj_post_zle.html")
      else:

         return render_template("dodaj_post_logowanie.html")



@app.route("/zaloguj_sie_postownik",methods=["POST"])
def zaloguj_sie_postowink():
   login=request.form['login']
   password=request.form['password']
   print(password,login)
   password=str(password)
   login=str(login)
   if password=="haslo" and login=="loki":
      session['sjnsda8i3j2k4a,mSDAlk*@nb2']="87ashknm2afm,cxvnxc"
      return redirect("/dodaj_post")
   else:
      logowanie.bledne=True
      return redirect('/dodaj_post_logowanie')
   






if __name__ == '__main__':
    
    app.run('0.0.0.0',port=230,debug=True)


