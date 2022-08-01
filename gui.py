import PySimpleGUI as sg
import database

def gui():
  print(database.findHighest24h())
  layout = [[sg.Text(database.findHighest24h())], [sg.Button("OK")]]

  # Create the window
  window = sg.Window("Demo", layout)

  # Create an event loop
  while True:
      event, values = window.read()
      # End program if user closes window or
      # presses the OK button
      if event == "OK" or event == sg.WIN_CLOSED:
          break

  window.close()