import pygame as pg
import time
import random

pg.init()
#loading sounds:
#crash_sound = pg.mixer.Sound("Crash.wav")
#pg.mixer.music.load('Sand_Castle.wav')
display_width = 800
display_length = 600
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
no_color = (-1, -1, -1)
color = white
dodged_count = 0
car = pg.image.load('racecar.png')
icon = car
window = pg.display.set_mode((display_width, display_length))
#commenting this line is not needed at all
#window = pg.display.set_mode((0, 0))
pg.display.set_caption('helloworld')
pg.display.set_icon(icon)
clock = pg.time.Clock()


def pos_car(x, y):
    window.blit(car, (x, y))


def add_boundary(color):
    pg.draw.rect(window, color, [0, 0, 0.15* display_width, display_length], 10)
    pg.draw.rect(window, color, [0.85* display_width, 0, 0.15 * display_width, display_length], 10)


def draw_obstacle(posx, posy, sizex, sizey, color):
    pg.draw.rect(window, color, [posx, posy, sizex, sizey])


def draw_objects(posx, posy, sizex, sizey, n, color):
    for index in range(0, n+1):
        draw_obstacle(posx[index], posy[index], sizex, sizey, color= color)


def text_objects(text , font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, color, back_col, font_size, position):
    message_font = pg.font.Font('freesansbold.ttf', font_size)
    text_surf , text_rect = text_objects(text, message_font, color= color)
    text_rect.center = ((position[0]+position[2]//2), (position[1]+ position[3]//2))
    if back_col != no_color:
        window.fill(back_col)
    window.blit(text_surf, text_rect)
    pg.display.update(position)
    #time.sleep(2)
    #pg.display.update()


def obs_crash(obsx, obsy, x, y, obsh, obsw, n):
    for index in range(0, n+1):
        if(obsy[index] < display_length and (abs(y - obsy[index]) < obsh) and (obsx[index] - x <=70 and obsx[index] - x >0 or x-obsx[index] >0 and x - obsx[index] <= obsw)):
            return True
    return False


def print_progress(count, wave):
    font = pg.font.SysFont(None, 25)
    text = font.render('Dodged: ' + str(count), True, black)
    text2 = font.render('Wave: ' + str(wave), True, black)
    #window.blit(text, (display_width//2, 0))
    window.blit(text2, (display_width//2, 0))


def button(text, t_size, pos, type, color):
    mouse_pointer = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    returner = False
    insider = 0
    x = mouse_pointer[0]
    y = mouse_pointer[1]
    if type == 1:
        if (x > pos[0] and x < pos[0]+pos[2] and y > pos[1] and y < pos[1]+pos[3]):
            pg.draw.rect(window, white, pos)
            pg.draw.rect(window, color, pos, 10)
            insider += 1
        else:
            pg.draw.rect(window, color, pos)
    else:
        if (x > pos[0] and x < pos[0] + pos[2] and y > pos[1] and y < pos[1] + pos[3]):
            pg.draw.rect(window, color, pos)
            insider += 1
        else:
            pg.draw.rect(window, white, pos)
            pg.draw.rect(window, color, pos, 10)
    if click[0] == 1 and insider == 1:
        returner = True
    message_display(text, black, no_color, t_size, pos)
    return returner


def intro(text, b1_text, b2_text, color, back_color):
    #pg.mixer.music.stop()
    message_display(text= text, color = color, back_col= back_color, font_size= 100, position= (0, 0, display_width, display_length))
#event handling
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    return True
        if button(b1_text, 20, (100, 400, 100, 50), 1, green):
            return True
        if button(b2_text, 20, (600, 400, 100, 50), 2, red):
            return False
        #pg.display.update()
        clock.tick(60)


def game_loop():
    #pg.mixer.music.play(-1)
    x = display_width * 0.45
    y = display_length - 80
    x_change = 0
    game_exit = False
    moving = 0
    obsw = 100
    obsh = 100
    obsx = [200]
    obsy = [-100]
    n = 4
    #setting obsx[] and obsy[]
    for index in range(0, n+1):
        obsx.append(random.randrange(int(0.155 * display_width), int(display_width * 0.85) - obsw))
        obsy.append(random.randrange(1, 15)* -100)

    obs_speed = 2
    global dodged_count
    wave_count = 0
    while not game_exit:
        #event_handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
                value = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x_change = -5
                    moving = -1
                if event.key == pg.K_RIGHT:
                    x_change = 5
                    moving = 1
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and moving == -1 or event.key == pg.K_RIGHT and moving == 1:
                    x_change = 0
                    moving = 0
                if event.key == pg.K_p:
                    if intro('Paused', 'Resume', 'Quit!', red, no_color):
                        pass
                    else:
                        game_exit = True
                        value = False
                if event.key == pg.K_q:
                    game_exit = True
                    value = False

            #print(event)
        #moving it
        x += x_change

        #safe range white background
        if x <= (0.8 * display_width) and x >= (0.1* display_width):
            color = white
            #dodgded count obs y rest obs x reset
            inside = False
            for index in range(0, n+1):
                if(obsy[index] <= display_length):
                    #some block is inside
                    obsy[index] += obs_speed
                    inside = True
            if inside:
                draw_objects(obsx, obsy, obsw, obsh, n= n, color = yellow)
            else:
                #n = random.randrange(2, 6)
                wave_count += 1
                obs_speed += 1
                for index in range(0, n + 1):
                    obsx[index] = random.randrange(int(0.155 * display_width), int(display_width * 0.85) - obsw)
                    obsy[index] = (random.randrange(1, 15)) * -100

            # whether or not car crashes into the block
            if obs_crash(obsx, obsy, x, y, obsh, obsw, n):

                #pg.mixer.music.stop()
                #pg.mixer.Sound.play(crash_sound)

                message_display('CRASHHEDDD!!', black, yellow, font_size= 100, position= (0, 0, display_width, display_length))
                print_progress(dodged_count, wave= wave_count)
                #draw_obstacle(obsx, obsy, obsw, obsh, red)
                draw_objects(obsx, obsy, obsw, obsh, n=n, color = red)
                pos_car(x, y)
                pg.display.update()
                time.sleep(1)
                game_exit = True
                value = True
            else:
                window.fill(color)
                pos_car(x, y)
                add_boundary(red)
                print_progress(dodged_count, wave_count)
                draw_objects(obsx, obsy, obsw, obsh, n=n, color=yellow)
                pg.display.update()

        # crash happened due to out of bounds
        else:
            #pg.mixer.music.stop()
            #pg.mixer.Sound.play(crash_sound)
            message_display('CRASHHEDDD!!', black, yellow, font_size= 100, position= (0, 0, display_width, display_length))
            time.sleep(1)
            game_exit = True
            value = True
        clock.tick(60)
    return value


if intro('Game  1', 'Start', 'Quit!', green, white) and game_loop():
    dodged_count = 0
    message_display('Restarting......', white, red, font_size= 100, position= (0, 0, display_width, display_length))
    time.sleep(1)
    while intro('Game 1', 'Start\nover', 'Quit!', yellow, red) and game_loop() is True:
        dodged_count = 0
        message_display('Restarting......', white, red, font_size= 100, position= (0, 0, display_width, display_length))
        time.sleep(1)
    pass
pg.quit()