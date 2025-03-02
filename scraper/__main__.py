import os
import importlib
import scraperconfig

def get_modules():
    directory = os.path.dirname(os.path.realpath(__file__))
    modules = []
    for f in os.listdir(directory):
        if f.endswith(".py") and f != "__init__.py" and f != "__main__.py":
            module_name = f[:-3]  # Remove ".py" extension
            try:
                module = importlib.import_module(module_name)
                title = getattr(module, "title", module_name)
                modules.append({"name": module_name, "module": module, "title": title})
            except ImportError as e:
                print(f"Warning: Could not import module '{module_name}': {e}. Skipping.")
            except Exception as e:
                print(f"Warning: Error while processing module '{module_name}': {e}. Skipping.")
    return modules

def display_module_menu(modules):
    print("\nAvailable Options:")
    for i, module in enumerate(modules):
        print(f"{i + 1}. {module['title']}")
    print("0. Exit")

def get_module_choice(modules):
    while True:
        try:
            choice = int(input("Enter the number of the option to run: "))
            if 0 <= choice <= len(modules):
                return choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_module(module):
    function_name = "main"
    try:
        function = getattr(module, function_name)
        if not callable(function):
            print(f"Error: Module does not have a callable function '{function_name}'.")
            return

        result = function()
        if result is not None:
            print("Module output:", result)

    except AttributeError:
        print(
            f"Error: Module does not have a '{function_name}' function."
        ) 
    except Exception as e:
        print(f"An error occurred while running the module: {e}")


def main():
    scraperconfig.setup()

    modules = get_modules()

    if not modules:
        print("No Python modules found")
        return

    display_module_menu(modules)
    module_choice = get_module_choice(modules)

    if module_choice == 0:
        exit("Exiting...")

    selected_module = modules[module_choice - 1]
    module_name = selected_module["name"]
    try:
        run_module(selected_module["module"])
    except ImportError:
        print(f"Error: Could not import module '{module_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
