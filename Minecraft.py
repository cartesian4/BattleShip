import pygame as pg, math as m, random as r
try: from noise import pnoise2
except: pnoise2 = lambda x, y, **k: 0

pg.init(); w, h = 800, 600; screen = pg.display.set_mode((w, h))
clock = pg.time.Clock(); pg.mouse.set_visible(False); pg.event.set_grab(True)
f_u = pg.font.SysFont('Arial', 20); f_d = pg.font.SysFont('Arial', 40)

# Settings
CHUNK_SIZE, RENDER_DIST, SEED = 4, 2, r.randint(0, 999)
SKY, P_EYE = (135, 206, 235), 1.8 # Player eye height

def reset():
    global p_p, p_r, dy, hp, gm, menu, chunks, target
    p_p, p_r, dy, hp, gm, menu, target = [0.0, 5.0, 0.0], [0.0, 0.0], 0.0, 10.0, False, False, None
    chunks = {}
reset()

def project(p_list):
    # Relativize and Rotate
    x, y, z = p_list[0]-p_p[0], p_list[1]-p_p[1], p_list[2]-p_p[2]
    nx = x*m.cos(p_r[1]) - z*m.sin(p_r[1])
    nz = x*m.sin(p_r[1]) + z*m.cos(p_r[1])
    ny = y*m.cos(p_r[0]) - nz*m.sin(p_r[0])
    nz = y*m.sin(p_r[0]) + nz*m.cos(p_r[0])
    # FRUSTUM CULLING: Block is behind camera
    if nz <= 0.1: return None, nz
    f = 400 / (nz + 1e-6)
    return [int(w/2 + nx*f), int(h/2 - ny*f)], nz

run = True
while run:
    screen.fill(SKY)
    for e in pg.event.get():
        if e.type == pg.QUIT: run = False
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE: menu = not menu; pg.mouse.set_visible(menu)

    if not gm and not menu:
        rel_x, rel_y = pg.mouse.get_rel()
        p_r[1] += rel_x * 0.003
        p_r[0] = max(-1.5, min(1.5, p_r[0] - rel_y * 0.003))
        
        # Terrain Generation
        cx, cz = int(p_p[0]//CHUNK_SIZE), int(p_p[2]//CHUNK_SIZE)
        visible_blocks = []
        for x in range(cx-RENDER_DIST, cx+RENDER_DIST+1):
            for z in range(cz-RENDER_DIST, cz+RENDER_DIST+1):
                if (x, z) not in chunks:
                    c_blks = []
                    for bx in range(x*CHUNK_SIZE, (x+1)*CHUNK_SIZE):
                        for bz in range(z*CHUNK_SIZE, (z+1)*CHUNK_SIZE):
                            nh = int((pnoise2(bx*0.1, bz*0.1, base=SEED)+1)*3)
                            for by in range(nh + 1):
                                # OCCLUSION: Only add blocks if they have an exposed face
                                c_blks.append([float(bx), float(by), float(bz), (34,139,34) if by==nh else (101,67,33)])
                    chunks[(x, z)] = c_blks
                visible_blocks.extend(chunks[(x, z)])

        # AABB Physics & Movement
        keys, sp = pg.key.get_pressed(), 0.12
        s, c = m.sin(p_r[1]), m.cos(p_r[1])
        next_p = p_p[:]
        if keys[pg.K_w]: next_p[0]+=s*sp; next_p[2]+=c*sp
        if keys[pg.K_s]: next_p[0]-=s*sp; next_p[2]-=c*sp
        
        dy -= 0.01; next_p[1] += dy
        
        # Collision Detection: Stop player from falling into void or walking through blocks
        ground = -1.0 # Buffer floor
        for b in visible_blocks:
            if b[0]-0.3 < next_p[0] < b[0]+1.3 and b[2]-0.3 < next_p[2] < b[2]+1.3:
                if b[1] < next_p[1]-P_EYE: ground = max(ground, b[1]+P_EYE)
                elif b[1] < next_p[1]+0.2: next_p[0], next_p[2] = p_p[0], p_p[2] # Wall hit
        
        if next_p[1] <= ground: next_p[1], dy = ground, 0
        if keys[pg.K_SPACE] and next_p[1] == ground: dy = 0.18
        p_p = next_p

        # Render Logic
        visible_blocks.sort(key=lambda b: (b[0]-p_p[0])**2 + (b[1]-p_p[1])**2 + (b[2]-p_p[2])**2, reverse=True)
        target = None
        for b in visible_blocks:
            v = [[b[0]+i, b[1]+j, b[2]+k] for i in (0,1) for j in (0,1) for k in (0,1)]
            # FACE WINDING: Front, Back, Left, Right, Top, Bottom
            faces = [(0,1,3,2), (4,6,7,5), (0,4,6,2), (1,5,7,3), (2,3,7,6), (0,1,5,4)]
            for f in faces:
                pts, d_sum = [], 0
                for idx in f:
                    prj, nz = project(v[idx])
                    if prj: pts.append(prj); d_sum += nz
                if len(pts) == 4:
                    # BACK-FACE CULLING: (v1_x * v2_y - v1_y * v2_x)
                    if (pts[1][0]-pts[0][0])*(pts[2][1]-pts[0][1]) - (pts[1][1]-pts[0][1])*(pts[2][0]-pts[0][0]) < 0:
                        pg.draw.polygon(screen, b[3], pts)
                        pg.draw.polygon(screen, (0,0,0), pts, 1)
                        if abs(pts[0][0]-w//2)<20 and abs(pts[0][1]-h//2)<20: target = b

    # UI
    xh_clr = (255, 255, 0) if target else (255, 255, 255)
    pg.draw.line(screen, xh_clr, (w//2-10, h//2), (w//2+10, h//2), 2)
    pg.draw.line(screen, xh_clr, (w//2, h//2-10), (w//2, h//2+10), 2)
    pg.display.flip(); clock.tick(60)
pg.quit()
