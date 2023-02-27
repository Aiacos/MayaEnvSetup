import os
import pathlib


def get_system_env_var(var_name):
    """
    Get ENVIRONMENT VAR
    :param var_name: string
    :return: string
    """
    # refresh_terminal_env_var()
    return os.environ.get(var_name)


def remove_system_env_var_permanently(var_name):
    """
    Remove ENVIRONMENT VAR
    :param var_name:
    :return:
    """
    os.system('wmic ENVIRONMENT where "Name=\'' + var_name + '\'" delete')


def rename_system_env_var_permanently(old_name, new_name):
    """
    Rename ENVIRONMENT VAR
    :param old_name:
    :param new_name:
    :return:
    """
    var_value = os.getenv(old_name)
    remove_system_env_var_permanently(old_name)
    add_system_env_var_permanently(new_name, var_value)
    # os.system('wmic ENVIRONMENT where Name=\'' + old_name + '\' set Name=\'' + new_name + '\'')


def add_system_env_var_permanently(var_name, var_value):
    """
    Add ENVIRONMENT VAR
    :param var_name:
    :param var_value:
    :return:
    """

    os.environ[var_name] = var_value
    os.system('wmic environment create name=\'' + var_name + '\', username=' + os.getenv(
        'USERNAME') + ', variablevalue=\'' + var_value + '\'')


def update_system_env_value_permanently(var_name, var_value):
    """
    Update ENVIRONMENT VAR value
    :param var_name:
    :param var_value:
    :return:
    """

    os.environ[var_name] = var_value
    os.system('wmic environment where name=\'' + var_name + '\' set variablevalue=\'' + var_value + '\'')


def refresh_terminal_env_var():
    """
    Refresh ENVIRONMENT VAR in current session
    :return:
    """
    os.system('RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters')
    # os.system('refreshenv')


def parse_maya_env(maya_env_path):
    """
    Parse Maya.env
    :param maya_env_path: string - file path
    :return: dict - dict with ENV VAR as key and string value
    """
    var_dict = {}
    with open(maya_env_path, "r") as file:
        for line in file:
            try:
                var, value = line.replace(' ', '').replace('\n', '').split('=')
            except:
                var = None
                value = None

            var_dict[var] = value

    return var_dict


def write_maya_env(maya_env_path, var_dict):
    """
    Write Maya.env
    :param maya_env_path: string - file path
    :param var_dict: dict - dict with ENV VAR as key and string value
    :return:
    """
    lines = []
    for key, value in var_dict.items():
        line = ''
        if isinstance(value, str):
            line = key + ' = ' + value
        if isinstance(value, list):
            line = key + ' = ' + ';'.join(value)

        line = line + '\n'
        lines.append(line)

    with open(maya_env_path, "w") as file:
        file.writelines(lines)


def search_env_file(root_file_path):
    """
    Search all .env files in directory with recursion
    :param root_file_path: string
    :return: list of string
    """
    env_files = []
    for path in pathlib.Path(root_file_path).rglob('*.env'):
        env_files.append(str(path))

    return env_files


def write_main_usersetup(usersetup_path, data):
    pass


if __name__ == '__main__':
    # Print the value
    print(get_system_env_var('WORKSPACES'))
    env_vars = list(os.environ.keys())
    print(env_vars)
    # parse_maya_env('C:\Test\Maya.env')
