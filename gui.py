import PySimpleGUI as sg
import database

def gui():
  tablesnames = database.tableNames()

  layout = [
          [sg.T("         "), sg.Radio(tablesnames[0], "ALL", default=False, key="-IN1-")],
          [sg.T("         "), sg.Radio(tablesnames[1], "ALL", default=False, key="-IN2-")],
          [sg.T("         "), sg.Radio(tablesnames[2], "ALL", default=False, key="-IN3-")],
          [sg.T("         "), sg.Radio(tablesnames[3], "ALL", default=False, key="-IN4-")],
          [sg.T("")],[sg.T("        "), sg.Button("Submit"), sg.Button("Reset")], [sg.T("")],
          [sg.Output(size=(40, 20))]
          ]

  # Create the window
  #window = sg.Window("Demo", layout)
  window = sg.Window('Push my Buttons', layout, size=(800,400))

  # Create an event loop
  while True:
      event, values = window.read()
      # End program if user closes window or
      # presses the OK button
      if event == "OK" or event == sg.WIN_CLOSED:
          break
      elif event == 'Reset':
        window["-IN1-"].reset_group()
      elif values["-IN1-"] == True:
        print(database.findHighest24h(tablesnames[0]))
      elif values["-IN2-"] == True:
        print("Hello World")
      elif values["-IN3-"] == True:
        print("Hello World")
      elif values["-IN4-"] == True:
        print("Hello World")
      

  window.close()