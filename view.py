class View():
    def __init__(self, presenter):
        self._presenter = presenter

    def show(self):
        pass

    def render_map(self, figure):
        pass

    def notify_map_updated(self):
        pass
