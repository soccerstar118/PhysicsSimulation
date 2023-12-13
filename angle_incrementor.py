class AngleIncr:
    def __init__(self, start, end, incr_amount):
        self.angle = start

        self.min = min(start, end)
        self.max = max(start, end)

        self.incr = abs(incr_amount)

    def update(self):
        self.angle += self.incr
        if self.angle > self.max:
            self.incr = -abs(self.incr)
        if self.angle < self.min:
            self.incr = abs(self.incr)

