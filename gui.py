import PySimpleGUI as sg
import database

def gui():
  tablesnames = database.tableNames()
  # todo: add exit, clear buttons.
  database.numOwners()

  layout = [
          [sg.Text("Function:"), sg.Radio("MAX", "agg", default=False, key="-MAX-"), sg.Radio("MIN", "agg", default=False, key="-MIN-"), sg.Radio("AVG", "agg", default=False, key="-AVG-")],
          [sg.Text("Chain"), sg.Radio(tablesnames[0], "ALL", default=False, key="-IN1-"), sg.Radio(tablesnames[1], "ALL", default=False, key="-IN2-"), sg.Radio(tablesnames[2], "ALL", default=False, key="-IN3-"), sg.Radio(tablesnames[3], "ALL", default=False, key="-IN4-")],
          [sg.Button("Submit"), sg.Button("Reset")],
          [sg.Output(size=(40, 20))]
          ]

  # Create the window
  window = sg.Window('Opensea NFT Statistics', layout, size=(400,400))

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

  window.close()