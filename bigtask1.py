import os
import sys

import pygame
import requests
LAN_STEP = 0.008
LON_STEP = 0.02
coord_to_get_x = 0.0000428
coord_to_get_y = 0.0000428
map_file = "map.png"


class Mapa:
    def __init__(self, lan=37.530887, lon=55.703118, zoom=15):
        self.lan = lan
        self.lon = lon
        self.zoom = zoom
        self.type = "map"



def load_map(mapa):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={lan},{lon}&l={type}&z={zoom}".format\
        (lan=mapa.lan, lon=mapa.lon, type=mapa.type, zoom=mapa.zoom)
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

    cords = sys.argv[1:]
    mapa = Mapa(cords[0], cords[1], cords[2])

    while pygame.event.wait().type != pygame.QUIT:
        load_map(mapa)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()



if __name__ == "__main__":
    main()



