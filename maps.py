import pygame, sys

# --- Khởi tạo ---
pygame.init()
TILE_SIZE = 50
ROWS, COLS = 5, 20
WIDTH, HEIGHT = (COLS-5) * TILE_SIZE, ROWS * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Map 5x20 Example")


# Camera class để quản lý scrolling
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target = None
        
    def follow(self, target):
        """Camera theo dõi một đối tượng"""
        self.target = target
        
    def update(self):
        """Cập nhật vị trí camera để theo dõi target"""
        if self.target:
            # Đặt camera sao cho target ở giữa màn hình
            self.x = self.target.x - WIDTH // 2
            self.y = self.target.y - HEIGHT // 2
            
            # Giới hạn camera trong phạm vi map
            self.x = max(0, min(self.x, COLS * TILE_SIZE - WIDTH))
            self.y = max(0, min(self.y, ROWS * TILE_SIZE - HEIGHT))
    
    def apply(self, rect):
        """Chuyển đổi tọa độ world sang tọa độ screen"""
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)

# Tạo camera
camera = Camera()

tile_images = {
    1: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/dirt.png").convert_alpha(),
    2: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/grass2.png").convert_alpha(),
    3: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/water.gif").convert_alpha(),
    4: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/dirt_grass.png").convert_alpha(),
    5: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/leaves.png").convert_alpha(),
    7: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/trunk_bottom.png").convert_alpha(),
    6: pygame.image.load("./kenney_voxel-pack/PNG/Tiles/trunk_mid.png").convert_alpha(),
}
# Resize về 32x32
for key in tile_images:
    tile_images[key] = pygame.transform.scale(tile_images[key], (TILE_SIZE, TILE_SIZE))

water_frames = [
    pygame.image.load("./kenney_voxel-pack/PNG/Tiles/water/water1.png").convert_alpha(),
    pygame.image.load("./kenney_voxel-pack/PNG/Tiles/water/water2.png").convert_alpha(),
    # pygame.image.load("./kenney_voxel-pack/PNG/Tiles/water/water3.png").convert_alpha(),
    # pygame.image.load("./kenney_voxel-pack/PNG/Tiles/water/water4.png").convert_alpha(),
]

# resize tất cả frames
for i in range(len(water_frames)):
    water_frames[i] = pygame.transform.scale(water_frames[i], (TILE_SIZE, TILE_SIZE))


background = pygame.image.load("./kenney_voxel-pack/PNG/Tiles/blue-sky-background-in-pixel-art-style-vector.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

# --- Tạo tile map ---
tile_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,5,5,5,5],
    [0,0,2,4,4,4,0,0,0,0,0,0,4,0,0,5,5,5,5,0],
    [0,0,4,1,1,1,4,4,0,0,0,4,1,0,0,0,0,7,2,0],    
    [4,4,1,1,1,1,1,1,1,1,1,1,1,3,3,3,4,4,4,4],
]


# --- Load sprite nhân vật (demo: hình vuông đỏ) ---
player = pygame.Rect(50, 50, TILE_SIZE, TILE_SIZE)
player_speed = 10
frame_index = 0
frame_timer = 0
frame_speed = 10
camera.follow(player)
# --- Vòng lặp game ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))
    camera.update()

    frame_timer += 1
    if frame_timer >= frame_speed:
        frame_timer = 0
        frame_index = (frame_index + 1) % len(water_frames)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # --- Vẽ nền ---
    for row in range(len(tile_map)):
        for col in range(len(tile_map[row])):
            value = tile_map[row][col]
            if value != 0:
                world_x = col * TILE_SIZE
                world_y = row * TILE_SIZE
                
                # Áp dụng camera offset
                screen_x = world_x - camera.x
                screen_y = world_y - camera.y

                if value == 3:  # water
                    screen.blit(water_frames[frame_index], (screen_x, screen_y))
                elif value in tile_images:
                    screen.blit(tile_images[value], (screen_x, screen_y))


    # --- Vẽ nhân vật ---
    pygame.draw.rect(screen, (255, 0, 0), player)

    pygame.display.flip()
    clock.tick(30)
