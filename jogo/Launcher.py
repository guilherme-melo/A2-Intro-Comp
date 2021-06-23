import pygame_menu
from pygame_menu import sound
from pygame_menu.examples import create_example_window
from main import J


surface = create_example_window('Corona Runaway', (823,759))
surface2 = create_example_window('Corona Runaway', (823,759))


# Implementa a fonte escolhida
font = pygame_menu.font.FONT_8BIT

# Tipo de barra
barra = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL


# Tema do jogo e especificações do fundo
mytheme = pygame_menu.themes.Theme(widget_font=font,
                                   title_bar_style = barra,
                                   widget_selection_effect=pygame_menu.widgets.HighlightSelection())

myimage = pygame_menu.baseimage.BaseImage(
    image_path='imagens/fundo.png',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

mytheme.background_color = myimage


# menu 1
menu = pygame_menu.Menu(
    height=759,
    theme=mytheme,
    title='Corona Runaway',
    width=823
)

# menu 2
menu2 = pygame_menu.Menu(
    height=759,
    theme=mytheme,
    title='Como jogar',
    width=823
)

# Frases do menu 2
como_jogar = ['NAO SEJA ESMAGADO',
              'PELO TETO',
              '',
              'APERTE P PARA PAUSAR',
              '',
              'Pressione as setas',
              'LEFT e RIGHT',
              'para se mover'
              ]



for m in como_jogar:
        print(m)

for m in como_jogar:
        menu2.add.label(m, align=pygame_menu.locals.ALIGN_CENTER)
        menu2.add.vertical_margin(25)


# Trinca RGB da cor usada de background para os botões
azul_claro = (51, 172, 255)


# Adicionando som
engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'sons/mouse-click.mp3')
engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, 'sons/keyboard.mp3')
engine.set_sound(sound.SOUND_TYPE_KEY_DELETION, 'sons/keyboard.mp3')


# Botões da surface 1 (Início do jogo)
user_name = menu.add.text_input('Nome: ', maxchar=10, background_color = azul_claro)

menu.add.button('Jogar', J.loop, background_color = azul_claro)
menu.add.button('Como jogar', menu2, background_color = azul_claro)
menu.add.button('Sair', pygame_menu.events.EXIT, background_color = azul_claro)
menu.set_sound(engine, recursive=True)


# Botões da surface 2 (Como jogar)
menu2.add.button('Voltar', pygame_menu.events.BACK, background_color = azul_claro)
menu2.set_sound(engine, recursive=True)


menu.mainloop(surface)
menu2.mainloop(surface2)




