import pygame

# 초기화
pygame.init()

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 색깔
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 카메라 크기
CAMERA_WIDTH = 400
CAMERA_HEIGHT = 300

# FPS
FPS = 60

# 게임 화면
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("파이게임 카메라와 벽 예제")

# 플레이어
player_pos = [0, 0]
player_radius = 20
player_speed = 5

# 벽
walls = [
    pygame.Rect(300, 150, 200, 20),
    pygame.Rect(100, 400, 20, 200),
    pygame.Rect(500, 400, 20, 200),
    pygame.Rect(200, 100, 20, 150),
    pygame.Rect(400, 350, 200, 20)
]

# 카메라
camera = pygame.Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)

# FPS 설정
clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    screen.fill(WHITE)
    
    # 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_player_pos = [player_pos[0] - player_speed, player_pos[1]]
        if all(not wall.colliderect(pygame.Rect(new_player_pos[0] - player_radius, new_player_pos[1] - player_radius, player_radius * 2, player_radius * 2)) for wall in walls):
            player_pos = new_player_pos
    if keys[pygame.K_RIGHT]:
        new_player_pos = [player_pos[0] + player_speed, player_pos[1]]
        if all(not wall.colliderect(pygame.Rect(new_player_pos[0] - player_radius, new_player_pos[1] - player_radius, player_radius * 2, player_radius * 2)) for wall in walls):
            player_pos = new_player_pos
    if keys[pygame.K_UP]:
        new_player_pos = [player_pos[0], player_pos[1] - player_speed]
        if all(not wall.colliderect(pygame.Rect(new_player_pos[0] - player_radius, new_player_pos[1] - player_radius, player_radius * 2, player_radius * 2)) for wall in walls):
            player_pos = new_player_pos
    if keys[pygame.K_DOWN]:
        new_player_pos = [player_pos[0], player_pos[1] + player_speed]
        if all(not wall.colliderect(pygame.Rect(new_player_pos[0] - player_radius, new_player_pos[1] - player_radius, player_radius * 2, player_radius * 2)) for wall in walls):
            player_pos = new_player_pos
    
    # 카메라 업데이트
    camera.center = player_pos
    
    # 카메라 영역에 벽만 그리기
    for wall in walls:
        if camera.colliderect(wall):
            pygame.draw.rect(screen, RED, wall.move(-camera.x, -camera.y))
    
    # 플레이어 그리기
    pygame.draw.circle(screen, RED, player_pos, player_radius)
    
    # 게임 종료 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 화면 업데이트
    pygame.display.flip()
    
    # FPS 설정
    clock.tick(FPS)

# 종료
pygame.quit()
