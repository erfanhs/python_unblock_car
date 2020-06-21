import pygame
from tkinter import Tk
from tkinter import messagebox
import ast
import os

from car import Car


def getSelectedCar(event):
    for car in Car.cars:
        rect = car.rect
        if rect.collidepoint(event.pos):
            mouse_x, mouse_y = event.pos
            offset_x = rect.x - mouse_x
            offset_y = rect.y - mouse_y
            return (car, offset_x, offset_y)
 

Tk().wm_withdraw()
pygame.init()


window_size = (300, 300)


screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('python unblock car')

background = pygame.image.load(os.path.join('images', 'asphalt.jpeg'))
background = pygame.transform.scale(background, window_size)


stages = ast.literal_eval(open('stages.json').read())
last_stage = open('laststage').read()

for x, y, width, height in stages[last_stage]:
    Car(x, y, width, height)


draging_car = None


while True:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()



        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                SelectedCar = getSelectedCar(event)
                if SelectedCar: 
                    draging_car, offset_x, offset_y = SelectedCar




        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                
                if not draging_car:
                    continue

                rounded_x, rounded_y = draging_car.round()

                # x
                rect_x = draging_car.rect.x
                rect_w = draging_car.rect.width
                if rect_x <= 0: rect_x = 0
                else:
                    if rect_w == 150:
                        if rounded_x >= 150: rect_x = 150
                        else: rect_x = rounded_x
                    elif rect_w == 50:
                        if rounded_x >= 250: rect_x = 250
                        else: rect_x = rounded_x
                    elif rect_w == 100:
                        if rounded_x >= 200:
                            if draging_car.is_main:
                                if last_stage == str(len(stages) - 1):
                                    messagebox.showinfo('won', 'you won the game.\nGame Over ! Thank you for playing.')
                                    with open('laststage', 'w') as laststage_file:
                                        laststage_file.write('1')
                                        laststage_file.close()
                                    pygame.quit()
                                else:
                                    last_stage = str(int(last_stage) + 1)
                                    with open('laststage', 'w') as laststage_file:
                                        laststage_file.write(last_stage)
                                        laststage_file.close()
                                    Car.cars.clear()
                                    r = messagebox.askquestion("won","you won the game ! next stage ?")
                                    if r == 'no':
                                        pygame.quit()
                                    for x, y, width, height in stages[last_stage]:
                                        Car(x, y, width, height)
                            else:
                                rect_x = 200
                        else: rect_x = rounded_x
                draging_car.rect.x = rect_x


                # y
                rect_y = draging_car.rect.y
                rect_h = draging_car.rect.height
                if rect_y <= 0: rect_y = 0
                else:
                    if rect_h == 150:
                        if rounded_y >= 150: rect_y = 150
                        else: rect_y = rounded_y
                    elif rect_h == 50:
                        if rounded_y >= 250: rect_y = 250
                        else: rect_y = rounded_y
                    elif rect_h == 100:
                        if rounded_y >= 200: rect_y = 200
                        else: rect_y = rounded_y
                draging_car.rect.y = rect_y


                draging_car = None





        elif event.type == pygame.MOUSEMOTION:

            if draging_car:
                mouse_x, mouse_y = event.pos
                new_y = mouse_y + offset_y
                new_x = mouse_x + offset_x

                draging_car.move(new_x, new_y)


        pygame.display.update()



    # set background image (parking asphalt)
    screen.blit(background, background.get_rect())
    
    # put cars in parking
    for car in Car.cars: car.show(screen)

    pygame.display.flip()