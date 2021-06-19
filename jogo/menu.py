import pygame_menu
from pygame_menu import sound
from pygame_menu.examples import create_example_window
from Trabalho_A2 import J


surface = create_example_window('Corona Runaway', (600, 600))
surface2 = create_example_window('Corona Runaway', (600, 600))
surface3 = create_example_window('Corona Runaway', (600, 600))

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
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER,
)

mytheme.background_color = myimage


# menu 1
menu = pygame_menu.Menu(
    height=600,
    theme=mytheme,
    title='Corona Runaway',
    width=600
)

# menu 2
menu2 = pygame_menu.Menu(
    height=600,
    theme=mytheme,
    title='Como jogar',
    width=600
)

# Frases do menu 2
como_jogar = ['A BOLA NAO PODE',
              'SAIR DA TELA',
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


# menu 3
menu3 = pygame_menu.Menu(
    height=600,
    theme=mytheme,
    title='Corona Runaway',
    width=600
)

# Frase do menu 3
jogo_acabou = ['VOCE PERDEU']

for w in jogo_acabou:
        print(w)

for w in jogo_acabou:
        menu3.add.label(w, align=pygame_menu.locals.ALIGN_CENTER)
        menu3.add.vertical_margin(25)


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
# menu.add.button('menu 3', menu3, background_color = azul_claro)
menu.set_sound(engine, recursive=True)


# Botões da surface 2 (Como jogar)
menu2.add.button('Voltar', pygame_menu.events.BACK, background_color = azul_claro)
menu2.set_sound(engine, recursive=True)


# Botões da surface 3 (Fim de jogo)
# Aqui a gente puxa do módulo principal a função pra quando o jogador perder
menu3.add.button('Jogar novamente', J.loop, background_color = azul_claro)
menu3.add.button('Sair', pygame_menu.events.EXIT, background_color = azul_claro)
menu3.set_sound(engine, recursive=True)


menu.mainloop(surface)
menu2.mainloop(surface2)
menu3.mainloop(surface3)
