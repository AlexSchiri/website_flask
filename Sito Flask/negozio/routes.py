from negozio import app
from flask import render_template, redirect, url_for, flash, request
from negozio.models import Prodotto, Utente, Acquisto
from negozio.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from negozio import db
# import classe login user
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# lettura dei record e rendering nella pagina abilitazione di GET e POST
@app.route('/market', methods=['GET', 'POST'])
# richiesto essere loggati per accedere al market
@login_required
def market():
    # creazione form di acquisto
    purchase_form = PurchaseItemForm()
    # creazione form di rilascio prodotto
    selling_form = SellItemForm()
    
    if request.method == "POST":

        control = 0 #controllo caricamento e rilascio
        # Logica caricamento nel carrello
        purchased_item = request.form.get('purchased_item')
        qta_comprata = request.form.get('qta')
        p_item_object = Prodotto.query.filter_by(servizio=purchased_item).first()
        if p_item_object:
            control = 1  
            if current_user.can_purchase(p_item_object):
                p_item_object.carrello(current_user, int(qta_comprata))
                flash(f"Aggiunto al carrello: {p_item_object.servizio} per {p_item_object.prezzo} Euro", category='success')
            else:
                flash(f"Credito non sufficiente !!! {p_item_object.servizio}!", category='danger')
        
       
        # Logica rilascio servizi dal carrello
        sold_item = request.form.get('sold_item') # id del prodotto che voglio rilasciare
        qta_rilasciata = request.form.get('qta')

        if control==0:
            # prodotto che proviene dal carrello
            prodotto_da_rilasciare = Prodotto.query.filter_by(id=sold_item).first()
            qta_carrello = request.form.get('qta_carrello')           
            #devo verificare con una validazione che la qta rilasciata 
            #sia minore o uguale della qta in carrello
            #se uguale, elimino l'articolo dal carrello
            if qta_rilasciata > qta_carrello:
                flash(f"Non puoi rilasciare una quantità maggiore di quella presente nel tuo carrello per questo articolo", category='danger')
                return redirect(url_for('market'))
            elif qta_rilasciata == qta_carrello:
                # aggiornamento del budget
                current_user.budget += (prodotto_da_rilasciare.prezzo * int(qta_rilasciata))
                # eliminazione del servizio dal carrello    
                Acquisto.query.filter(
                    and_(
                        Acquisto.prodotto_id == sold_item,
                        Acquisto.utente_id == current_user.id,
                        )
                    ).delete()
                db.session.commit()  
                flash(f"Servizio rilasciato e budget aggiornato", category='success')
            else:
                # aggiornamento del budget
                current_user.budget += (prodotto_da_rilasciare.prezzo * int(qta_rilasciata))
                Acquisto.query.filter(
                    and_(
                        Acquisto.prodotto_id == sold_item,
                        Acquisto.utente_id == current_user.id,
                        )
                    ).update(dict(qta=int(qta_carrello) - int(qta_rilasciata)))
                db.session.commit()
        control=0
        return redirect(url_for('market'))


    #filtro del carrello
    if request.method == "GET":
        items = Prodotto.query.all()

        #join delle tre tabelle per filtrare i prodotti nel carrello dell'id corrente
        query = db.session.query(Prodotto.id, Prodotto.servizio, Prodotto.codice, Prodotto.prezzo, Acquisto.qta) \
            .join(Acquisto, Acquisto.prodotto_id == Prodotto.id) \
            .join(Utente, Utente.id == Acquisto.utente_id) \
            .filter(Utente.id == current_user.id)

        owned_items = query.all()
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # verifico se le credenziali sono corrette
    if form.validate_on_submit():
        attempted_user = Utente.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Successo! sei loggato nel sistema: {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Nome utente e/o password sbagliati, riprova!', category='danger')

    return render_template('login.html', form=form)

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # se la validazione dei dati va a buon fine registro l'utente
    if form.validate_on_submit():
        utente_da_registrare = Utente(username=form.username.data,
                                     email_address=form.email_address.data,
                                     password=form.password1.data)
        db.session.add(utente_da_registrare)
        try:
          db.session.flush()
          # Se flush() non genera eccezioni, il record è stato salvato
          # ... codice per gestire il record salvato ...
        except Exception as e:
          # Se flush() genera un'eccezione, il record non è stato salvato
          # ... codice per gestire l'errore di salvataggio ...
          print("Errore durante la registrazione dell'utente.")
        db.session.commit()
        # dopo aver registrato il nuovo utente faccio un redirect al listino prodotti
        return redirect(url_for('login'))
    
    if form.errors != {}: #se il dizionario degli errori non è vuoto
        for err_msg in form.errors.values():
            flash(f'Errore nella creazione nuovo utente: {err_msg}', category='danger')
       
    
    return render_template('register.html', form=form)

# route di logout
@app.route('/logout')
def logout():
    logout_user()
    flash("Logout avvenuto correttamente!", category='info')
    return redirect(url_for("home"))