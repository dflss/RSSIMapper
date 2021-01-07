from model import Model
from program_data import ProgramData
from view import View


class Presenter:
    def run(self):
        self.view.show()

    def set_model(self, model: Model):
        self.model = model

    def set_view(self, view: View):
        self.view = view

    def set_program_data(self, program_data: ProgramData):
        if self.model is None:
            raise ValueError("Model not initialized in Presenter")
        self.model.set_program_data(program_data)

    def measure_point_by_coordinates(self, x: int, y: int):
        if self.model is None:
            raise ValueError("Model not initialized in Presenter")
        if self.view is None:
            raise ValueError("View not initialized in Presenter")
        self.model.measure_point_by_coordinates(x, y)
        self.view.notify_map_updated()

    def measure_point_by_id(self, id: int):
        if self.model is None:
            raise ValueError("Model not initialized in Presenter")
        if self.view is None:
            raise ValueError("View not initialized in Presenter")
        self.model.measure_point_by_id(id)
        self.view.notify_map_updated()

    def update_map(self):
        if self.model is None:
            raise ValueError("Model not initialized in Presenter")
        if self.view is None:
            raise ValueError("View not initialized in Presenter")
        fig = self.model.get_map_with_rssi_values()
        self.view.render_map(fig)
