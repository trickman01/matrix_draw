import pygame as pg
pg.init()

class Pixel:
    def __init__(self, pos: tuple, surf_true: pg.Surface, surf_false: pg.Surface):
        self.pos = pos
        self.true_surf = surf_true
        self.false_surf = surf_false
        self.state = False
        self.rect = self.false_surf.get_rect()
        self.rect.center = self.pos
        self.disp_surf = self.false_surf

    def toggle_pixel(self, mouse_x, mouse_y):
        if self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom:
            self.state = (not self.state)
        if self.state:
            self.disp_surf = self.true_surf
        else:
            self.disp_surf = self.false_surf

def get_values(pixels: list):                   #outputs string in format "const uint32_t frame[] = {0x8ffc7fe3, 0xff1ff8ff, 0xc7fe3ff1};" to use in Arduino Sketch.  Change variable name if needed
    values = []
    for pixel in pixels:
        if pixel.state:
            values.append('1')
        else:
            values.append('0')
    
    one = values[:32]
    two = values[32:64]
    three = values[64:]

    one_hex = hex(int(''.join(one), 2))
    two_hex = hex(int(''.join(two), 2))
    three_hex = hex(int(''.join(three), 2))
    output = f'const uint32_t frame[] = {{{one_hex}, {two_hex}, {three_hex}}};'
    print(output)

if __name__ == '__main__':

    matrix = [0] * 96
    mWidth = 12
    mHeight = 8
    radius = 15

    screen_width = 800
    screen_height = 600

    true_surf = pg.Surface((radius * 2, radius * 2))
    true_surf.fill('black')
    false_surf = true_surf.copy()
    pg.draw.circle(true_surf, 'red', (radius, radius), radius)
    pg.draw.circle(false_surf, 'red', (radius, radius), radius, 2)

    xs = [int(screen_width / (mWidth + 1)) * x for x in range(mWidth + 1) if x > 0]
    ys = [int(screen_height / (mHeight + 1)) * y for y in range(mHeight + 1) if y > 0]
    pos_list = []
    for y in ys:
        for x in xs:
            pos_list.append((x, y))

    pixels = []

    for p in pos_list:
        pixels.append(Pixel(p, true_surf, false_surf))

    screen = pg.display.set_mode((screen_width, screen_height))
    screen.fill('black')
    for p in pixels:
        screen.blit(p.disp_surf, p.rect)
    pg.display.flip()

    running = True
    clicked = False
    update = False

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if running:
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == pg.KEYDOWN:
                    update = True
                    if event.key == pg.K_SPACE:
                        get_values(pixels)
                    if event.key == pg.K_r:
                        for p in pixels:
                            p.state = False
                            p.disp_surf = p.false_surf
                    if event.key == pg.K_s:
                        pg.image.save(screen, 'screen_capture.png')

        if running:
            if clicked:
                clicked = False
                mouse_x, mouse_y = pg.mouse.get_pos()
                screen.fill('black')
                for pixel in pixels:
                    pixel.toggle_pixel(mouse_x, mouse_y)
                    screen.blit(pixel.disp_surf, pixel.rect)
                pg.display.flip()
            
            if update:
                screen.fill('black')
                for pixel in pixels:
                    screen.blit(pixel.disp_surf, pixel.rect)
                pg.display.flip()

    pg.quit()