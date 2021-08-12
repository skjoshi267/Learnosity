from os import name
from load_data import assign_data, load_data, transform_data, build_ui_data, run_app

if __name__ == "__main__":
    data = load_data()

    data_obj = assign_data(data)

    transform_data(data_obj)

    build_ui_data(data_obj)

    run_app(data_obj)
