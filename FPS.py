import pygame, math, random

# --- Settings ---
W, H = 800, 600
VW, VH = 200, 150 
TILE, MAP_SIZE = 100, 11
FOV, NUM_RAYS = math.pi / 3, 100
STEP, SCALE = FOV / NUM_RAYS, VW // NUM_RAYS

# --- Palette ---
C_WALL, C_DOOR, C_EXIT = (100, 70, 50), (80, 80, 80), (0, 100, 255)
C_ENEMY, C_SKY, C_FLOOR = (200, 0, 0), (25, 15, 15), (35, 35, 35)

def get_maze(size):
    maze = [[1] * size for _ in range(size)]
    def walk(x, y):
        maze[y][x] = 0
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]; random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx*2, y+dy*2
            if 0 < nx < size-1 and 0 < ny < size-1 and maze[ny][nx] == 1:
                maze[y+dy][x+dx] = 0; walk(nx, ny)
    walk(1, 1)
    # Add exit door at bottom right
    maze[size-2][size-2] = 3
    return maze

def get_spawn(m):
    while True:
        rx, ry = random.randint(1, 9), random.randint(1, 9)
        if m[ry][rx] == 0: return rx * TILE + 50, ry * TILE + 50

class Player:
    def __init__(self):
        self.hp, self.level = 10, 1
        self.z, self.vz = 0, 0 # Jump variables
        self.reset_pos()
    def reset_pos(self):
        self.x, self.y, self.a = TILE+50, TILE+50, 0
    def update_jump(self):
        self.z += self.vz
        if self.z > 0 or self.vz > 0: self.vz -= 1
        else: self.z, self.vz = 0, 0

class Enemy:
    def __init__(self, m):
        self.x, self.y = get_spawn(m)
        self.alive, self.last_s = True, 0

# --- Init ---
pygame.init()
pygame.mouse.set_visible(False) # Hide system cursor
sc = pygame.display.set_mode((W, H))
v_sc = pygame.Surface((VW, VH))
clock = pygame.time.Clock()
f_huge = pygame.font.SysFont('Impact', 80)

p = Player()
curr_map = get_maze(MAP_SIZE)
enemies = [Enemy(curr_map) for _ in range(3)]

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE and p.z == 0: p.vz = 12 # Jump
            if ev.key == pygame.K_e: # Interact
                tx, ty = p.x + math.cos(p.a)*TILE, p.y + math.sin(p.a)*TILE
                mx, my = int(tx/TILE), int(ty/TILE)
                if 0<=mx<11 and 0<=my<11 and curr_map[my][mx] == 3:
                    p.level += 1; curr_map = get_maze(MAP_SIZE); p.reset_pos()
                    enemies = [Enemy(curr_map) for _ in range(2 + p.level)]
        if ev.type == pygame.MOUSEBUTTONDOWN and p.hp > 0:
            for e in enemies:
                edx, edy = e.x - p.x, e.y - p.y
                ea = math.atan2(edy, edx) - p.a
                while ea > math.pi: ea -= 2*math.pi
                while ea < -math.pi: ea += 2*math.pi
                if abs(ea) < 0.15 and e.alive: e.alive = False

    # Movement (WASD + Strafe)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: p.a -= 0.07
    if keys[pygame.K_RIGHT]: p.a += 0.07
    spd, s_a, c_a = 5, math.sin(p.a), math.cos(p.a)
    dx, dy = 0, 0
    if keys[pygame.K_w]: dx += c_a * spd; dy += s_a * spd
    if keys[pygame.K_s]: dx -= c_a * spd; dy -= s_a * spd
    if keys[pygame.K_a]: dx += s_a * spd; dy -= c_a * spd # Strafe Left
    if keys[pygame.K_d]: dx -= s_a * spd; dy += c_a * spd # Strafe Right
    
    if curr_map[int(p.y/TILE)][int((p.x+dx)/TILE)] == 0: p.x += dx
    if curr_map[int((p.y+dy)/TILE)][int(p.x/TILE)] == 0: p.y += dy
    p.update_jump()

    # Rendering
    v_sc.fill(C_SKY)
    pygame.draw.rect(v_sc, C_FLOOR, (0, VH//2 + p.z, VW, VH//2 - p.z))
    dists = []
    for r in range(NUM_RAYS):
        ra = p.a - FOV/2 + r * STEP
        for d in range(1, 1000, 5):
            mx, my = int((p.x+d*math.cos(ra))/TILE), int((p.y+d*math.sin(ra))/TILE)
            if 0<=mx<11 and 0<=my<11 and curr_map[my][mx] > 0:
                d *= math.cos(p.a - ra); dists.append(d)
                h = (VW * TILE) / (d + 0.001)
                sh = 255 / (1 + d * d * 0.00002)
                col = C_WALL if curr_map[my][mx] == 1 else C_EXIT
                v_sc.fill([min(255, c*sh/255) for c in col], (r*SCALE, VH//2-h//2 + p.z, SCALE, h))
                break

    for e in enemies:
        if not e.alive: continue
        edx, edy = e.x - p.x, e.y - p.y
        dist = math.hypot(edx, edy)
        ea = math.atan2(edy, edx) - p.a
        while ea > math.pi: ea -= 2*math.pi
        while ea < -math.pi: ea += 2*math.pi
        if abs(ea) < FOV/2:
            sx = (ea + FOV/2) / FOV * VW
            idx = max(0, min(int(sx // SCALE), len(dists)-1))
            if dist < dists[idx]:
                pygame.draw.circle(v_sc, C_ENEMY, (int(sx), VH//2 + p.z), int(15000/dist))
                if dist < 120 and p.z < 20 and pygame.time.get_ticks() - e.last_s > 1000:
                    p.hp -= 1; e.last_s = pygame.time.get_ticks()

    sc.blit(pygame.transform.scale(v_sc, (W, H)), (0, 0))
    
    # Custom Crosshair
    pygame.draw.line(sc, (0, 255, 0), (W//2-10, H//2), (W//2+10, H//2), 2)
    pygame.draw.line(sc, (0, 255, 0), (W//2, H//2-10), (W//2, H//2+10), 2)

    # Status Bar
    pygame.draw.rect(sc, (30, 30, 30), (0, H-80, W, 80))
    face = (0, 255, 0) if p.hp > 6 else (255, 255, 0) if p.hp > 3 else (255, 0, 0)
    pygame.draw.rect(sc, face, (W//2-25, H-70, 50, 60))
    sc.blit(f_huge.render(f"{p.hp*10}%", True, (200,0,0)), (50, H-85))
    sc.blit(f_huge.render(f"LVL {p.level}", True, (200,200,200)), (W-250, H-85))

    if p.hp <= 0: exit()
    pygame.display.flip(); clock.tick(60)
