import sys

from src.presenter.presenter import Presenter
from src.model.model import Model
from src.view.view_cli import ViewCLI
from src.view.view_gui import ViewGUI


def main():
    presenter = Presenter()
    model = Model()
    presenter.set_model(model)
    if not len(sys.argv) > 1:
        view = ViewGUI(presenter)
    else:
        view = ViewCLI(presenter)
    presenter.set_view(view)
    presenter.run()


if __name__ == '__main__':
    main()
