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
  eth = pd.read_csv('1dv503-pa2/datasets/eth-data.csv')
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
    csv[i].columns[0] + " varchar(100) PRIMARY KEY," +
    csv[i].columns[1] + " varchar(400)," +
    csv[i].columns[2] + " varchar(100)," +
    csv[i].columns[3] + " float," +
    csv[i].columns[4] + " int," +
    csv[i].columns[5] + " int," +
    csv[i].columns[6] + " float," +
    csv[i].columns[7] + " float," +
    csv[i].columns[8] + " float," +
    csv[i].columns[9] + " float," +
    csv[i].columns[10] + " float," +
    csv[i].columns[11] + " float)")
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

def findHighest24h(table):
  # query = "SELECT name, oneDayChange FROM " + dbName + ". Ethereum WHERE oneDayChange > 0"

  query = "SELECT MAX(oneDayChange) FROM " + dbName + ' . ' + table
  cursor.execute(query)
  highest = cursor.fetch()
  print(highest)

  # Return procent
  return highest[0] * 100

readCsv()
#createDatabase()
#insertData()