# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv()

import mysql.connector

myuser = os.getenv("BRUKER")
mypassword = os.getenv("PASSORD")

mydb = mysql.connector.connect(
  host="10.2.35.19",
  port="3306",
  user=myuser,
  password=mypassword,
  database='musikk'
)

mycursor = mydb.cursor()

# ubrukt input to execute
sql = "INSERT INTO artists (x) VALUES (%s)"
val = [
    ('Paul McCartney',),
    ('Taylor Swift',),
    ('Kaizers Orchestra',),
    ('Beharie',),
    ('John Lennon',)
]

# lager database og tabeller om de ikke finnes
try:
  mycursor.execute("CREATE DATABASE music")
  mycursor.execute("CREATE TABLE artists (id INTAUTO_INCREMENT PRIMARY KEY, navn VARCHAR(50) NOT NULL)")
  mycursor.execute("CREATE TABLE songs (id INT AUTO_INCREMENT PRIMARY KEY, navn VARCHAR(255) NOT NULL, artists_id INT, FOREIGN KEY (artists_id) REFERENCES artists(id))")
except:
  print("Database og tabeller eksisterer allerede.")
else:
  print(mycursor.rowcount, "endring(er).")

# meny man kan velge fra
mydb.commit()

menu = input('''
Velkommen til musikkregisteret! Her er dagens meny:

(a) Legg til ny artist

(b) Legg til ny sang
             
(c) Vis innhold i en tabell
             
(d) Oppdater artist- eller sangnavn
             
(e) Slett noe fra registeret (sang eller artist)
             
(q) Avslutt

Velg (Tast enter for å bekrefte): ''')

match menu:
  #legg til artist
  case "a":
    #spør bruker antall registre som skal skje
    antall = int(input("Hvor mange artister skal du legge til?: "))
    for i in range(antall):
      sql = "INSERT INTO artister (navn) VALUES (%s)"

      artistname = input("\nHva heter artisten du vil registere?: ")

      mycursor.execute(sql, (artistname,))

    mydb.commit()
    
    print(mycursor.rowcount, "endring(er)")
  
  #legg til sang
  case "b":
    #spør bruker antall registre som skal skje
    antall = int(input("Hvor mange sanger skal du legge til?: "))
    for i in range(antall):
      songname = input("\nHva heter sangen du vil registere?: ")
      songartist = int(input("Hvem fremførte denne låten? (OBS! id til artist, tall): "))
      sql = "INSERT INTO sanger (navn, artists_id) VALUES (%s, %s)"
      mycursor.execute(sql, (songname, songartist,))

    mydb.commit()

    print(mycursor.rowcount, "endring(er)")
  
  #viser brukervalgt tabell
  case "c":
    table = input("Hvilken tabell vil du se? (artister, sanger): ")

    sql = f"SELECT * FROM {table}"

    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for x in myresult:
      print(x)
    
  #oppdater navn
  case "d":
    table = input("Hvilken tabell vil du oppdatere i? (artister, sanger): ")
    column = input("Hvilken kolonne vil du oppdatere? (\'navn\', så langt): ")
    old = input("Hvilket navn vil du endre?: ")
    new = input("Skriv inn nytt navn: ")

    sql = f"UPDATE {table} SET {column} = %s WHERE {column} = %s"

    mycursor.execute(sql, (new, old))

    mydb.commit()

    print("Dine endringer ble gjennomført.")
  
  #slett valgt innhold fra database, én sang eller artist
  case "e":
    table = input("Hvilken tabell vil du slette i?: ")
    victim = input("Hva vil du slette?: ")
    sql = f"DELETE FROM {table} WHERE navn = %s"
    mycursor.execute(sql, victim)

  #avslutter program med enkel melding
  case "q":
    print("Du avsluttet")

print("\nHa det på badet.")