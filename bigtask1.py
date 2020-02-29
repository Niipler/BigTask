import math
import sys
import pygame
import requests
LAN_STEP = 0.008
LON_STEP = 0.008
coord_to_get_x = 0.0000428
coord_to_get_y = 0.0000428
map_file = "map.png"


class Mapa:
    def __init__(self, lan=37.530887, lon=55.703118, zoom=15):
        self.lon = lon
        self.lan = lan
        self.zoom = zoom
        self.map_type = "map"
        self.i = 1

    def change_zoom(self, key):
        if key:
            if self.zoom < 19:
                self.zoom += 1
        else:
            if self.zoom > 2:
                self.zoom -= 1

    def move_map(self, key):
        if key == 'down':
            self.lon -= LON_STEP * math.pow(2, 15 - self.zoom)
        elif key == 'up':
            self.lon += LON_STEP * math.pow(2, 15 - self.zoom)
        elif key == 'right' and self.lan < 85:
            self.lan += LAN_STEP * math.pow(2, 15 - self.zoom)
        elif key == 'left' and self.lan > -85:
            self.lan -= LAN_STEP * math.pow(2, 15 - self.zoom)
        if self.lon > 180: self.lon -= 360
        if self.lon < -180: self.lon += 360

    def change_type(self):
        if self.i == 1:
            self.map_type = 'sat'
            self.i += 1
        elif self.i == 2:
            self.map_type = 'skl'
            self.i += 1
        elif self.i == 3:
            self.map_type = 'map'
            self.i = 1


def load_map(mapa):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={lan},{lon}&l={type}&z={zoom}".format\
        (lan=mapa.lan, lon=mapa.lon, type=mapa.map_type, zoom=mapa.zoom)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.flip()
    mapa = Mapa()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= 500 and x <= 600 and y >= 400 and y <= 450:
                    mapa.change_type()
            key = pygame.key.get_pressed()
            if key[pygame.K_PAGEUP]:
                mapa.change_zoom(True)
            if key[pygame.K_PAGEDOWN]:
                mapa.change_zoom(False)
            if key[pygame.K_UP]:
                mapa.move_map('up')
            if key[pygame.K_DOWN]:
                mapa.move_map('down')
            if key[pygame.K_LEFT]:
                mapa.move_map('left')
            if key[pygame.K_RIGHT]:
                mapa.move_map('right')
        load_map(mapa)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), (500, 400, 100, 50))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
