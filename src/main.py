from src.ui import MainMenu
from src.utils import weave


if __name__ == "__main__":
    # from src.utils import delete_tables, create_tables
    # delete_tables()
    # create_tables()

    weave()
    print("Welcome!")
    MainMenu.run()
    print("\nBye!")
