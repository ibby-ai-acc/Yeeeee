class TrailingStop:
    def __init__(self, trail_pct=1.5):
        self.pct = trail_pct
        self.entry = self.high = None
    def set_entry(self, price):
        self.entry = self.high = price
    def update(self, price):
        if self.high is None: return False
        self.high = max(self.high, price)
        return price <= self.high * (1 - self.pct/100)
