from negozio import app,db
from negozio.models import Prodotto, Acquisto, Utente

with app.app_context():
     db.create_all()


# creazione del database
with app.app_context():
    if not db.inspect(db.engine).has_table('Prodotto'):
        db.create_all()
        serv1 = Prodotto(servizio="Massaggio", codice="893212299897", prezzo= 90, descrizione="Massaggio sdrenante 1 ora")
        serv2 = Prodotto(servizio="Manicure", codice="893212299898", prezzo= 70, descrizione="Manicure standard 45 min")
        serv3 = Prodotto(servizio="Pedicure", codice="893212299899", prezzo= 50, descrizione="Pedicure standard 45 min")
        serv4 = Prodotto(servizio="Lampada", codice="893212299900", prezzo= 40, descrizione="Lampada solare 30 min")
        db.session.add(serv1)
        db.session.add(serv2)
        db.session.add(serv3)
        db.session.add(serv4)
        db.session.commit()
    
    if not db.inspect(db.engine).has_table('Acquisto'):
        db.create_all()