import pygame as pg
import random
import time

pg.init()
window =  pg.display.set_mode((800, 600))
display_width = 800
display_length = 600
pg.display.set_caption('Ginger')
clock = pg.time.Clock()

# colors
cyan = (15, 123, 115)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
lilac = (157, 43, 142)
pink = (240, 32, 100)
no_color = (-1, -1, -1)
n = 4


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


def eat(x, y, pos):
    xs = pos[0] - x
    ys = pos[1] - y
    global n
    if((ys * ys)+ (xs * xs) < (400)):
        x = random.randrange(50, 750)
        y = random.randrange(50, 550)
        n += 1
    return x, y


def is_cut(list):

    for pos in list[2:]:
        xs = list[0][0] - pos[0]
        ys = list[0][1] - pos[1]
        if ((ys * ys) + (xs * xs) < (400)):
            return True
        else:
            pass
    return False


def game_loop():
    in_game = True
    move = [0, 0]
    move_list = [move]
    position = [0, 250]
    position_list = [position]
    x = random.randrange(50, 750)
    y = random.randrange(50, 550)
    pauser = 150
    global count
    window.fill(white)
    pg.display.update()

    num  = n
    value = True
    while(in_game == True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                in_game = False
                value = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT and move != [-1, 0]:
                    move = [1, 0]
                    break
                    # pg.time.delay(30)
                elif event.key == pg.K_LEFT and move != [1, 0]:
                    move = [-1, 0]
                    break
                    # pg.time.delay(30)
                elif event.key == pg.K_UP and  move != [0, 1]:
                    move = [0, -1]
                    break
                    # pg.time.delay(30)
                elif event.key == pg.K_DOWN and move != [0, -1]:
                    move = [0, 1]
                    break
                    # pg.time.delay(30)
                if event.key == pg.K_q:
                    in_game = False
                    value = False
                if event.key == pg.K_p:
                    if not intro(text = 'PAUSED', b1_text='RESUME', b2_text='Quit', color = black, back_color=no_color):
                        in_game = False
                        value = False

        # moving the snakes position
        for pos, mov in zip(position_list, move_list):
            pos[0] += (mov[0] * 20)
            pos[1] += (mov[1] * 20)
            # wrapping
            if pos[1]< 0:  # for upper line
                pos[1] += 600
            if pos[1] > 600:  # for bottom line
                pos[1] -= 600
            if pos[0] < 0:  # for left
                pos[0] += 780
            if pos[0] > 780:  # for right
                pos[0] -= 800
        # shift the move values by one position
        index = len(move_list) - 1
        while index > 0:
            move_list[index] = move_list[index - 1]
            index -= 1
        # moving the head only
        move_list[0] = move
        position = position_list[0]


        # eat?
        x, y = eat(x, y, position)
        if n > num:
            num = n
            count += 1
            if pauser > 60:
                pauser -= 10
            alpha = position_list[-1]
            position_list.append([alpha[0], alpha[1]])
            move_list.append([0, 0])

        # checking for cut
        if is_cut(position_list):
            in_game = False
            value = True

        # drawing
        window.fill((255, 157, 206))
        # print the progress
        font = pg.font.SysFont(None, 25)
        text2 = font.render('Eaten: ' + str(count), True, black)
        window.blit(text2, (display_width // 2, 0))

        # drawing the fruit
        # pg.draw.rect(window, yellow, (x, y, 20, 20))
        pg.draw.circle(window, green, (x+10, y+10), int(12))

        # Drawing the snake
        for pos in position_list[1:]:
            pg.draw.rect(window, cyan, (pos[0], pos[1], 20, 20))

        # marking the head
        tail_x = position_list[-1][0]
        tail_y = position_list[-1][1]
        # pg.draw.polygon(window, yellow, [(tail_x+20, tail_y), (tail_x, tail_y+10), (tail_x+20, tail_y+20)])

        pg.draw.rect(window, yellow, (tail_x, tail_y, 20, 20))
        pg.draw.rect(window, red, (position_list[0][0], position_list[0][1], 20, 20))
        # print(position_list[-1])


        # update screen
        pg.display.update()
        pg.time.delay(pauser)
        clock.tick(60)
        pass
    return value


if __name__ == '__main__':
    count = 0
    if intro('Game  1', 'Start', 'Quit!', green, (240, 32, 100)) and game_loop():
        count = 0
        pg.time.delay(2000)

        message_display('Restarting......', pink, black, font_size= 100, position= (0, 0, display_width, display_length))
        time.sleep(0.5)
        while intro('Game 1', 'Start over', 'Quit!', yellow, (240, 32, 100)) and game_loop() is True:
            count = 0
            pg.time.delay(2000)

            message_display('Restarting......', black, cyan, font_size= 100, position= (0, 0, display_width, display_length))
            time.sleep(0.5)
        pass
pg.quit()