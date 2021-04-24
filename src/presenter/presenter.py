from src.constants import RSSI_CHOICE, PERCENT_CHOICE
from src.log import logger
from src.model.model import Model
from src.model.program_data import ProgramData
from src.view.view import View


class Presenter:
    def run(self):
        self.check_if_view_initialized()
        self.view.show()

    def set_model(self, model: Model):
        self.model = model

    def set_view(self, view: View):
        self.view = view

    def check_if_model_initialized(self):
        if self.model is None:
            raise ValueError("Model not initialized in Presenter")

    def check_if_view_initialized(self):
        if self.view is None:
            raise ValueError("View not initialized in Presenter")

    def set_program_data(self, program_data: ProgramData):
        self.check_if_model_initialized()
        self.model.set_program_data(program_data)
        self.model.config_mgr.update(program_data)
        try:
            self.update_map()
        except Exception as e:
            logger.error(f"Exception occurred: {e}")

    def fetch_saved_settings(self):
        program_data = self.model.config_mgr.read()
        self.model.set_program_data(program_data)
        return program_data

    def measure_point_by_coordinates(self, x: int, y: int):
        self.check_if_model_initialized()
        self.check_if_view_initialized()
        self.model.measure_point_by_coordinates(x, y)
        self.view.notify_map_updated()

    def measure_point_by_id(self, id: int):
        self.check_if_model_initialized()
        self.check_if_view_initialized()
        self.model.measure_point_by_id(id)
        self.view.notify_map_updated()

    def update_map(self, choice=RSSI_CHOICE):
        self.check_if_model_initialized()
        self.check_if_view_initialized()
        if choice == RSSI_CHOICE:
            fig = self.model.get_map_with_rssi_values()
        elif choice == PERCENT_CHOICE:
            fig = self.model.get_map_with_percent_values()
        else:
            raise ValueError("Incorrect choice value")
        self.model.save_plot()
        self.view.render_map(fig)

    def get_received_status(self):
        return self.model.get_received_status()
