class LatencyAgent:
    def analyze(self, latency_ms):
        return "HIGH_LATENCY" if latency_ms > 100 else "NORMAL"
