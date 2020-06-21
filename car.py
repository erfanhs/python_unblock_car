import os
import pygame


class Car:

    __cars_img = {
        (100, 50): '1.png',
        (150, 50): '2.png',
        (50, 100): '3.png',
        (50, 150): '4.png'
    }

    __SPEED_LIMIT = 50

    cars = []


    def __init__(self, x, y, width, height):
        if y == 100 and height == 50:
            self.is_main = True
            img = os.path.join('images', 'main_car.png')
        else:
            self.is_main = False
            img = os.path.join('images', self.__cars_img[(width, height)])
        self.car = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.rect = self.car.get_rect()
        self.rect.x = x
        self.rect.y = y
        if width > height:
            self.horizontal = True
        else:
            self.horizontal = False

        self.cars.append(self)



    def round(self):
        x = self.rect.x
        y = self.rect.y
        # x
        u = (x // 50) * 50
        if x >= u + 25:
            new_x = u + 50
        else:
            new_x = u
        # y
        u = (y // 50) * 50
        if y >= u + 25:
            new_y = u + 50
        else:
            new_y = u
        return (new_x, new_y)



    def show(self, screen):
        screen.blit(self.car, self.rect)



    def __block_factor(self, x, y):
        for car in self.cars:
            if car == self:
                continue

            if car.rect.collidepoint((x, y)):
                return car.rect
        return False


    def __checkSpeed(self, speed):
        if speed > self.__SPEED_LIMIT:
            return True



    ########## movements ##########




    # main move function
    def move(self, new_x, new_y):
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height

        if self.horizontal:
            self.__mv_horizontal(new_x)
        else:
            self.__mv_vertical(new_y)




    # move horizontal
    def __mv_horizontal(self, new_x):
        if new_x > self.x:
            self.__mv_right(new_x)
        else:
            self.__mv_left(new_x)

    def __mv_right(self, new_x):
        block_factor = self.__block_factor(self.x + self.width, self.y)
        if block_factor:
            self.rect.x -= (self.x + self.width) - block_factor.x
        else:
            if self.__checkSpeed(new_x - self.x): return
            self.rect.x = new_x

    def __mv_left(self, new_x):
        block_factor = self.__block_factor(self.x - 1, self.y)
        if block_factor:
            self.rect.x = block_factor.x + block_factor.width
        else:
            if self.__checkSpeed(self.x - new_x): return
            self.rect.x = new_x



    # move vertical
    def __mv_vertical(self, new_y):
        if new_y > self.y:
            self.__mv_bottom(new_y)
        else:
            self.__mv_top(new_y)


    def __mv_bottom(self, new_y):
        block_factor = self.__block_factor(self.x, self.y + self.height)
        if block_factor:
            self.rect.y -= (self.y + self.height) - block_factor.y
        else:
            if self.__checkSpeed(new_y - self.y): return
            self.rect.y = new_y


    def __mv_top(self, new_y):
        block_factor = self.__block_factor(self.x, self.y - 1)
        if block_factor:
            self.rect.y = block_factor.y + block_factor.height
        else:
            if self.__checkSpeed(self.y - new_y): return
            self.rect.y = new_y
