from pico2d import *
import game_world
import game_framework
import random

# Bird Run Speed
PIXEL_PER_METER = (10.0/0.3)   # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0   # km/h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

class Run:

    @staticmethod
    def enter(bird, e):
        bird.dir, bird.action, bird.face_dir = 2, 2, 1

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

        if bird.x < 50 :    # 충돌 체크
            bird.face_dir = 1
        elif bird.x > (1500 - 50):
            bird.face_die = -1

        bird.action = (bird.action + 1) % 3

    @staticmethod
    def draw(bird):
            if bird.face_dir == 1:
                bird.image.clip_composite_draw(int(bird.frame) % 5 * 182, bird.action * 165, 180, 165, 0, '', bird.x, bird.y, 100, 100)
            elif bird.face_dir == -1:
                bird.image.clip_composite_draw(int(bird.frame) % 5 * 182, bird.action * 165, 180, 165, 0, 'h', bird.x, bird.y, 100, 100)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
        self.transitions = {Run : {}}
    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def draw(self):
        self.cur_state.draw(self.bird)



class Bird:
    def __init__(self):
        self.x, self.y = random.randint(50, 1500), random.randint(200, 550)
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'(Time : {get_time():.2f})',(255, 255, 0))


