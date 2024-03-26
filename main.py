import PySimpleGUI as sg


class Interface:
    def __init__(self) -> None:
        self.layout = self.__set_layout()
        self.window = self.__create_window()

    def __set_layout(self) -> list:
        return [
            [sg.Text('Hello, World!')],
            [sg.Button('Clique aqui')]
        ]

    def __create_window(self) -> sg.Window:
        return sg.Window('Calculadora de Coisas', self.layout, resizable=True, icon='./files/icon.ico',
                         font=('@Microsoft JhengHei UI Light', 12, 'normal'), text_justification='center', element_justification='left',
                         background_color='#FFFFFF', default_button_element_size=(5, 10), button_color='#FAFAFA',
                         # right_click_menu=[],
                         return_keyboard_events=True, print_event_values=True, size=(320, 470))


calculator = Interface()
while True:
    calculator.event, calculator.values = calculator.window.read()

    if calculator.event == sg.WIN_CLOSED:
        break
