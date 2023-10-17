import pygame
import pytmx
import os

pygame.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

white = (255, 255, 255)
black = (0, 0, 0)

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Map Test")

tmxMap = pytmx.load_pygame("stuf.tmx")

running = True
clock = pygame.time.Clock()

# Entities OWO
class Entity:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

Player = Entity(725, 175, 25, 25, 5)

class cammy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

Camera = cammy(0, 0, 5)

collisionObjects = []
for obj in tmxMap.objects:
    if obj.name == "Collision":
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        collisionObjects.append(rect)

while(running):
    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            running = False

    # Code for game here uwu

    # Movement lol
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_w]):
        Player.y -= Player.speed
    if(keys[pygame.K_a]):
        Player.x -= Player.speed
    if(keys[pygame.K_s]):
        Player.y += Player.speed
    if(keys[pygame.K_d]):
        Player.x += Player.speed

    # Camera lol
    Camera.x = Player.x - (window.get_width() // 2)
    Camera.y = Player.y - (window.get_height() // 2)

    Camera.x = max(0, min(Camera.x, tmxMap.width * tmxMap.tilewidth - window.get_width()))
    Camera.y = max(0, min(Camera.y, tmxMap.height * tmxMap.tileheight - window.get_height()))

    window.fill(black)

    # Check for collision uwu
    playerRect = pygame.Rect(Player.x, Player.y, Player.width, Player.height)
    for obj in collisionObjects:
        if Player.x < obj.x + obj.width and Player.x + Player.width > obj.x and Player.y < obj.y + obj.height and Player.y + Player.height > obj.y:
            Player.x = max(Player.x, obj.x + obj.width)
            Player.x = min(Player.x, obj.x - Player.width)
            Player.y = max(Player.y, obj.y + obj.height)
            Player.y = min(Player.y, obj.y - Player.height)

    # Draw stuff lol
    # Draw map (ground layer)
    for layer in tmxMap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if(layer.name == "Ground"):
                for x, y, gid in layer:
                    tile = tmxMap.get_tile_image_by_gid(gid)
                    if tile:
                        window.blit(tile, (x * tmxMap.tilewidth - Camera.x, y * tmxMap.tileheight - Camera.y))
    
    # Draw map (objects layer)
    for layer in tmxMap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if(layer.name == "Objects"):
                for x, y, gid in layer:
                    tile = tmxMap.get_tile_image_by_gid(gid)
                    if tile:
                        window.blit(tile, (x * tmxMap.tilewidth - Camera.x, y * tmxMap.tileheight - Camera.y))

    # draw player
    pygame.draw.rect(window, white, (Player.x - Camera.x, Player.y - Camera.y, Player.width, Player.height))

    # Draw map (upper objects layer)
    for layer in tmxMap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if(layer.name == "UpperObjects"):
                for x, y, gid in layer:
                    tile = tmxMap.get_tile_image_by_gid(gid)
                    if tile:
                        window.blit(tile, (x * tmxMap.tilewidth - Camera.x, y * tmxMap.tileheight - Camera.y))


    pygame.display.flip()
    clock.tick(60)
pygame.quit()
