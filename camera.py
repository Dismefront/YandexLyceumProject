class Camera:
    def __init__(self, sz, border):
        self.dx = 0
        self.sz = sz
        self.border = border
        self.relative_pos = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        if target[0] >= self.sz[0] * 2 // 3 and \
                self.relative_pos + self.sz[0] < self.border[1]:
            self.dx = -10
        elif target[0] <= self.sz[0] // 3 and \
                self.relative_pos > self.border[0]:
            self.dx = 10
        else:
            self.dx = 0
        self.relative_pos -= self.dx