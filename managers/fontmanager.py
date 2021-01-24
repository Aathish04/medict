import PySimpleGUI as sg
if __name__=="__main__":
    from _config  import set_settings_config
    from _config import get_settings_config
else:
    from ._config import set_settings_config    
    from ._config import get_settings_config     


class FontManager:
    fontSize= int(get_settings_config()["fontsize"])
    layout = [[sg.Spin([sz for sz in range(12, 21)], font=('Helvetica 20'), initial_value=fontSize,key="FONTSPIN",change_submits=True),
               sg.Text("Aa", size=(2, 1), font="Helvetica "  + str(fontSize), key="FontPreview")]]
    def set_fontsize(self,fontsize):
        settings={}
        settings['fontsize']=str(fontsize)
        set_settings_config(settings)

if __name__=="__main__":    
    fontmanager=FontManager()
    window = sg.Window("Font size selector", fontmanager.layout, grab_anywhere=False)
    # Event Loop
    while True:
        event, values= window.read()
        if event == sg.WIN_CLOSED:
             break
        else:
               print(event)
        sz_spin = int(values['FONTSPIN'])
        fontSize = sz_spin
        font = "Helvetica "  + str(fontSize)
        window["FontPreview"].update(font=font)
        window['FONTSPIN'].update(sz_spin)



