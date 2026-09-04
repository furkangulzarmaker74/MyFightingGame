import os
import math

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.image import Image as CoreImage
from kivy.uix.button import Button
from kivy.uix.label import Label


class FightingGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.p1_x = 100
        self.p2_x = 620
        self.p1_y = 180
        self.p2_y = 180

        self.p1_health = 100
        self.p2_health = 100

        self.p1_velocity_y = 0
        self.gravity = 1
        self.jump_power = -18

        self.p1_attack = None
        self.p1_attack_timer = 0
        self.p1_attack_cooldown = 0

        self.p2_attack = None
        self.p2_attack_timer = 0
        self.p2_attack_cooldown = 0

        self.hit_timer = 0
        self.hit_x = 0
        self.hit_y = 0

        self.game_over = False
        self.winner = ""

        base = os.path.dirname(os.path.abspath(__file__))
        self.player1_path = os.path.join(base, "player1.png")
        self.player2_path = os.path.join(base, "player2.png")

        self.p1_texture = CoreImage(self.player1_path).texture
        self.p2_texture = CoreImage(self.player2_path).texture

        self.touch_buttons = []
        self.make_controls()

        Clock.schedule_interval(self.update, 1 / 60)

    def make_controls(self):
        # Transparent-ish mobile controls. They are real Kivy buttons,
        # so they work with Android touch input.
        specs = [
            ("<", 0.02, 0.03, 0.10, 0.13, self.move_left),
            (">", 0.13, 0.03, 0.10, 0.13, self.move_right),
            ("JUMP", 0.66, 0.03, 0.12, 0.13, self.jump),
            ("PUNCH", 0.77, 0.20, 0.11, 0.13, lambda *_: self.player1_attack("punch")),
            ("KICK", 0.88, 0.03, 0.10, 0.13, lambda *_: self.player1_attack("kick")),
        ]

        for text, x, y, w, h, callback in specs:
            b = Button(text=text, size_hint=(w, h), pos_hint={"x": x, "y": y})
            b.bind(on_press=callback)
            self.add_widget(b)
            self.touch_buttons.append(b)

        self.restart_button = Button(
            text="RESTART",
            size_hint=(0.27, 0.12),
            pos_hint={"x": 0.365, "y": 0.20},
            opacity=0,
            disabled=True,
        )
        self.restart_button.bind(on_press=self.reset_game)
        self.add_widget(self.restart_button)

        self.result_label = Label(
            text="",
            font_size="55sp",
            bold=True,
            size_hint=(1, 0.2),
            pos_hint={"x": 0, "y": 0.55},
            opacity=0,
        )
        self.add_widget(self.result_label)

    def move_left(self, *_):
        if not self.game_over:
            self.p1_x -= 25

    def move_right(self, *_):
        if not self.game_over:
            self.p1_x += 25

    def jump(self, *_):
        if not self.game_over and self.p1_y >= 180:
            self.p1_velocity_y = self.jump_power

    def player1_attack(self, kind):
        if self.game_over or self.p1_attack_cooldown > 0:
            return

        self.p1_attack = kind

        if kind == "punch":
            self.p1_attack_timer = 18
            self.p1_attack_cooldown = 30
            damage = 10
            attack_x = self.p1_x + 100
            attack_y = self.p1_y + 65
            attack_w = 110
            attack_h = 90
        else:
            self.p1_attack_timer = 24
            self.p1_attack_cooldown = 40
            damage = 15
            attack_x = self.p1_x + 80
            attack_y = self.p1_y + 145
            attack_w = 140
            attack_h = 100

        if (attack_x < self.p2_x + 155 and
                attack_x + attack_w > self.p2_x + 25 and
                attack_y < self.p2_y + 265 and
                attack_y + attack_h > self.p2_y + 25):
            self.p2_health -= damage
            self.hit_timer = 12
            self.hit_x = self.p2_x + 80
            self.hit_y = self.p2_y + 120

    def reset_game(self, *_):
        self.p1_x = 100
        self.p1_y = 180
        self.p2_x = 620
        self.p2_y = 180
        self.p1_health = 100
        self.p2_health = 100
        self.p1_velocity_y = 0
        self.p1_attack = None
        self.p1_attack_timer = 0
        self.p1_attack_cooldown = 0
        self.p2_attack = None
        self.p2_attack_timer = 0
        self.p2_attack_cooldown = 0
        self.hit_timer = 0
        self.game_over = False
        self.winner = ""
        self.result_label.opacity = 0
        self.restart_button.opacity = 0
        self.restart_button.disabled = True
        self.touch_buttons_visibility(True)

    def touch_buttons_visibility(self, visible):
        for b in self.touch_buttons:
            b.disabled = not visible
            b.opacity = 1 if visible else 0

    def update(self, dt):
        if not self.game_over:
            self.p1_x = max(0, min(self.p1_x, 900 - 180))

            self.p1_velocity_y += self.gravity
            self.p1_y += self.p1_velocity_y

            if self.p1_y >= 180:
                self.p1_y = 180
                self.p1_velocity_y = 0

            if self.p1_attack_cooldown > 0:
                self.p1_attack_cooldown -= 1

            if self.p1_attack_timer > 0:
                self.p1_attack_timer -= 1
            else:
                self.p1_attack = None

            distance = self.p1_x - self.p2_x

            if self.p2_attack is None:
                if distance > 130:
                    self.p2_x += 2
                elif distance < -130:
                    self.p2_x -= 2

            self.p2_x = max(0, min(self.p2_x, 900 - 180))

            if self.p2_attack_cooldown > 0:
                self.p2_attack_cooldown -= 1

            if abs(self.p1_x - self.p2_x) < 145 and self.p2_attack is None and self.p2_attack_cooldown == 0:
                if int(Clock.get_time() * 1000) % 2 == 0:
                    self.p2_attack = "punch"
                    self.p2_attack_timer = 18
                    self.p2_attack_cooldown = 50
                else:
                    self.p2_attack = "kick"
                    self.p2_attack_timer = 24
                    self.p2_attack_cooldown = 60

            if self.p2_attack is not None:
                self.p2_attack_timer -= 1

                if self.p2_attack_timer == 9 and abs(self.p1_x - self.p2_x) < 160:
                    self.p1_health -= 10 if self.p2_attack == "punch" else 15
                    self.hit_timer = 12
                    self.hit_x = self.p1_x + 70
                    self.hit_y = self.p1_y + 120

                if self.p2_attack_timer <= 0:
                    self.p2_attack = None

            if self.hit_timer > 0:
                self.hit_timer -= 1

            if self.p2_health <= 0:
                self.p2_health = 0
                self.game_over = True
                self.winner = "YOU WIN!"
            elif self.p1_health <= 0:
                self.p1_health = 0
                self.game_over = True
                self.winner = "YOU LOSE!"

            if self.game_over:
                self.result_label.text = self.winner
                self.result_label.opacity = 1
                self.restart_button.opacity = 1
                self.restart_button.disabled = False
                self.touch_buttons_visibility(False)

        self.draw_game()

    def draw_game(self):
        self.canvas.before.clear()

        with self.canvas.before:
            # Sky
            Color(80 / 255, 160 / 255, 220 / 255, 1)
            Rectangle(pos=(0, 0), size=self.size)

            # Ground
            Color(65 / 255, 155 / 255, 75 / 255, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.height * 0.25))

            # Ground line
            Color(20 / 255, 20 / 255, 20 / 255, 1)
            Line(points=[0, self.height * 0.25, self.width, self.height * 0.25], width=3)

            # Health bars
            bar_w = self.width * 0.39
            bar_h = self.height * 0.05
            y = self.height * 0.90

            Color(90 / 255, 0, 0, 1)
            Rectangle(pos=(self.width * 0.03, y), size=(bar_w, bar_h))
            Rectangle(pos=(self.width * 0.58, y), size=(bar_w, bar_h))

            Color(220 / 255, 40 / 255, 40 / 255, 1)
            Rectangle(pos=(self.width * 0.03, y), size=(bar_w * self.p1_health / 100, bar_h))
            Rectangle(pos=(self.width * 0.58, y), size=(bar_w * self.p2_health / 100, bar_h))

            # Characters
            pw = self.width * 0.20
            ph = self.height * 0.45

            p1_draw_x = self.p1_x / 900 * self.width
            p2_draw_x = self.p2_x / 900 * self.width
            p1_draw_y = self.height * 0.25
            p2_draw_y = self.height * 0.25

            if self.p1_attack == "punch":
                progress = self.p1_attack_timer / 18
                p1_draw_x += (20 * math.sin(progress * math.pi)) / 900 * self.width
            elif self.p1_attack == "kick":
                progress = self.p1_attack_timer / 24
                p1_draw_x += (28 * math.sin(progress * math.pi)) / 900 * self.width

            if self.p2_attack == "punch":
                progress = self.p2_attack_timer / 18
                p2_draw_x -= (25 * math.sin(progress * math.pi)) / 900 * self.width
            elif self.p2_attack == "kick":
                progress = self.p2_attack_timer / 24
                p2_draw_x -= (32 * math.sin(progress * math.pi)) / 900 * self.width

            Rectangle(texture=self.p1_texture, pos=(p1_draw_x, p1_draw_y),
                      size=(pw, ph))
            Rectangle(texture=self.p2_texture, pos=(p2_draw_x, p2_draw_y),
                      size=(pw, ph))

            # Attack effects
            if self.p1_attack == "punch" and self.p1_attack_timer / 18 < 0.75:
                fx = p1_draw_x + pw * 1.03
                fy = p1_draw_y + ph * 0.39
                Color(1, 220 / 255, 40 / 255, 1)
                Ellipse(pos=(fx, fy), size=(22, 22))
            elif self.p1_attack == "kick" and self.p1_attack_timer / 24 < 0.75:
                fx = p1_draw_x + pw * 1.06
                fy = p1_draw_y + ph * 0.72
                Color(1, 220 / 255, 40 / 255, 1)
                Ellipse(pos=(fx, fy), size=(26, 26))

            if self.p2_attack == "punch" and self.p2_attack_timer / 18 < 0.75:
                fx = p2_draw_x - 8
                fy = p2_draw_y + ph * 0.39
                Color(1, 220 / 255, 40 / 255, 1)
                Ellipse(pos=(fx, fy), size=(22, 22))
            elif self.p2_attack == "kick" and self.p2_attack_timer / 24 < 0.75:
                fx = p2_draw_x - 8
                fy = p2_draw_y + ph * 0.72
                Color(1, 220 / 255, 40 / 255, 1)
                Ellipse(pos=(fx, fy), size=(26, 26))

            # Hit effect
            if self.hit_timer > 0:
                size = 30 + (12 - self.hit_timer) * 3
                hx = self.hit_x / 900 * self.width
                hy = self.height * 0.25 + (self.hit_y - 180) / 420 * self.height * 0.45
                Color(1, 220 / 255, 40 / 255, 1)
                Line(circle=(hx, hy, size), width=3)
                Line(points=[hx-size, hy-size, hx+size, hy+size], width=3)
                Line(points=[hx+size, hy-size, hx-size, hy+size], width=3)


class FightingApp(App):
    def build(self):
        self.title = "My Fighting Game"
        return FightingGame()


if __name__ == "__main__":
    FightingApp().run()
