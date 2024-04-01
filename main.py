import PySimpleGUI as sg


class Interface:
    def __init__(self) -> None:
        # Visor da calculadora
        self.title = sg.Text('Calculadora', pad=(2, 7), key='title', expand_x=True, justification='left',
                             colors=('#000000', '#FFFFFF'), font=('Bahnschrift', 18, 'bold'))
        self.display = sg.Text('0', pad=(3, (0, 5)), key='display', expand_x=True, justification='right',
                               colors=('#000000', '#C3EBEB'), font=('System', 36, 'bold'))

        # Botões númericos
        self.zero = sg.Button('0', size=(7, 2), pad=2, key='0', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))
        self.one = sg.Button('1', size=(7, 2), pad=2, key='1', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.two = sg.Button('2', size=(7, 2), pad=2, key='2', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.three = sg.Button('3', size=(7, 2), pad=2, key='3', target='display',
                               mouseover_colors=('#000000', '#F5F5F5'))
        self.four = sg.Button('4', size=(7, 2), pad=2, key='4', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))
        self.five = sg.Button('5', size=(7, 2), pad=2, key='5', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))
        self.six = sg.Button('6', size=(7, 2), pad=2, key='6', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.seven = sg.Button('7', size=(7, 2), pad=2, key='7', target='display',
                               mouseover_colors=('#000000', '#F5F5F5'))
        self.eight = sg.Button('8', size=(7, 2), pad=2, key='8', target='display',
                               mouseover_colors=('#000000', '#F5F5F5'))
        self.nine = sg.Button('9', size=(7, 2), pad=2, key='9', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))

        # Outros botões
        self.clear = sg.Button('C', size=(7, 2), pad=2, key='clear', target='display',
                               mouseover_colors=('#000000', '#F5F5F5'))
        self.add = sg.Button('+', size=(7, 2), pad=2, key='addition', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.sub = sg.Button('-', size=(7, 2), pad=2, key='subtraction', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.mult = sg.Button('*', size=(7, 2), pad=2, key='multiplication', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))
        self.div = sg.Button('/', size=(7, 2), pad=2, key='division', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.perc = sg.Button('%', size=(7, 2), pad=2, key='percent', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))
        self.sqrt = sg.Button('√', size=(7, 2), pad=2, key='sq_root', target='display',
                              mouseover_colors=('#000000', '#F5F5F5'))
        self.sqr = sg.Button('^', size=(7, 2), pad=2, key='square', target='display',
                             mouseover_colors=('#000000', '#F5F5F5'))
        self.equal = sg.Button('=', size=(7, 2), pad=2, key='equal', target='display',
                               mouseover_colors=('#000000', '#F5F5F5'))
        self.comma = sg.Button(',', size=(7, 2), pad=2, key='comma', target='display',
                               mouseover_colors=('#000000', '#F5F5F5'))

        # Parâmetros úteis
        # image_source = str | image_subsample = int | image_zoom = int

        self.layout = self.__set_layout()
        self.window = self.__create_window()

    def __set_layout(self) -> list:
        return [
            [self.title],
            [self.display],
            [self.clear, self.perc, self.sqrt, self.sqr],
            [self.seven, self.eight, self.nine, self.div],
            [self.four, self.five, self.six, self.mult],
            [self.one, self.two, self.three, self.sub],
            [self.zero, self.comma, self.equal, self.add]
        ]

    def __create_window(self) -> sg.Window:
        return sg.Window('Calculadora de Coisas', self.layout, resizable=True, print_event_values=True,
                         icon='./files/icon.ico', font=('Terminal', 12, 'normal'), text_justification='center',
                         element_justification='left', background_color='#FFFFFF', button_color=('#000000', '#FAFAFA'))


calc = Interface()
while True:
    not_number = ['clear', 'addition', 'subtraction', 'multiplication',
                  'division', 'percent', 'sq_root', 'square', 'equal', 'comma']
    calc.event, calc.values = calc.window.read()

    if calc.event == sg.WIN_CLOSED:
        break

    display = calc.window['display']
    display_text = display.DisplayText

    if calc.event not in not_number and len(display_text) < 15:
        if display_text == '0':
            display.update(calc.event)
        if display_text != '0':
            display.update(f'{display_text}{calc.event}')

    match calc.event:
        case 'clear':
            display.update('0')
        case 'addition':
            display.update('+')
        case 'subtraction':
            display.update('-')
        case 'multiplication':
            display.update('*')
        case 'division':
            display.update('/')
        case 'percent':
            display.update('%')
        case 'sq_root':
            display.update('√')
        case 'square':
            display.update('^')
        case 'equal':
            display.update('=')
        case 'comma':
            if ',' not in display_text:
                display.update(f'{display_text},')
