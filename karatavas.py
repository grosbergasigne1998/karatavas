import random
import logging
import string
import mysql.connector
from vardi import vardi
from karatavu_zimejums import solis
from datetime import datetime

logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

punkti = 0
# ar random funkciju iegust minamo vardu no vardu saraksta
def randomVards(vardi):
    vards = random.choice(vardi)  
    while '-' in vards or ' ' in vards:
        vards = random.choice(vardi)
    return vards.upper()   


logging.info('Programma tiek palaista')

vards = randomVards(vardi)
# iegust burtu skaitu no varda
vardaSastavs = set(vards)
alfabets = set(string.ascii_uppercase)
izmantotieBurti = set()  
dzivibas = 10

print("\n")
print("Tavs uzdevums ir atminēt doto angļu valodas vārdu, lai izbēgtu no karātavām.")

# iegust lietotaja ievadi
while len(vardaSastavs) > 0 and dzivibas > 0:
        print('Tev ir palikušas', dzivibas, 'dzīvības. Izmantotie burti: ', ' '.join(izmantotieBurti))
        # Salidzina lietotaja ievadito burtu ar katru minama varda burtu, ja tas atbilst - ievieto burtu, ja nē - atstāj "-"
        jaunaisVards = [burts if burts in izmantotieBurti else '-' for burts in vards]
        # tiek izdrukats karatavu zimejums, atbilstosi atlikusa sola jeb dzivibu skaitam
        print(solis[dzivibas])
        print('Minamais vārds: ', ' '.join(jaunaisVards))

        lietotajaIevaditaisBurts = input('Ievadi burtu: ').upper()
        # parbauda vai ievaditais burts atrodas alfabeta un vai tas nav izmantots
        if lietotajaIevaditaisBurts in alfabets - izmantotieBurti:
            izmantotieBurti.add(lietotajaIevaditaisBurts)
            if lietotajaIevaditaisBurts in vardaSastavs:
                vardaSastavs.remove(lietotajaIevaditaisBurts)
                print('')

            else:
                # ja ievaditais burts nav varda sastava tiek atnemta dziviba
                dzivibas = dzivibas - 1  
                print('\nBurts ', lietotajaIevaditaisBurts, ' nav šajā vārdā!')

        elif lietotajaIevaditaisBurts in izmantotieBurti:
            # ja kads burts tiek ievadits atkartoti, konsole tiek paradits pazinojums
            logging.warning('lietotaja ievades kluda (atkartojas)')
            print('\nŠo burtu jau izmantoji! Izvēlies citu!')

        else:
            logging.warning('lietotaja ievades kluda(nepareizs simbols)')
            print('\nIzvēlies citu, derīgu, burtu!')

# ja beidzas soli jeb dzivibas vai vards tiek atminets tiek izvadits pazinojums
if dzivibas == 0:
        print(solis[dzivibas])
        print('Ak nē! Tu neizbēgi no karātavām! :( Vārds, kuru neatminēji: ', vards)
        print("")
        
else:
        print('Apsveicu! Tu atminēji vārdu:', vards, 'Tu izbēgi no karātavām! :)')
        print("")
        punkti=dzivibas


logging.info('rezultats tiek saglabats datubaze')

now = datetime.now()

#veic piekluvi mysql un izveletajai datubazei
db = mysql.connector.connect(
    #areja host piekluve, ja npieciesama piekluve no cita datora
    #host="DESKTOP-7JR578B",
    host="localhost",
    user="root",
    passwd="Grosberga@1998",
    database = "karatavas"
)
mycursor = db.cursor(buffered=True)
#mycursor.execute("CREATE TABLE ScoreBoard (jauniPunkti int, datums varchar(40))")
#komanda jau ir izpildita - tabula izveidota
mycursor.execute("DESCRIBE ScoreBoard")
#ievieto iegutos datus no speles
mycursor.execute("INSERT INTO ScoreBoard (jauniPunkti, datums) VALUES (%s,%s)",(punkti,now))
db.commit()

print("(iegūtie punkti, spēles norises laiks)")
mycursor.execute("SELECT * FROM ScoreBoard")
for x in mycursor:
    print(x)

#ja velas nodzest datus izveidotaja tabula
#mycursor.execute("TRUNCATE TABLE ScoreBoard")
#db.commit()

logging.info('Programma tiek aptureta')
