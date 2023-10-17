import datetime
import telegram
from db import *
from datetime import date, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters



#-------------------------------------------------------------------------------------------------------
#                   10.3 Contatto e prenotazione ricevimento docente tramite bot
#-------------------------------------------------------------------------------------------------------





#-----------------------------------------------------
#               DEFINIZIONE FUNZIONE KEYBOARD 
#-----------------------------------------------------

def create_keyboard(lista,flag = False, frase = ''):
    if flag:
        keyboard = [[InlineKeyboardButton(str(lista[x]), callback_data= frase + str(lista[x]))] for x in range(len(lista))] 
        return InlineKeyboardMarkup(keyboard)
    #tastiera inline modificabile in base all'evenienza
    keyboard = [[InlineKeyboardButton(str(lista[x]), callback_data=str(lista[x]))] for x in range(len(lista))] 
    return InlineKeyboardMarkup(keyboard)




#-----------------------------------------------------
#               DEFINIZIONE FUNZIONE START 
#-----------------------------------------------------

def start(update, context):
    id = update.message.chat_id
    #controllo che l'utente non sia gia registrato
    if seeDocenti(id) or seeStudenti(id):
        update.message.reply_text('Essendo gia registrato, vuole cambiare il suo ruolo?', reply_markup=create_keyboard(['SI','NO']))
    #registrazione dell'utente
    else:
        update.message.reply_text('Benvenuto, sono un bot per il contatto e la prenotazione del ricevumento. La prego di identificarsi: ', reply_markup=create_keyboard(['DOCENTE','STUDENTE']))


#-----------------------------------------------------
#               DEFINIZIONE FUNZIONE COMMAND 
#-----------------------------------------------------

def command(update, context):
    id = update.message.chat_id
    
    #comandi per gli studenti
    if seeStudenti(id):
        update.message.reply_text('I comandi da lei utilizzabili, essendo uno studente sono:', reply_markup=create_keyboard(['INVIA UN MESSAGGIO','INIZIA A SEGUIRE UN DOCENTE','INIZIA A SEGUIRE UN CORSO','SMETTI DI SEGUIRE','VISUALIZZA DOCENTI CHE STA SEGUENDO','VISUALIZZA CORSI CHE STA SEGUENDO']))
    
    #comandi per i docenti
    if seeDocenti(id):
        update.message.reply_text('I comandi da lei utilizzabili, essendo un docente sono:', reply_markup=create_keyboard(['MESSAGGIO DIRETTO','BROADCAST','AGGIUNGI UN TUO CORSO', 'ELIMINA UN TUO CORSO','LISTA DEI SUOI CORSI','LISTA DEI SUOI SEGUACI']))




#-----------------------------------------------------
#               DEFINIZIONE FUNZIONE BUTTON 
#-----------------------------------------------------

def button(update, context):
    query = update.callback_query
    id = query.message.chat_id,

    #iscrizione docente
    if query.data == 'DOCENTE':
        if seeDocenti(id[0]):
            context.bot.send_message(chat_id=query.message.chat_id, text="Prema /start un altra volta per poter cambiare il suo ruolo")
        else:
            nuovoDocente(id[0],update.effective_user['username'],'','')
            context.bot.send_message(chat_id=query.message.chat_id, text="Si è appena registrato come DOCENTE")
    
    #iscrizione studente
    if query.data == 'STUDENTE':
        if seeDocenti(id[0]):
            context.bot.send_message(chat_id=query.message.chat_id, text="Prema /start un altra volta per poter cambiare il suo ruolo")
        else:
            nuovoStudente(id[0],update.effective_user['username'],'','')
            #nuovoStudente(id[0],update.effective_user['username'])
            context.bot.send_message(chat_id=query.message.chat_id, text="Si è appena registrato come STUDENTE")
    
    #cambio ruolo utente
    if query.data == 'SI':
        if seeDocenti(id[0]):
            eliminaDocente(id[0])
            nuovoStudente(id[0],update.effective_user['username'])
            context.bot.send_message(chat_id=query.message.chat_id, text="Si è appena registrato come STUDENTE")
        else:
            eliminaStudente(id[0])
            nuovoDocente(id[0],update.effective_user['username'],'','')
            context.bot.send_message(chat_id=query.message.chat_id, text="Si è appena registrato come DOCENTE")
    
    #no cambio ruolo utente
    if query.data == 'NO':
        context.bot.send_message(chat_id=query.message.chat_id, text="Non ha apportato nessuna modifica")
    
    #comando broadcast
    if query.data == 'BROADCAST': 
        context.bot.send_message(chat_id=query.message.chat_id, text="Per inviare un messaggio in broadcast a tutti i suoi follower, la prego di impostare il messaggio cosi:  BROADCAST: 'testo '")
        context.bot.send_message(chat_id=query.message.chat_id, text="La informo che per mandare un messaggio in broadcast non deve necessariamente selezionare il comando ogni volta ma puo anche solamente mandare il messaggio")
    
    #comando messaggio diretto
    if query.data == 'MESSAGGIO DIRETTO':
        context.bot.send_message(chat_id=query.message.chat_id, text="Per inviare un messaggio diretto a una persona, la prego di impostare il messaggio cosi: 'NOME DESTINATARIO': 'testo'")
    
    if query.data == 'INVIA UN MESSAGGIO':
        context.bot.send_message(chat_id=query.message.chat_id, text="Per inviare un messaggio diretto a una persona, la prego di impostare il messaggio cosi: 'NOME DESTINATARIO': 'testo'")
    

    
    #comando aggiungi corso (se docente)
    if query.data == 'AGGIUNGI UN TUO CORSO':
        context.bot.send_message(chat_id=query.message.chat_id, text="Per inserire un suo corso, mi inoltri un messaggio del tipo: 'CORSO': 'nome corso'")
    
    #comando elimina corso (se docente)
    if query.data == 'ELIMINA UN TUO CORSO':
        context.bot.send_message(chat_id=query.message.chat_id, text="Per eliminare un suo corso dalla sua lista, mi inoltri un messaggio del tipo: 'ELIMINA CORSO': 'testo'")
    
    #comando lista corsi (se docente)
    if query.data == 'LISTA DEI SUOI CORSI':
        corsi = getCorsi(id[0]).split(',')
        if not corsi[0]:
            context.bot.send_message(chat_id=query.message.chat_id, text='Al momento non detiene nessun corso')
        else:
            context.bot.send_message(chat_id=query.message.chat_id, text='I suoi corsi sono:')
            for x in corsi:
                if x:
                    context.bot.send_message(chat_id=query.message.chat_id, text=x)
    
    #comando inizia a seguire docente (se studente)
    if query.data == 'INIZIA A SEGUIRE UN DOCENTE':
            query.message.reply_text("Ecco a lei la lista di tutti i docenti:",reply_markup=create_keyboard(allDocenti(),True,'NUOVO SEGUACE DOCENTE:'))

    #comando inizia a seguire corso (se studente)        
    if query.data == 'INIZIA A SEGUIRE UN CORSO':
            context.bot.send_message(chat_id=query.message.chat_id, text='Ecco qua la lista di tutti i docenti con i rispettivi corsi:')
            nomi = allDocenti()
            for x in nomi:
                query.message.reply_text(x,reply_markup=create_keyboard(allCorsi(x),True,'NUOVO SEGUACE CORSO:'))
    
    #divido il messaggio per individuare se è presente un comando
    splitD = query.data.split(':')
    
    #comando smetti di seguire (se studente)
    if query.data == 'SMETTI DI SEGUIRE':
        query.message.reply_text('Cosa vuole smettere di seguire? ',reply_markup=create_keyboard(['PROFESSORE','LEZIONE']))
    
    #comando successivo a smetti di seguire che va a stampare la lista dei docenti che uno studente sta seguendo
    if query.data == 'PROFESSORE':
        query.message.reply_text('Se non segue nessun docente non le verra inviata nessuna lista. Altrimenti questa è la lista dei docenti che segue: ',reply_markup=create_keyboard(seeFollow(id[0])))

    #controlla se query.data sia un nome di un docente 
    #e se si allora si è nel caso in cui uno studente vuole smettere di seguire un docente
    if seeDocenti(nome = query.data):
        updateDB(campo = 'follow', id = id[0], aggiunta = ',' + query.data, modalita = 2)
        updateDB(campo = 'follower', id = takeID(query.data)[0], aggiunta = ','+ takeName(id[0]), modalita = 2)
        query.message.reply_text(f'Hai smesso di seguire {query.data}')

    #comando successivo a smetti di seguire che va a stampare tutti i corsi che segue
    if query.data == 'LEZIONE':
        query.message.reply_text('Se non segue nessun corso non le verra inviata nessuna lista. Altrimenti questa è la lista dei corsi che segue: ',reply_markup=create_keyboard(takeCorsi(id[0]),True,'COS:')) 

    #comando che applica l effettivo smettimento di seguire di un corso da parte di uno studente
    if splitD[0] == 'COS':
        print('split= ' + str(',' + splitD[1]))
        updateDB(campo = 'corsi', id = id[0], aggiunta = ',' + splitD[1], modalita = 2)
        updateDB(campo = 'follower', id = id[0], aggiunta = splitD[1], modalita = 2, corso = True)
        query.message.reply_text(f'Hai smesso di seguire {splitD[1]}')
 
       
    #controllo corrispondenza messaggio e stringa
    #successivo inizio a seguire di un corso
    if splitD[0] == 'NUOVO SEGUACE CORSO':
        updateDB(campo = 'corsi', id = id[0], aggiunta = ',' + splitD[1], modalita = 1)
        updateDB(campo = 'follower', id = id[0],aggiunta = splitD[1], modalita = 1, corso = True)
        query.message.reply_text(f'Hai iniziato a seguire {splitD[1]}')

    #controllo corrispondenza messaggio e stringa 
    #successivo inizio a seguire un docente 
    if splitD[0] == 'NUOVO SEGUACE DOCENTE':
        aggiunta =',' + str(splitD[1])
        updateDB(campo = 'follow',id = id[0], aggiunta = aggiunta,modalita = 1)
        updateDB(campo = 'follower', id = takeID(splitD[1])[0], aggiunta = ',' + takeName(id[0]),modalita = 1) 
        query.message.reply_text(f'Hai iniziato a seguire {splitD[1]}')
    
    #comando che manda per messaggio i corsi che sta seguendo
    if query.data == 'VISUALIZZA CORSI CHE STA SEGUENDO':
        corsi = (allCorsi(takeName(id[0])))[0].split(',')
        print(corsi)
        if not corsi[0]:
            context.bot.send_message(chat_id=query.message.chat_id, text='Non segue ancora nessun corso')
        else:
            context.bot.send_message(chat_id=query.message.chat_id, text='I corsi che sta seguendo sono:')
            for x in corsi:
                context.bot.send_message(chat_id=query.message.chat_id, text=x)
        print('---------visualizza corsi--------')
        seeTable('studenti')
        seeTable('corso')
    
    #comando che manda per messaggio i docenti che sta seguendo
    if query.data == 'VISUALIZZA DOCENTI CHE STA SEGUENDO':
        docenti = allFollow(id[0]).split(',')
        print(type(docenti))
        print(docenti)
        if not docenti[0]:
                context.bot.send_message(chat_id=query.message.chat_id, text='Non segue ancora nessun docente')
        else:
            context.bot.send_message(chat_id=query.message.chat_id, text='I docenti che sta seguendo sono:')
            for x in docenti:
                context.bot.send_message(chat_id=query.message.chat_id, text=x)
    
    #comando che permette al docente di visualizzare i suoi follower
    if query.data == 'LISTA DEI SUOI SEGUACI':
        follower = allFollower(id[0]).split(',')
        print('pre folloerw')
        print(str(follower))
        if not follower[0]:
            print('--------------------------')
            context.bot.send_message(chat_id=query.message.chat_id, text='Mi dispiace ma non ha nessun seguace')
        else:
            context.bot.send_message(chat_id=query.message.chat_id, text = 'I seguenti nomi sono tutti gli studenti che la seguono:')
            for x in follower:
                context.bot.send_message(chat_id=query.message.chat_id, text = x)




#-----------------------------------------------------
#               DEFINIZIONE FUNZIONE MESSAGE 
#-----------------------------------------------------

def message(update,context):
    query = update.message
    id = query.chat_id
    splitM = query.text.split()
    
    #divisione del messaggio e controllo se l'utente è un docente
    if splitM[0] == 'BROADCAST:' and seeDocenti(id):
        followersID = seeFollowers(id)
        #invio messaggio tramite broadcast
        for x in followersID:
            context.bot.send_message(chat_id=x, text=query.text)

    #divisione del messaggio        
    splitD = query.text.split(':')
    
    #controllo se studente o docente
    if seeStudenti(nome = splitD[0]) or seeDocenti(nome = splitD[0]):
        #context.bot.send_message(chat_id=query.chat_id, text= ':'.join(splitD))
        context.bot.send_message(chat_id=takeID(splitD[0])[0], text=str(takeName(query.chat_id)) + ': '+ splitD[1])
    
    #comando che crea un nuovo corso
    if splitM[0] == 'CORSO:' and seeDocenti(id):
        print('prima')
        seeTable('corso')
        aggiunta = ',' + (' '.join(splitM[1:]))
        updateDB('corsi',id,aggiunta,1)
        nuovoCorso(' '.join(splitM[1:]),id)
        context.bot.send_message(chat_id=query.chat_id, text= '"' + str(aggiunta[1:]) + '" è appena stato aggiunto come corso')
        print('dopo')
        seeTable('corso')
    
    #comando che elimina un corso
    if splitD[0] == 'ELIMINA CORSO' and seeDocenti(id):
        cancellazione = ',' + (':'.join(splitD[1:]))[1:]
        updateDB('corsi',id,cancellazione,2)
        eliminaCorso(cancellazione[1:])
        context.bot.send_message(chat_id=query.chat_id, text= '"' + str(cancellazione[1:]) + '" è appena stato eliminato come corso')

        

        
        
    

#-----------------------------------------------------
#               CREAZIONE DI DOCENTI FITTIZI
#-----------------------------------------------------
def main():
    avvioBot()
    print('-----------------------------------')
    seeTable('docenti')
    print('-----------------------------------')
    seeTable('studenti')
    print('-----------------------------------')
    seeTable('corso')
    print('-----------------------------------')


main()


#-----------------------------------------------------
#               CONFIGURAZIONE E GESTIONE  BOT
#-----------------------------------------------------

updater = Updater('TOKEN')
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('command', command))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message))




#-----------------------------------------------------
#                      AVVIO BOT
#-----------------------------------------------------

updater.start_polling()
updater.idle()
