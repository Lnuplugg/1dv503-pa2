from mysql.connector import connect, Error
import pandas as pd
import numpy as np
import gui

try:
  db = connect(
    host="localhost",
    user="debian-sys-maint",
    password="Ymt634UhHtP8umg7"
  )
  dbName = "Andersson"
  
  cursor = db.cursor(buffered=True)

except Error as e:
  print(e)

def tableNames():
  return ['Ethereum', 'Polygon', 'Klaytn', 'Solana']

# Read csv files and replace all nan values in the dataframe with None, 
# translates to NULL in the database.
def readCsv():
  eth = pd.read_csv('datasets/eth-data.csv')
  poly = pd.read_csv('datasets/poly-data.csv')
  klaytn = pd.read_csv('datasets/klaytn-data.csv')
  solana = pd.read_csv('datasets/solana-data.csv')

  eths = eth.replace(np.nan, None)
  polys = poly.replace(np.nan, None)
  klaytn = klaytn.replace(np.nan, None)
  solana = solana.replace(np.nan, None)

  return [eths, polys, klaytn, solana]

def createDatabase():
  db = showDatabase()
  
  if db == None:
    inputData = readCsv()

    cursor.execute("CREATE DATABASE " + dbName)
    createTables(inputData)
    insertData()
    print("Database " + dbName + " created.")
  else:
    gui.gui()

def showDatabase():
  cursor.execute("SHOW DATABASES")

  for db in cursor:
    if db == (dbName,):
      return db

def createTables(csv):
  tableNamesArray = tableNames()

  i = 0
  for df in csv:
    cursor.execute("CREATE TABLE " + dbName + " . " + tableNamesArray[i] + "(" +
    csv[i].columns[0] + " int," +
    csv[i].columns[1] + " varchar(100) PRIMARY KEY," +
    csv[i].columns[2] + " varchar(400)," +
    csv[i].columns[3] + " varchar(100)," +
    csv[i].columns[4] + " float," +
    csv[i].columns[5] + " int," +
    csv[i].columns[6] + " int," +
    csv[i].columns[7] + " float," +
    csv[i].columns[8] + " float," +
    csv[i].columns[9] + " float," +
    csv[i].columns[10] + " float," +
    csv[i].columns[11] + " float," +
    csv[i].columns[12] + " float)")
    i += 1

#Creating attributes and inserting values into respective tables.
def insertData():
  csv = readCsv()
  fieldNamesArray = tableNames()
  
  try:
    attributeIndex = 0
    for i in fieldNamesArray:
      attributes = "`,`".join([str(i) for i in csv[attributeIndex].columns.tolist()])

      # Commit each row in a file(dataframe) to database.
      for j, row in csv[attributeIndex].iterrows():
          sql = "INSERT INTO `Andersson` . " + i + "(`" + attributes + "`) VALUES (" + "%s," * (len(row)-1) + "%s)"
          cursor.execute(sql, tuple(row))
          db.commit()
      attributeIndex += 1
  except Error as e:
    print(e)

# Aggregation MAX, MIN, AVG from gui.
def change24h(aggregation, table):
  query = "SELECT "+ aggregation + "(oneDayChange) FROM " + dbName + ' . ' + table
  cursor.execute(query)
  highest = cursor.fetchone()

  # Return procent
  return str(highest[0] * 100) + "%"

def findCollectionName(chain, searchInput):
    query = f"SELECT {chain}.name FROM {dbName} . {chain} WHERE {chain}.name LIKE '%{searchInput}%'"
    cursor.execute(query)
    collectionMatches = cursor.fetchall()

    return chain, collectionMatches

# JOIN's tables to retrieve the top5 collections accross all blockchains.
def top5RankedCollections():
  query = (
    f"SELECT Ethereum.ranking, Ethereum.name, Ethereum.numOwners, Polygon.ranking, Polygon.name, Polygon.numOwners, Klaytn.ranking, Klaytn.name, Klaytn.numOwners, Solana.ranking, Solana.name, Solana.numOwners FROM " 
    f"{dbName} . Ethereum "
    f"JOIN {dbName} . Polygon ON Ethereum.ranking = Polygon.ranking "
    f"JOIN {dbName} . Klaytn ON Polygon.ranking = Klaytn.ranking "
    f"JOIN {dbName} . Solana ON Klaytn.ranking = Solana.ranking "
    f"ORDER BY Ethereum.ranking, Polygon.ranking, Klaytn.ranking, Solana.ranking"
  )

  cursor.execute(query)
  top5 = cursor.fetchmany(size=5)

  return top5

#readCsv()
createDatabase()
#insertData()