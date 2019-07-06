import sys

from cad.main import MainWindow, Application


def main() -> int:
    app = Application(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    status_code = main()
    sys.exit(status_code)
