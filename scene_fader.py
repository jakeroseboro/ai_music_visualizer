from PIL import Image

class SceneFader:
    def __init__(self, ctx, scene_paths):
        self.ctx = ctx
        self.textures = [self.load_texture(p) for p in scene_paths]
        self.current = 0
        self.next = 1
        self.transition = 0.0

    def load_texture(self, path):
        img = Image.open(path).convert('RGB')
        tex = self.ctx.texture(img.size, 3, img.tobytes())
        tex.build_mipmaps()
        return tex

    def update(self, dt):
        self.transition += dt * 0.05
        if self.transition >= 1.0:
            self.transition = 0.0
            self.current = self.next
            self.next = (self.next + 1) % len(self.textures)

    def bind(self, prog):
        self.textures[self.current].use(location=0)
        if len(self.textures) > 1:
            self.textures[self.next].use(location=1)
        prog['mix_factor'].value = self.transition
