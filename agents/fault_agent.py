class FaultAgent:
    def analyze(self, link_alive):
        return "LINK_FAILURE" if not link_alive else "HEALTHY"
