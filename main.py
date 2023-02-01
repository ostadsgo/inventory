import tomllib
from ui import Ui


def read_toml(filename="config.toml") -> dict[str, str]:
    """Read content of config.toml

    Parameters
    ----------
    filename: str
        filename for config.

    Return
    -------
    outs: dict[str, str]
        Dictionary of the config.toml file
    """
    with open(filename, "rb") as toml_file:
        config = tomllib.load(toml_file)
    return config


def get_credentioal() -> tuple[str]:
    """Read config file and return username and password.

    Returns
    -------
    outs: tuple[str]
        Return a tuple contain username and password
    """
    config = read_toml()
    username = config.get("username")
    password = config.get("password")
    return username, password


def user_validation(usr, passwd) -> bool:
    """Check the username and password responsed by the user
    with username and password stored in the config file.

    Return
    ------
    out: bool
        Return True if responsed username and password was correct
        otherwise return False.
    """
    username, password = get_credentioal()
    if usr == username and password == passwd:
        return True
    return False


def main():
    for _ in range(3):
        username = input("Username: ")
        password = input("Password: ")
        if not user_validation(username, password):
            print("Username or password is incorrect.")
            continue
        # if username and password was correct
        Ui.menu()


if __name__ == "__main__":
    main()
