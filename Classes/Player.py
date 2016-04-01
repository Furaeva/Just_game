from pygame import *
from Utilities.load_image import load_image
from Utilities.animation import Animation

LEFT = 1
RIGHT = 2
MOVE_SPEED = 3  # убрать


def load_souces():
    global LEFT_SPRITES, RIGHT_SPRITES, UP_SPRITES, DOWN_SPRITES, LEFT_STOP_SPRITES, RIGHT_STOP_SPRITES
    LEFT_SPRITES = load_image(['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png'], alpha_channel=True)
    RIGHT_SPRITES = load_image(['1.1.png', '2.1.png', '3.1.png', '4.1.png',
                                '5.1.png', '6.1.png', '7.1.png', '8.1.png'], alpha_channel=True)
    UP_SPRITES = load_image('1.png', alpha_channel=True)
    # UP_SPRITES = load_image(['1.png'], alpha_channel=True)
    DOWN_SPRITES = load_image('1.1.png', alpha_channel=True)
    LEFT_STOP_SPRITES = load_image('1.png', alpha_channel=True)
    RIGHT_STOP_SPRITES = load_image('1.1.png', alpha_channel=True)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        load_souces()
        self.image = None
        self.xvel = MOVE_SPEED
        self.yvel = MOVE_SPEED
        self.rect = Rect(x, y, 30, 10)
        self.state = 'stop'
        # Направление для определения анимации покоя
        self.direction = LEFT
        # TODO: Бинарная матрица
        self.anim_left = Animation(LEFT_SPRITES)
        self.anim_right = Animation(RIGHT_SPRITES)
        self.anim_up = Animation(UP_SPRITES)
        self.anim_down = Animation(DOWN_SPRITES)
        self.anim_stop_left = Animation(LEFT_STOP_SPRITES)
        self.anim_stop_right = Animation(RIGHT_STOP_SPRITES)
        self.left = self.right = self.up = self.down = False

    def event(self, e):
        if e.type == KEYDOWN and e.key == K_LEFT:
            self.left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            self.right = True
        if e.type == KEYDOWN and e.key == K_UP:
            self.up = True
        if e.type == KEYDOWN and e.key == K_DOWN:
            self.down = True

        if e.type == KEYUP and e.key == K_RIGHT:
            self.right = False
        if e.type == KEYUP and e.key == K_LEFT:
            self.left = False
        if e.type == KEYUP and e.key == K_UP:
            self.up = False
        if e.type == KEYUP and e.key == K_DOWN:
            self.down = False

    def update(self, dt, objects):
        """
        Обновление состояния объекта. dt - сколько миллисекунд прошло с прошлого вызова данного метода
        """

        if self.left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.state = 'move'
            self.direction = LEFT

        if self.right:
            self.xvel = MOVE_SPEED   # Право = x + n
            self.state = 'move'
            self.direction = RIGHT

        if self.up:
            self.yvel = -MOVE_SPEED
            self.state = 'move'

        if self.down:
            self.yvel = MOVE_SPEED
            self.state = 'move'

        if not(self.left or self.right or self.up or self.down):       # стоим, когда нет указаний идти
            self.xvel = 0
            self.yvel = 0
            self.state = 'stop'

        self.rect.y += self.yvel
        self.collision(0, self.yvel, objects)

        self.rect.x += self.xvel
        self.collision(self.xvel, 0, objects)

        # # Анимация
        for anim in [self.anim_right, self.anim_left, self.anim_up,
                     self.anim_down, self.anim_stop_left, self.anim_stop_right]:
            anim.update(dt)

        if self.left:
            self.image = self.anim_left.get_sprite()
        if self.right:
            self.image = self.anim_right.get_sprite()
        if self.up:
            self.image = self.anim_up.get_sprite()
        if self.down:
            self.image = self.anim_down.get_sprite()

        if self.state == 'stop' and self.direction == LEFT:
            self.image = self.anim_stop_left.get_sprite()
        if self.state == 'stop' and self.direction == RIGHT:
            self.image = self.anim_stop_right.get_sprite()

    def render(self, screen):
        x = self.rect.x - self.image.get_rect().width / 7
        y = self.rect.y - self.image.get_rect().height + self.rect.height
        screen.blit(self.image, (x, y))

    def collision(self, xvel, yvel, objects):
        for o in objects:
            if self.rect.colliderect(o["object"]):       # если есть пересечение платформы с игроком

                if xvel > 0:                       # если движется вправо
                    self.rect.right = o["object"].rect.left  # то не движется вправо

                if xvel < 0:                       # если движется влево
                    self.rect.left = o["object"].rect.right  # то не движется влево

                if yvel > 0:
                    self.rect.bottom = o["object"].rect.top
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = o["object"].rect.bottom
                    self.yvel = 0

    def area_collision(self, objects):
        for o in objects:
            if self.rect.colliderect(o["object"].area):
                return True, o
            else:
                return False, None