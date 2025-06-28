from trailing_stop import TrailingStop
class PositionManager:
    def __init__(self, trail_pct=1.5):
        self.tstop = TrailingStop(trail_pct)
        self.active = False
    def open(self, price): self.tstop.set_entry(price); self.active = True
    def check(self, price): return self.tstop.update(price)
    def reset(self): self.active = False
