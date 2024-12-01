from negozio import db, bcrypt, login_manager
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# gestione stato utente
from flask_login import UserMixin
from datetime import datetime

# id utente per gestire il suo stato
@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))

#definizione del modello di dati 

class Prodotto(db.Model):
    __tablename__ = 'Prodotto'
    id = db.Column(db.Integer(), primary_key=True)
    servizio = db.Column(db.String(length=30), nullable=False, unique=True)
    codice = db.Column(db.String(length=12), nullable=False, unique=True)
    prezzo = db.Column(db.Integer(), nullable=False)
    descrizione = db.Column(db.String(length=1024), nullable=False, unique=True)

    # aggiungo il servizio al carrello devo passare anche il prodotto
    def carrello(self, user, qta_articolo):
        data_ora_corrente = datetime.now()
        #recupero eventualmente l'articolo già inserito con le qta
        query = db.session.query(Prodotto.codice, func.sum(Acquisto.qta), Acquisto.id) \
            .join(Acquisto, Acquisto.prodotto_id == Prodotto.id) \
            .join(Utente, Utente.id == Acquisto.utente_id) \
            .filter(Utente.id == user.id) \
            .filter(Prodotto.id == self.id)

        get_count_item = query.count()
        items = query.all()
        print(get_count_item)
        #se trova articoli nel carrello
        if get_count_item == 1 and (items[0][1] != None and items[0][1] >0):
            Acquisto.query.filter_by(id=items[0][2]).update(dict(qta=items[0][1] + qta_articolo))
            user.budget -= (self.prezzo * int(qta_articolo))           
            db.session.commit()
        #se trova articoli, ma non nel carrello
        elif get_count_item == 1 and (items[0][1] == None or items[0][1] == 0):
            car = Acquisto(prodotto_id=self.id, utente_id=user.id,data_acquisto=data_ora_corrente, qta = qta_articolo)
            user.budget -= (self.prezzo * int(qta_articolo))
            db.session.add(car)
            db.session.commit()
      
        
    def __repr__(self):
        return f'Prodotto {self.servizio}'

class Utente(db.Model, UserMixin):
    __tablename__ = 'Utente'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)

    # creazione di un metodo setter per criptare la password
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # decriptazione della password 
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.prezzo
    
    
class Acquisto(db.Model):
    __tablename__ = 'Acquisto'
    id = db.Column(db.Integer(), primary_key=True)
    prodotto_id = db.Column(db.Integer(), ForeignKey('Prodotto.id'), nullable=False)
    utente_id = db.Column(db.Integer(), ForeignKey('Utente.id'), nullable=False)
    data_acquisto = db.Column(db.DateTime, nullable=False)
    qta = db.Column(db.Integer(), nullable=False)

    prodotto = relationship("Prodotto", backref="acquisti")
    utente = relationship("Utente", backref="acquisti")

    def can_sell(self, item_obj):
        return item_obj in self.prodotto

    def __repr__(self):
        return f'Acquisto {self.id}: {self.prodotto.servizio} by {self.utente.username}'