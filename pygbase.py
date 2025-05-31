import pygame
import sys
import asyncio


class PyGameBase:
    def __init__(self, title="PyGameBase", width=800, height=600, fps=60, background_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.window_font = "msgothic"
        self.browser_font = "sans-serif"
        self.background_color = background_color
        self.prepressed = {}

    async def pyodide_init(self, js):
        pass

    def init(self):
        pass

    def update(self):
        pass

    def event(self, event):
        pass

    def check_key_press(self, pressed, key, delay=-1):
        if pressed[key]:
            if key not in self.prepressed or self.prepressed[key] == -1:
                self.prepressed[key] = 0
                return True
            else:
                self.prepressed[key] += 1
                if delay >= 0 and self.prepressed[key] > delay:
                    self.prepressed[key] = 0
                    return True
        else:
            if key in self.prepressed:
                self.prepressed[key] = -1

        return False

    def reset_key_press(self, key=None):
        if key is not None:
            if key in self.prepressed:
                self.prepressed[key] = -1
        else:
            for key in self.prepressed:
                self.prepressed[key] = -1

    def clear(self):
        self.screen.fill(self.background_color)
        if sys.platform == "emscripten":
            ctx = self.text_canvas_context
            ctx.clearRect(0, 0, self.width, self.height)

    def render_text(self, text, x, y, color=(0, 0, 0), font_size=24, bold=False, italic=False):
        if sys.platform == "emscripten":
            ctx = self.text_canvas_context
            boldtext = "bold " if bold else ""
            italictext = "italic " if italic else ""
            ctx.font = f"{boldtext}{italictext}{font_size}px {self.browser_font}"
            if isinstance(color, str):
                ctx.fillStyle = color
            elif isinstance(color, tuple) and len(color) == 3:
                ctx.fillStyle = f"rgb({color[0]}, {color[1]}, {color[2]})"
            ctx.fillText(text, x, y)
        else:
            font = pygame.font.SysFont(self.window_font, font_size, bold, italic)
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (x, y))

    def get_text_size(self, text, font_size=24, bold=False, italic=False):
        if sys.platform == "emscripten":
            ctx = self.text_canvas_context
            boldtext = "bold " if bold else ""
            italictext = "italic " if italic else ""
            ctx.font = f"{boldtext}{italictext}{font_size}px {self.browser_font}"
            metrics = ctx.measureText(text)
            return metrics.width, font_size
        else:
            font = pygame.font.SysFont(self.window_font, font_size, bold, italic)
            text_surface = font.render(text, True, (0, 0, 0))
            return text_surface.get_size()

    async def __start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        if sys.platform == 'emscripten':
            import js
            text_canvas = js.document.getElementById("text_canvas")
            text_canvas.width = self.width
            text_canvas.height = self.height
            self.text_canvas_context = text_canvas.getContext("2d")
            self.text_canvas_context.textBaseline = "top"
            loading = js.document.getElementById("loading")
            if loading is not None:
                loading.style.display = "none"
            await self.pyodide_init(js)

        self.init()

        self.frame = 0
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.event(event)

            self.clear()
            self.update()
            pygame.display.flip()

            self.clock.tick(self.fps)
            await asyncio.sleep(0)
            self.frame += 1

        pygame.quit()
        sys.exit()

    def run(self):
        if sys.platform == 'emscripten':
            asyncio.create_task(self.__start())
        else:
            asyncio.run(self.__start())
