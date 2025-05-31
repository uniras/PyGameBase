import pygame
from pygbase import PyGameBase


class InputTest(PyGameBase):
    def init(self):
        self.circle_x = 100      # 円の中心X座標
        self.circle_y = 100      # 円の中心Y座標
        self.circle_move = 10    # 円の移動量
        self.circle_delay = 10   # キーリピートの受付間隔(0は無制限、-1以下は無効)

    def update(self):
        # マウスの現在位置を取得
        x, y = pygame.mouse.get_pos()

        # テキストの描画
        self.render_text(f"X位置: {x}  Y位置: {y}", 0, 0, (255, 255, 255), 36)

        # カーソルキーの入力処理(キーリピート対応)
        pressed = pygame.key.get_pressed()
        if self.check_key_press(pressed, pygame.K_UP, self.circle_delay):
            self.circle_y -= self.circle_move
        if self.check_key_press(pressed, pygame.K_DOWN, self.circle_delay):
            self.circle_y += self.circle_move
        if self.check_key_press(pressed, pygame.K_LEFT, self.circle_delay):
            self.circle_x -= self.circle_move
        if self.check_key_press(pressed, pygame.K_RIGHT, self.circle_delay):
            self.circle_x += self.circle_move

        pygame.draw.circle(self.screen, (255, 0, 0), (self.circle_x, self.circle_y), 50)


InputTest(title="Input Test", width=800, height=600, background_color=(0, 0, 0)).run()
