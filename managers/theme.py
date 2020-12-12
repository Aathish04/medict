 
import PySimpleGUI as sg 
if __name__=="__main__":
    from _config import set_settings_config
else:
    from ._config import set_settings_config
  
class ThemeManager:
  
    layout = [[sg.Text('List of InBuilt Themes')], 
              [sg.Text('Please Choose a Theme  to see Demo window')], 
              [sg.Listbox(values = sg.theme_list(), 
                          size =(20, 12), 
                          key ='THEMELIST', 
                         enable_events = True)],
              [sg.Button(button_text="Set Theme",button_color=("white","blue"),size=(18,1),key='THEMEBTN')]
             ]
    def set_theme(self,theme):
        settings={}
        settings['theme']=theme
        set_settings_config(settings)
        
        
if __name__=="__main__":
    thememanager=ThemeManager()

    window = sg.Window('Theme List',thememanager.layout) 
  
    # This is an Event Loop 
    while True:   
        event, values = window.read() 
      
        if event in (None, 'Exit'): 
            break
          
        sg.theme(values['-LIST-'][0]) 
        sg.popup_get_text('This is {}'.format(values['-LIST-'][0])) 
      
    # Close 
    window.close() 
