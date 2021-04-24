import argparse
import sys
import matplotlib.pyplot as plt

from src.presenter.presenter import Presenter
from src.model.program_data import ProgramData
from src.view.view import View


class ViewCLI(View):
    def __init__(self, presenter: Presenter):
        super().__init__(presenter)
        self.menu_actions = {
            "main_menu": self.main_menu,
            "1": self._presenter.update_map,
            "2": self.measure_point,
            "9": self.back,
            "0": sys.exit,
        }
        program_data = self._parse_cmd_args()
        self._presenter.set_program_data(program_data)

    def show(self):
        self.main_menu()

    def render_map(self, figure: plt.Figure):
        plt.show()

    def main_menu(self):
        print("Please choose the action:")
        print("[1] Show map")
        print("[2] Start measurements")
        print("[0] Quit")
        choice = input(">>  ")
        self.exec_menu(choice)

    def back(self):
        self.menu_actions["main_menu"]()

    def exec_menu(self, choice: str):
        ch = choice.lower()
        if ch == "":
            self.menu_actions["main_menu"]()
        else:
            try:
                self.menu_actions[ch]()
            except KeyError:
                print("Invalid selection, please try again.")
        self.menu_actions["main_menu"]()

    def _parse_cmd_args(self) -> ProgramData:
        parser = argparse.ArgumentParser()
        optional = parser._action_groups.pop()
        optional.add_argument(
            "-ic", "--input_csv", help="input csv to create shapefile"
        )
        required = parser.add_argument_group("required arguments")
        required.add_argument(
            "-is", "--input_shapefile", help="input shapefile", required=True
        )
        required.add_argument(
            "-or",
            "--output_results",
            help="text file for saving results",
            required=True,
        )
        required.add_argument(
            "-os",
            "--output_shapefile",
            help="file for saving output shapefile",
            required=True,
        )
        required.add_argument(
            "-op", "--output_plot", help="file for saving colored map", required=True
        )
        required.add_argument(
            "-p", "--port", help="port where board is connected", required=True
        )
        required.add_argument(
            "-b", "--baudrate", help="baudrate for serial connection", required=True
        )
        required.add_argument(
            "-st",
            "--serial_timeout",
            help="timeout for serial connection",
            required=True,
        )
        required.add_argument(
            "-mt",
            "--measurement_timeout",
            help="timeout for measurement point",
            required=True,
        )
        required.add_argument(
            "-n",
            "--n_measurements",
            help="number of measurements taken for 1 point",
            required=True,
        )
        parser._action_groups.append(optional)
        args = parser.parse_args()
        return ProgramData(
            args.input_csv,
            args.input_shapefile,
            args.output_results,
            args.output_shapefile,
            args.output_plot,
            args.port,
            int(args.baudrate),
            int(args.serial_timeout),
            int(args.measurement_timeout),
            int(args.n_measurements),
        )

    def measure_point(self):
        print("Type measurement point id and click enter, b to go back to menu.")
        choice = input(">>  ")
        if choice == "b":
            self.menu_actions["main_menu"]()
        else:
            try:
                id = int(choice)
                print("Measurement started, please wait...")
                self._presenter.measure_point_by_id(id)
                print("Done. Press c to continue, b to go back to menu.")
                choice = input(">>  ")
                if choice == "c":
                    self.measure_point()
                elif choice == "b":
                    self.menu_actions["main_menu"]()
            except ValueError as e:
                print(e)
