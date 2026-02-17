class BandwidthAgent:
    def analyze(self, usage):
        return "CONGESTED" if usage > 80 else "NORMAL"
