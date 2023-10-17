import mysql.connector


#definizione del db
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'PASSWORD',
    database = 'DB'
)


#creo un corsore per la visita delle tabelle 
cursor = db.cursor()




#----------------------------------------------------------------------------------------------------
#          QUESTO METODO CREA LE TABELLE E LE RIEMPE PER L'USO DURANTE IL TESTING
#----------------------------------------------------------------------------------------------------

def avvioBot():
    #elimino le tabelle se sono gia esistenti
    cursor.execute('DROP TABLE IF EXISTS studenti')
    cursor.execute('DROP TABLE IF EXISTS docenti')
    cursor.execute('DROP TABLE IF EXISTS corso')
    #creo le tabelle

    cursor.execute('CREATE TABLE corso (nome VARCHAR(255) PRIMARY KEY, follower VARCHAR(255), docente VARCHAR(255))')
    cursor.execute('CREATE TABLE studenti (id INT PRIMARY KEY, nome VARCHAR(255), follow VARCHAR(255), corsi VARCHAR(255))')
    cursor.execute('CREATE TABLE docenti (id INT PRIMARY KEY, nome VARCHAR(255), follower VARCHAR(255), corsi VARCHAR(255))')

    #populo la tabella docenti
    sql = 'INSERT INTO docenti (id, nome, follower, corsi) VALUES (%s,%s,%s,%s)'
    val = [(1,'Riccardo Cristofani', '', ',programmazione 1'),(2,'Goffredo Antonelli', '', ',architettura'),(3,'Giuseppe Verdi', '', ',protocolli reti')]
    cursor.executemany(sql, val)
    db.commit()

    #populo la tabella studenti
    sql = 'INSERT INTO studenti (id, nome, follow, corsi) VALUES (%s,%s,%s,%s)'
    val = [(4,'Edoardo Pippi','',''),(5,'Max Manselli','ingegneria del software',''),(6,'Christian Angileri','','')]
    cursor.executemany(sql, val)
    db.commit()

    #populo la tabella corso
    sql = 'INSERT INTO corso (nome, follower, docente) VALUES (%s,%s,%s)'
    val = [('programmazione 1','',1),('architettura','',2),('protocolli reti','',3)]
    cursor.executemany(sql, val)
    db.commit()






#------------------------------------------------------------------------------
#          QUESTO METODO CREA UN NUOVO DOCENTE NELLA TABELLA DOCENTI
#------------------------------------------------------------------------------

def nuovoDocente(id:int, nome:str, followers = '', corsi = ''):
    sql = 'INSERT INTO docenti (id, nome, follower, corsi) VALUES (%s,%s,%s,%s)'
    cursor.execute('INSERT INTO docenti (id, nome, follower, corsi) VALUES (%s,%s,%s,%s)',(id,nome,followers,corsi))
    db.commit()






#------------------------------------------------------------------------------
#          QUESTO METODO CREA UN NUOVO CORSO NELLA TABELLA CORSI
#------------------------------------------------------------------------------

def nuovoCorso(nome:str, idDoc:int, follower = ''):
    cursor.execute('INSERT INTO corso (nome,follower,docente) VALUES (%s,%s,%s)', (nome,follower,idDoc))
    db.commit()





#------------------------------------------------------------------------------
#          QUESTO METODO CONTROLLA SE UN CORSO ESISTE GIA'
#------------------------------------------------------------------------------

def controllaCorso(nome:str):
    cursor.execute('SELECT * FROM corso WHERE nome = %s',nome)
    if cursor.fetchone():
        return True
    return False




#------------------------------------------------------------------------------
#          QUESTO METODO CREA UN NUOVO STUDENTE NELLA TABELLA STUDENTI
#------------------------------------------------------------------------------

def nuovoStudente(id:int, nome:str, follow = '', corsi = ''):
    sql = 'INSERT INTO studente (id, nome, follow, corsi) VALUES (%s,%s,%s,%s)'
    cursor.execute('INSERT INTO studenti (id, nome, follow, corsi) VALUES (%s,%s,%s,%s)',(id,nome,follow,corsi))
    db.commit()





#------------------------------------------------------------------------------
#          QUESTO METODO ELIMINA UNO STUDENTE DALLA TABELLA STUDENTI
#------------------------------------------------------------------------------

def eliminaStudente(id = 0, nome = ''):
    if id != 0:
        cursor.execute('DELETE FROM studenti WHERE id = %s',(id,))
    else: 
        cursor.execute('DELETE FROM studenti WHERE nome = %s',(nome,))
    db.commit()




#------------------------------------------------------------------------------
#          QUESTO METODO ELIMINA UN CORSO DALLA TABELLA CORSO
#------------------------------------------------------------------------------

def eliminaCorso(nome):
    cursor.execute('SELECT follower FROM corso where nome = %s',(nome,))
    follower =cursor.fetchone()[0]
    if follower:
        follower = follower.split(',')
        for x in follower:
            updateDB('follow',takeID(x),nome,2)
    
    cursor.execute('DELETE FROM corso WHERE nome = %s',(nome,))
    db.commit()




#------------------------------------------------------------------------------
#           QUESTO METODO ELIMINA UN DOCENTE DALLA TABELLA DOCENTI
#------------------------------------------------------------------------------
def eliminaDocente(id = 0, nome = ''):
    if id != 0:
        cursor.execute('DELETE FROM docenti WHERE id = %s',(id,))
    else:
        cursor.execute('DELETE FROM docenti WHERE nome = %s',(nome,))
    db.commit()





#------------------------------------------------------------------------------
#           QUESTO METODO RITORNA IL NOME DI UN UTENTE DATO IL SUO ID
#------------------------------------------------------------------------------

def takeName(id):
    if seeDocenti(id):
        cursor.execute('SELECT nome FROM docenti WHERE id = %s', (id,))
        name = cursor.fetchone()[0]

    if seeStudenti(id):
        cursor.execute('SELECT nome FROM studenti WHERE id = %s', (id,))
        name = cursor.fetchone()[0]
    return name





#------------------------------------------------------------------------------
#           QUESTO METODO RITORNA  L'ID DI UN UTENTE DATO IL SUO NOME
#------------------------------------------------------------------------------

def takeID(nome):
    if seeDocenti(nome = nome):
        cursor.execute('SELECT id FROM docenti WHERE nome = %s', (nome,))
        return cursor.fetchone()
    if seeStudenti(nome = nome):
        cursor.execute('SELECT id FROM docenti WHERE nome = %s', (nome,))
        return cursor.fetchone()
    




#----------------------------------------------
#           STAMPA LA TEBELLA DESIGNATA
#----------------------------------------------
def seeTable(name:str):
    cursor.execute(f'SELECT * FROM {name}')
    row = cursor.fetchall()
    for x in row:
        print(x)




#------------------------------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI I DOCENTI REGISTRATI
#------------------------------------------------------------------------------

def allDocenti():
    cursor.execute('SELECT nome FROM docenti')
    nomi = cursor.fetchall()
    res = []
    for x in nomi:
        res.append(x[0])
    return res



#---------------------------------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI GLI STUDENTI CHE SEGUONO UN CERTO DOCENTE
#---------------------------------------------------------------------------------

def allFollower(id):
    cursor.execute(f'SELECT follower FROM docenti WHERE id = {str(id)}')
    nomi = cursor.fetchone()
    print('nomi = ' + str(nomi))
    return nomi[0]
    res = []
    for x in nomi:
        res.append(x[0])
    return res

def allFollow(id):
    cursor.execute(f'SELECT follow FROM studenti WHERE id = {str(id)}')
    nomi = cursor.fetchone()
    print('nomi = ' + str(nomi))
    return nomi[0]





#------------------------------------------------------------------------------
#           QUESTO METODO VERIFICA SE UNO STUDENTE E' REGISTRATO
#------------------------------------------------------------------------------

def seeStudenti(id = 0, nome = ''):
    if id != 0:    
        cursor.execute('SELECT * FROM studenti WHERE id = %s', (id,))  
    else: 
        cursor.execute('SELECT * FROM studenti WHERE nome = %s', (nome,))  
    if cursor.fetchall():
        return True
    return False






#------------------------------------------------------------------------------
#           QUESTO METODO VERIFICA SE UN DOCENTE E' REGISTRATO
#------------------------------------------------------------------------------

def seeDocenti(id = 0, nome = ''):
    if id != 0:
        cursor.execute('SELECT * FROM docenti WHERE id = %s', (id,))   
    else:
        cursor.execute('SELECT * FROM docenti WHERE nome = %s', (nome,))   
    if cursor.fetchall():
        return True
    return False


#------------------------------------------------------------------------------
#           QUESTO METODO VERIFICA SE UN E' UN CORSO
#------------------------------------------------------------------------------

def seeCorso(id = 0, nome = ''):
    if id != 0:
        cursor.execute('SELECT * FROM docenti WHERE id = %s', (id,))   
    else:
        cursor.execute('SELECT * FROM docenti WHERE nome = %s', (nome,))   
    if cursor.fetchall():
        return True
    return False




#----------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI GLI STUDENTI 
#               CHE SEGUONO UN CERTO DOCENTE
#----------------------------------------------------------

def seeFollowers(id):
    cursor.execute('SELECT * FROM docenti WHERE id = %s', (id,))
    followers = cursor.fetchone()[2].split(',')
    idf = []
    for x in followers:
        cursor.execute('SELECT id FROM studenti WHERE nome = %s',(x,))
        fID = cursor.fetchall()
        if fID:
            idf.append(sum(fID[0]))
    return idf




#----------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI I CORSI 
#               CHE UNO STUDENTE SEGUE
#----------------------------------------------------------

def takeCorsi(id):
    cursor.execute('SELECT corsi FROM studenti WHERE id = %s', (id,))
    corsi = cursor.fetchone()[0].split(',')
    return corsi



#----------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI I DOCENTI 
#               CHE UNO STUDENTE SEGUE
#----------------------------------------------------------

def seeFollow(id):
    cursor.execute('SELECT * FROM studenti WHERE id = %s', (id,))
    follow = cursor.fetchone()[2].split(',')
    idf = []
    for x in follow:
        cursor.execute('SELECT id FROM docenti WHERE nome = %s',(x,))
        fID = cursor.fetchall()
        if fID:
            idf.append(takeName(sum(fID[0])))
    return idf









#------------------------------------------------
#           QUESTO METODO AGGIORNA I DB
#------------------------------------------------

def updateDB(campo,id,aggiunta,modalita,corso = False):
    if seeDocenti(id):
        ruolo = 'docenti'
    if seeStudenti(id):
        ruolo = 'studenti'
        if corso:
            ruolo = 'corso'
    if ruolo != 'corso':
        sql = 'SELECT '+ campo +' FROM ' + ruolo +' WHERE id = %s'
        cursor.execute(sql,(id,))

        if modalita == 1:
            vecchio = cursor.fetchone()
            if aggiunta in vecchio[0] or aggiunta[1:] in vecchio[0]:
                return 
            if not vecchio[0]:
                new = aggiunta[1:]
            else:
                new = ','.join(vecchio[:]) + aggiunta
        else:
            new = cursor.fetchone()[0]
            print('new= ' + str(new))
            if modalita == 2 and (aggiunta in new or aggiunta[1:] in new):
                if aggiunta in new:
                    new = new.replace(aggiunta,'')
                if  aggiunta[1:] + ',' in new:
                    new = new.replace(aggiunta[1:] + ',','') 
                if aggiunta[1:] in new:
                    print('2')
                    new = new.replace(aggiunta[1:],'') 
        sql = 'UPDATE ' + ruolo + ' set ' + campo + ' = %s ' + f'WHERE id = {int(id)}'
        cursor.execute(sql, (new,))
        db.commit()
    #codice specializzato nella tabella "corso"
    else:
        nome = takeName(id)
        sql = 'SELECT '+ campo +' FROM ' + ruolo +' WHERE nome = %s'
        cursor.execute(sql,(aggiunta,))
        old = cursor.fetchone()
        if modalita == 1:
            if nome in old[0] or ',' + nome in old[0]:
                return
            if not old[0]:
                new = nome
            else:
                new = ','.join(old[:]) + ',' + nome
        else:
            print('nome = ' + nome)
            new = old[0]
            print((str(new[0])))
            print(str(new))
            if modalita == 2 and (nome in new or nome[1:] in new):
                if len(nome) == len(new):
                    new = ''
                if (',' + nome) in new:
                    new = new.replace(',' + nome,'') 
                if nome in new:
                    new = new.replace(nome,'')  
    
        sql = 'UPDATE ' + ruolo + ' set ' + campo + ' = %s' + ' WHERE nome = %s'
        cursor.execute(sql,(new,aggiunta))
        db.commit()

    




        
    







#--------------------------------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI I CORSI SEGUITI DA UN UTENTE 
#                               (dato il suo id)
#--------------------------------------------------------------------------------

def getCorsi(id:int):
    if seeDocenti(id):
        cursor.execute('SELECT corsi FROM docenti WHERE id = %s', (id,)) 
        corsi = cursor.fetchone()[0]
    if seeStudenti(id):
        cursor.execute('SELECT corsi FROM studenti WHERE id = %s', (id,))
        corsi = cursor.fetchone()[0]
    return corsi







#------------------------------------------------------------------------------
#           QUESTO METODO RITORNA TUTTI I DOCENTI REGISTRATI 
#                              (dato il suo nome)
#------------------------------------------------------------------------------

def allCorsi(nome:str):
    if seeDocenti(nome = nome):
        cursor.execute('SELECT corsi FROM docenti WHERE nome = %s',(nome,))
        corsi = cursor.fetchall()
    if seeStudenti(nome = nome):
        cursor.execute('SELECT corsi FROM studenti WHERE nome = %s',(nome,))
        corsi = cursor.fetchall()
    res = []
    for x in corsi:
        res.append(x[0][1:])
    return res