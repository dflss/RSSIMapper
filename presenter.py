class Presenter:
    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view

    def run(self):
        self.view.show()

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def set_program_data(self, program_data):
        self.model.set_program_data(program_data)

    def measure_point_by_coordinates(self, x, y):
        self.model.measure_point_by_coordinates(x, y)
        self.view.notify_map_updated()

    def measure_point_by_id(self, id):
        self.model.measure_point_by_id(id)
        self.view.notify_map_updated()

    def update_map(self):
        fig = self.model.get_map_with_rssi_values()
        self.view.render_map(fig)
