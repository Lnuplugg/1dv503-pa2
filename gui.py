import PySimpleGUI as sg
import database

def gui():
  tablesnames = database.tableNames()
  # todo: add exit, clear buttons.
  
  layout = [
          [sg.Text("Function:"), sg.Radio("MAX", "agg", default=False, key="-MAX-"), sg.Radio("MIN", "agg", default=False, key="-MIN-"), sg.Radio("AVG", "agg", default=False, key="-AVG-")],
          [sg.Text("")],
          [sg.Text("Chain:"), sg.Radio(tablesnames[0], "ALL", default=False, key="-IN1-"), sg.Radio(tablesnames[1], "ALL", default=False, key="-IN2-"), sg.Radio(tablesnames[2], "ALL", default=False, key="-IN3-"), sg.Radio(tablesnames[3], "ALL", default=False, key="-IN4-")],
          [sg.Text("")],
          [sg.Text('Search collection(ex alien, crypto, ape)')],
          [sg.Text('Collection:', size =(10, 1)), sg.InputText()],
          [sg.Text("")],
          [sg.Radio("Show top 5 ranked collections", "ALL", default=False, key="-top5-")],
          [sg.Text("")],
          [sg.Button("Submit"), sg.Button("Reset")],
          [sg.Output(size=(60, 20))]
          ]

  # Create the window
  window = sg.Window('Opensea NFT Statistics', layout, size=(600,500))

  # Create an event loop
  while True:
      event, values = window.read()
      # End program if user closes window or
      # presses the OK button
      if event == "OK" or event == sg.WIN_CLOSED:
          break

      if event == 'Reset':
        window["-IN1-"].reset_group()
    
    # Single table aggregations:
      elif values["-MAX-"] == True:
        aggregation = "MAX"
        prefix = "Highest 24h: "

        if values["-IN1-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[0]))
        elif values["-IN2-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[1]))
        elif values["-IN3-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[2]))
        elif values["-IN4-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[3]))

      elif values["-MIN-"] == True:
        aggregation = "MIN"
        prefix = "Lowest 24h: "

        if values["-IN1-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[0]))
        elif values["-IN2-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[1]))
        elif values["-IN3-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[2]))
        elif values["-IN4-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[3]))

      elif values["-AVG-"] == True:
        aggregation = "AVG"
        prefix = "Average 24h: "

        if values["-IN1-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[0]))
        elif values["-IN2-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[1]))
        elif values["-IN3-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[2]))
        elif values["-IN4-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[3]))
    # End Single table aggregations.

      # Find collection name.
      if values[0]:
        matches = []

        if values["-IN1-"]  == True:
          matches = database.findCollectionName(tablesnames[0], values[0])
        elif values["-IN2-"] == True:
          matches = database.findCollectionName(tablesnames[1], values[0])
        elif values["-IN3-"] == True:
          matches = database.findCollectionName(tablesnames[2], values[0])
        elif values["-IN4-"] == True:
          matches = database.findCollectionName(tablesnames[3], values[0])
        else:
          print("Select a blockchain")

        # Print collection matches
        if len(matches[1]) > 0:
          print(matches[0] + ": " )
          for match in matches[1]:
            print(match)

        else:
          print("No Matches")
          
      # Display the top 5 collections across all blockchains.
      if values["-top5-"] == True:
        collections = database.top5RankedCollections()
        
        for collection in collections:
          print("Rank: " + str(collection[0]))
          print(f" {tablesnames[0]}\n  Name: {collection[1]}\n  Number of owners: {str(collection[2])}\n")
          print(f" {tablesnames[1]}\n  Name: {collection[4]}\n  Number of owners: {str(collection[5])}\n")
          print(f" {tablesnames[2]}\n  Name: {collection[7]}\n  Number of owners: {str(collection[8])}\n")
          print(f" {tablesnames[3]}\n  Name: {collection[10]}\n  Number of owners: {str(collection[11])}\n")


  window.close()