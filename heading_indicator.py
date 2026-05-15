import pygame
import math
import csv
import os
import time

pygame.init()

WIDTH = 1000
HEIGHT = 950

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Directional Gyro / HSI Simulator")
clock = pygame.time.Clock()

# --- STATE VARIABLES ---
night_mode = False
failure_mode = False
autoplay_mode = False

# Simulation parameters
true_heading = 0.0      # The actual magnetic heading of the aircraft
indicated_heading = 0.0 # What the gyro shows (true + drift)
drift_error = 0.0       # Gyro drift in degrees
drift_rate = 0.5        # Degrees of drift per second for simulation (exaggerated for demo)

target_heading = 0.0    # HDG BUG setting
airplane_turning_to = 0.0 # Autopilot target heading

# Fonts
font_title = pygame.font.SysFont("Arial", 36, bold=True)
font_subtitle = pygame.font.SysFont("Arial", 18)
font_labels = pygame.font.SysFont("Arial", 22, bold=True)
font_alarm = pygame.font.SysFont("Arial", 40, bold=True)
font_mono = pygame.font.SysFont("Courier New", 28, bold=True)
font_ui = pygame.font.SysFont("Arial", 20, bold=True)

# UI Elements
slider_x, slider_y, slider_w, slider_h = 150, HEIGHT - 80, WIDTH - 300, 10
dragging_slider = False
btn_sync = pygame.Rect(WIDTH//2 - 250, HEIGHT - 150, 140, 40)
btn_fail = pygame.Rect(WIDTH//2 - 70, HEIGHT - 150, 140, 40)
btn_auto = pygame.Rect(WIDTH//2 + 110, HEIGHT - 150, 140, 40)

# Logging
log_file = "heading_log.csv"
last_log_time = time.time()
start_time = time.time()

# Autoplay Scenario
scenario_sequence = [
    (0, 0), (5, 90), (15, 90), (20, 180), (35, 180), (40, 300), (55, 300), (60, 0)
]

def log_data(t, true_hdg, ind_hdg, tgt_hdg, drift):
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "True Heading", "Indicated Heading", "Target HDG Bug", "Gyro Drift Error"])
        writer.writerow([f"{t:.1f}", f"{true_hdg:.1f}", f"{ind_hdg:.1f}", f"{tgt_hdg:.1f}", f"{drift:.1f}"])

def shortest_angle_diff(a, b):
    diff = (b - a) % 360
    if diff > 180: diff -= 360
    return diff

def get_colors():
    if failure_mode:
        return {'bg': (10, 10, 10), 'dial': (5, 5, 5), 'border': (20, 20, 20), 'primary': (50, 50, 50), 'secondary': (50, 50, 50), 'plane': (50, 50, 50), 'alarm': (255, 0, 0), 'text':(50,50,50), 'ui':(30,30,30)}
    if night_mode:
        return {'bg': (5, 8, 5), 'dial': (0, 2, 0), 'border': (10, 30, 10), 'primary': (0, 255, 0), 'secondary': (50, 255, 100), 'plane': (0, 255, 0), 'alarm': (255, 50, 50), 'text':(0,200,0), 'ui':(10,40,10)}
    return {'bg': (36, 28, 24), 'dial': (18, 14, 12), 'border': (58, 50, 42), 'primary': (255, 230, 100), 'secondary': (255, 140, 0), 'plane': (255, 60, 20), 'alarm': (255, 0, 0), 'text':(200, 180, 160), 'ui':(60, 50, 40)}

running = True
while running:
    dt = clock.tick(60) / 1000.0
    now = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n: night_mode = not night_mode
            elif event.key == pygame.K_f: failure_mode = not failure_mode
            elif event.key == pygame.K_s: autoplay_mode = not autoplay_mode; start_time = now
            elif event.key == pygame.K_d: drift_error = 0.0 # SYNC
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if btn_sync.collidepoint(mx, my): drift_error = 0.0
            elif btn_fail.collidepoint(mx, my): failure_mode = not failure_mode
            elif btn_auto.collidepoint(mx, my): autoplay_mode = not autoplay_mode; start_time = now
            else:
                # Check slider
                thumb_x = slider_x + (target_heading / 360.0) * slider_w
                if math.hypot(mx - thumb_x, my - slider_y) < 25: dragging_slider = True
                elif slider_x <= mx <= slider_x + slider_w and slider_y - 20 <= my <= slider_y + 20:
                    target_heading = ((mx - slider_x) / slider_w) * 360.0
                    dragging_slider = True
                # Check dial click for HDG bug
                center_x, center_y = WIDTH//2, 430
                if math.hypot(mx - center_x, my - center_y) < 260:
                    ang = math.degrees(math.atan2(my - center_y, mx - center_x)) + 90
                    target_heading = (ang + indicated_heading) % 360
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_slider:
                mx = max(slider_x, min(event.pos[0], slider_x + slider_w))
                target_heading = ((mx - slider_x) / slider_w) * 360.0

    # Controls
    keys = pygame.key.get_pressed()
    if not autoplay_mode and not failure_mode:
        if keys[pygame.K_LEFT]: airplane_turning_to -= 60 * dt
        if keys[pygame.K_RIGHT]: airplane_turning_to += 60 * dt
        airplane_turning_to %= 360
        
    elif autoplay_mode and not failure_mode:
        elapsed = now - start_time
        for i in range(len(scenario_sequence)-1):
            t1, h1 = scenario_sequence[i]
            t2, h2 = scenario_sequence[i+1]
            if t1 <= elapsed < t2:
                prog = (elapsed - t1) / (t2 - t1)
                airplane_turning_to = h1 + shortest_angle_diff(h1, h2) * prog
                airplane_turning_to %= 360
                break
        if elapsed >= scenario_sequence[-1][0]: autoplay_mode = False

    # Dynamics
    if not failure_mode:
        # Aircraft turns towards airplane_turning_to
        diff = shortest_angle_diff(true_heading, airplane_turning_to)
        true_heading = (true_heading + diff * 1.5 * dt) % 360
        
        # Gyro Drift
        drift_error += drift_rate * dt
        if drift_error > 180: drift_error -= 360
        
        indicated_heading = (true_heading + drift_error) % 360

    # Logging
    if now - last_log_time >= 1.0:
        log_data(now - start_time, true_heading, indicated_heading, target_heading, drift_error)
        last_log_time = now

    # Drawing
    c = get_colors()
    screen.fill(c['bg'])

    # Title
    title = font_title.render("Advanced Directional Gyro / HSI Simulator", True, c['primary'])
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    sub = font_subtitle.render("Simulates Earth drift, manual sync, HDG select, and autopilot scenario.", True, c['text'])
    screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 60))

    # Dial
    center_x, center_y, radius = WIDTH//2, 430, 260
    pygame.draw.circle(screen, c['border'], (center_x, center_y), radius + 20)
    pygame.draw.circle(screen, c['dial'], (center_x, center_y), radius)

    for angle in range(0, 360, 5):
        rot = angle - indicated_heading
        rad = math.radians(rot - 90)
        is_l = angle % 30 == 0
        is_m = angle % 10 == 0
        t_len = 30 if is_l else (18 if is_m else 10)
        t_wid = 5 if is_l else (3 if is_m else 2)
        
        xo = center_x + math.cos(rad) * radius
        yo = center_y + math.sin(rad) * radius
        xi = center_x + math.cos(rad) * (radius - t_len)
        yi = center_y + math.sin(rad) * (radius - t_len)
        pygame.draw.line(screen, c['primary'], (xi, yi), (xo, yo), t_wid)
        
        if is_l:
            tx = center_x + math.cos(rad) * (radius - 65)
            ty = center_y + math.sin(rad) * (radius - 65)
            txt = {0:"N", 90:"E", 180:"S", 270:"W"}.get(angle, str(angle))
            col = c['secondary'] if angle in [0,90,180,270] else c['primary']
            lbl = font_labels.render(txt, True, col)
            screen.blit(lbl, lbl.get_rect(center=(tx, ty)))

    # Target Bug
    if not failure_mode:
        bug_rad = math.radians(target_heading - indicated_heading - 90)
        bx = center_x + math.cos(bug_rad) * radius
        by = center_y + math.sin(bug_rad) * radius
        
        # Draw a cyan bug shape
        bug_pts = [
            (bx, by), 
            (bx - 15 * math.cos(bug_rad + math.pi/2), by - 15 * math.sin(bug_rad + math.pi/2)), 
            (bx + 15 * math.cos(bug_rad + math.pi/2), by + 15 * math.sin(bug_rad + math.pi/2)),
            (bx - 20 * math.cos(bug_rad), by - 20 * math.sin(bug_rad))
        ]
        pygame.draw.polygon(screen, (0, 255, 255), bug_pts)

    # Top indicator
    pygame.draw.line(screen, c['secondary'], (center_x, center_y - radius), (center_x, center_y - radius + 40), 6)

    # Plane Icon
    plane_pts = [(0, -95), (4, -90), (8, -75), (10, -45), (12, -20), (85, 30), (85, 45), (16, 35), (14, 75), (40, 95), (40, 105), (10, 95), (5, 110), (0, 100)]
    poly = [(center_x+x, center_y+y-15) for x,y in plane_pts] + [(center_x-x, center_y+y-15) for x,y in reversed(plane_pts[:-1]) if x!=0]
    pygame.draw.polygon(screen, c['dial'], poly)
    pygame.draw.polygon(screen, c['plane'], poly, 3)

    # Heading Box
    box = pygame.Rect(center_x-50, center_y-radius-30, 100, 50)
    pygame.draw.rect(screen, c['dial'], box, border_radius=8)
    pygame.draw.rect(screen, c['text'], box, 2, border_radius=8)
    hlbl = font_mono.render(f"{int(indicated_heading):03d}", True, c['primary'])
    screen.blit(hlbl, hlbl.get_rect(center=box.center))
    
    # Drift Info Panel
    panel = pygame.Rect(center_x + radius + 30, center_y - 60, 240, 120)
    pygame.draw.rect(screen, c['dial'], panel, border_radius=8)
    pygame.draw.rect(screen, c['text'], panel, 2, border_radius=8)
    
    drift_lbl = font_ui.render(f"DRIFT: {drift_error:+.1f}°", True, c['alarm'] if abs(drift_error)>5 else c['primary'])
    screen.blit(drift_lbl, (panel.x + 15, panel.y + 20))
    true_lbl = font_ui.render(f"MAG HDG: {int(true_heading):03d}°", True, c['text'])
    screen.blit(true_lbl, (panel.x + 15, panel.y + 50))
    ind_lbl = font_ui.render(f"IND HDG: {int(indicated_heading):03d}°", True, c['primary'])
    screen.blit(ind_lbl, (panel.x + 15, panel.y + 80))

    # UI Buttons
    def draw_btn(r, text, active=False):
        pygame.draw.rect(screen, c['primary'] if active else c['ui'], r, border_radius=8)
        pygame.draw.rect(screen, c['text'], r, 2, border_radius=8)
        lbl = font_ui.render(text, True, c['bg'] if active else c['primary'])
        screen.blit(lbl, lbl.get_rect(center=r.center))
        
    draw_btn(btn_sync, "SYNC GYRO (D)")
    draw_btn(btn_fail, "FAILURE (F)", failure_mode)
    draw_btn(btn_auto, "AUTOPILOT (S)", autoplay_mode)

    # Slider
    pygame.draw.rect(screen, c['text'], (slider_x, slider_y - slider_h//2, slider_w, slider_h), border_radius=4)
    thx = slider_x + (target_heading / 360.0) * slider_w
    pygame.draw.circle(screen, (0, 255, 255), (int(thx), slider_y), 16)
    slbl = font_ui.render("HDG BUG SELECT", True, c['text'])
    screen.blit(slbl, (WIDTH//2 - slbl.get_width()//2, slider_y - 35))

    # Alarms
    if not failure_mode:
        dev = abs(shortest_angle_diff(indicated_heading, target_heading))
        if dev > 15 and int(now * 4) % 2 == 0:
            albl = font_alarm.render(f"HEADING DEV ({int(dev)}°)", True, c['alarm'])
            screen.blit(albl, (WIDTH//2 - albl.get_width()//2, center_y + radius + 40))

    if failure_mode:
        pygame.draw.line(screen, c['alarm'], (center_x-radius, center_y-radius), (center_x+radius, center_y+radius), 15)
        pygame.draw.line(screen, c['alarm'], (center_x+radius, center_y-radius), (center_x-radius, center_y+radius), 15)
        flbl = font_alarm.render("HDG FAIL", True, c['alarm'], (0,0,0))
        screen.blit(flbl, (center_x - flbl.get_width()//2, center_y - 30))

    pygame.display.flip()

pygame.quit()