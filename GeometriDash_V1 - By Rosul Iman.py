''' 
    harus melakukan instalasi windows "pip install arcade" 
    jika gagal download melalaui https://github.com/pythonarcade/arcade
    kemudian extrak zip, pada direktori yang telah di ekstrak, buka terminal dan install arcade "pip install e ."
'''

import arcade
import random

# Nilai konstanta yang diperlukan
SCREEN_WIDTH = 512 * 2
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Geometri dash KW By Rosul Iman"

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
PLAYER_START_X = 400
PLAYER_START_Y = 128 + 1
SCORE = 0

# Definisi variabel di tingkat global
x_min_obstacle = 1000
x_max_obstacle = 24000 # berdasarkan poin
height_lantai = 149

DISABLE_SPAM = True

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SCORE)
        self.player = Entity("asset/player_003.png", PLAYER_START_X, PLAYER_START_Y, 0.35)
        self.Entity_Obstacle = arcade.SpriteList()
        self.background = None

        self.music_list = arcade.load_sound("1-02. Stereo Madness.mp3")

        self.scane = arcade.SpriteList()

        self.physics_engine = None

        self.runDraw = True
        self.spam = DISABLE_SPAM

        self.Lantai = arcade.SpriteList()

        self.score = SCORE
        self.Pesan_terkenaDuri = arcade.Text("KAMU TERKENA DURI", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.RED, 30, anchor_x="center")
        self.Pesan_mulaiUlang = arcade.Text("TEKAN ENTER UNTUK MEMULAI", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50, arcade.color.WHITE, 30, anchor_x="center")
        self.Score = arcade.Text("Score: " + str(self.score), SCREEN_WIDTH/5, SCREEN_HEIGHT/1.2, arcade.color.WHITE, 30, anchor_x="center")
        self.Terkena_Obstacle = False        

        arcade.set_background_color(arcade.csscolor.BLUE)

    def setup(self):

        print("++===================================================++")
        print("||  SELAMAT DATANG DI GAME GEOMETRI DASH KW versi 1  ||")
        print("||  Created by Rosul Iman                            ||")
        print("||  Email  : rosuliman874@gmail.com                  ||")
        print("++===================================================++")
        print("                ||                ||                   ")
        print("                ||                ||                   ")
        print("                || Enjoy The Game ||                   ")
        print("                ||                ||                   ")
        print("                ||                ||                   ")
        print("                ++================++                   ")


        j = 0
        jumlah_background = x_max_obstacle/ 1024
        jumlah_background = int(jumlah_background)
        for _ in range(jumlah_background):
            self.background = Entity("asset/game_bg_01_001-hd.png", j, SCREEN_HEIGHT / 2, 1)
            self.scane.append(self.background)
            j += 1023

        size = 0
        jumlah_lantai = (x_max_obstacle/3) / 128
        jumlah_lantai = int(jumlah_lantai)
        for _ in range(jumlah_lantai):
            new_Lantai = Entity("asset/groundSquare_01_001-hd.png", size, 128/2, 0.5)
            self.Lantai.append(new_Lantai)
            size += 128

        jumlah_obstacle = (x_max_obstacle/3) / 2.3

        jumlah_obstacle = int(jumlah_obstacle)

        for _ in range(jumlah_obstacle):
            new_obstacle_dart = Entity("asset/obstacle_dart.png", 0, 0, 0.35)

            koordinat_obstacle_list = []

            koordinat_obstacle = random.randint(x_min_obstacle, x_max_obstacle)

            if (koordinat_obstacle not in koordinat_obstacle_list) and koordinat_obstacle % 40 == 0:
                jarak_dart = koordinat_obstacle                 
                koordinat_obstacle_list.append(koordinat_obstacle)
                new_obstacle_dart.setXY(jarak_dart, height_lantai - 4)
                self.Entity_Obstacle.append(new_obstacle_dart)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, [self.Entity_Obstacle, self.Lantai])

        self.bgm = arcade.play_sound(self.music_list, 0.05)

        self.coor_x_1 = 0
        self.coor_x_2 = 0
        self.poin = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W and self.spam:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
            self.player.angle = -15
            self.spam = False
        if key == arcade.key.ENTER and self.runDraw == False:
            self.Terkena_Obstacle = False
            self.runDraw = True
            self.bgm = arcade.play_sound(self.music_list, 0.05)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.angle = (self.player.angle + self.player.change_angle) % 360

    def on_draw(self):
        self.clear()
        self.scane.draw()
        self.Entity_Obstacle.draw()
        self.Lantai.draw()
        self.player.draw()
        self.Score.draw()

        if self.Terkena_Obstacle:
            self.Pesan_terkenaDuri.draw()
            self.Pesan_mulaiUlang.draw()

    def on_update(self, delta_time=1/60):

        if self.player.center_y <= 150 and self.player.center_y >= 148:
            self.spam = True
        
        if arcade.check_for_collision_with_list(self.player, self.Entity_Obstacle):
            self.runDraw = False
            self.Terkena_Obstacle = True
            self.reset_game()

        else:
            self.physics_engine.update()
            self.player.update()
            
        if self.runDraw:
            self.coor_x_1 += -0.5
            self.coor_x_2 += -5
            if abs(self.coor_x_2) % 5 == 0:
                self.poin = self.poin + 3                
                if self.poin % 16 == 0:
                    self.score += 1
                self.Score = arcade.Text("Score: " + str(self.score), SCREEN_WIDTH/5, SCREEN_HEIGHT/1.2, arcade.color.WHITE, 25, anchor_x="center")
            self.scane.move(-0.5, 0)
            self.Entity_Obstacle.move(-5, 0)
            self.Lantai.move(-5, 0)

    def reset_game(self):
        self.player.center_x = PLAYER_START_X

        self.reset_screen()
        arcade.stop_sound(self.bgm)

        self.coor_x_1 = 0
        self.coor_x_2 = 0
        self.poin = 0

        self.score = 0
        self.Score = arcade.Text("Score: " + str(self.score), SCREEN_WIDTH/5, SCREEN_HEIGHT/1.2, arcade.color.WHITE, 25, anchor_x="center")

    def reset_screen(self):
        self.Lantai.move(abs(self.coor_x_2), 0)
        self.Entity_Obstacle.move(abs(self.coor_x_2), 0)


class Entity(arcade.Sprite):
    def __init__(self, SourcesImage, x=0, y=0, SCALE=1):
        super().__init__(SourcesImage, SCALE)
        self.center_x = x
        self.center_y = y
        self.angle = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.angle not in [0, 90, 180, 270]:
            self.angle += -15

    def move_x(self, SPEED):
        self.center_x += SPEED

    def setXY(self, x, y):
        self.center_x += x
        self.center_y += y

    def getY(self):
        return self.center_y

    def getX(self):
        return self.center_x

    def getWith(self):
        return self.width

    def setName(self):
        self.name


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
