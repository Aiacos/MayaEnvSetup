import os
import pathlib

import model


class ProjectParser(object):
    def __init__(self, init=True, worskapces_env_var='WORKSPACES'):
        self.worskapces_env_var = worskapces_env_var
        self.default_maya_path = pathlib.Path.home() / 'Documents' / 'maya' #/ '2022'
        #tlm_maya_path = pathlib.Path('C:\TLM\maya')

        default_maya_env = self.default_maya_path / 'Maya.env'
        #tlm_maya_env = tlm_maya_path / 'Default.env'

        if init:
            if model.get_system_env_var(self.worskapces_env_var) is not None:
                for project in self.get_projects():
                    print('Found workspaces: ', project)
            else:
                model.add_system_env_var_permanently(self.worskapces_env_var, str(self.default_maya_path) + ';')
                #self.add_projects(str(self.default_maya_path))

            if model.get_system_env_var('MAYA_ENV_DIR'):
                value = model.get_system_env_var('MAYA_ENV_DIR')
                if model.get_system_env_var('OLD_MAYA_ENV_DIR'):
                    self.add_projects(value)
                else:
                    model.rename_system_env_var_permanently('MAYA_ENV_DIR', 'OLD_MAYA_ENV_DIR')

    def get_maya_versions(self):
        # Search for Maya folders in the document folder
        maya_versions = []
        for root, dirs, files in os.walk(self.default_maya_path):
            for dir in dirs:
                if dir.isdigit():
                    maya_versions.append(dir)

        return maya_versions

    def get_projects(self):
        project_list = []
        for project in model.get_system_env_var(self.worskapces_env_var).split(';'):
            if project:
                project_list.append(project)

        return project_list

    def add_projects(self, project):
        project_list = self.get_projects()
        project_list.append(str(project))
        new_value = ';'.join(project_list)
        model.update_system_env_value_permanently(self.worskapces_env_var, new_value)

    def search_env_file(self, path):
        """
        List of Env files for one Path
        :param path:
        :return:
        """

        return model.search_env_file(path)


class EnvVarManager(object):
    def __init__(self):
        """
        Init Final Maya env
        """
        self.maya_env_dict = {}

    def get_env_as_list(self):
        """
        Get all env variables from main dict as list of string
        :return: list(str)
        """
        lines = []
        for key, value in self.maya_env_dict.items():
            line = ''
            if isinstance(value, str):
                line = key + ' = ' + value
            if isinstance(value, list):
                line = key + ' = ' + ';'.join(value)

            #line = line + '\n'
            lines.append(line)

        return lines

    def check_variable(self, env_var):
        """
        Check if variable it is already present in the dict
        :param env_var:
        :return:
        """
        try:
            var, value = env_var.replace(' ', '').replace('\n', '').split('=')
        except:
            var = None
            value = None

        if var in self.maya_env_dict.keys():
            if value in self.maya_env_dict[var]:
                return True

        return False


    def add_variable(self, env_var):
        """
        Parse Variable and add to the Dict
        :param env_var: string
        :return:
        """
        try:
            var, value = env_var.replace(' ', '').replace('\n', '').split('=')
        except:
            var = None
            value = None

        if var and value:
            if var in self.maya_env_dict.keys():
                if value not in self.maya_env_dict[var]:
                    self.maya_env_dict[var].append(value)
            else:
                self.maya_env_dict[var] = [value]

    def remove_variable_value(self, env_var):
        """
        Remove Variable form the Dict
        :param env_var: string
        :return:
        """
        try:
            var, value = env_var.replace(' ', '').replace('\n', '').split('=')
        except:
            var = None
            value = None

        if var and value:
            if var in self.maya_env_dict.keys():
                if value not in self.maya_env_dict[var]:
                    pass
                else:
                    value_list = self.maya_env_dict[var]
                    value_list.remove(value)
                    self.maya_env_dict[var] = value_list

        # cleanup dict
        clean_dict = {k: v for k, v in self.maya_env_dict.items() if v}
        self.maya_env_dict = clean_dict

    def remove_variable(self, env_var):
        """
        Remove Variable form the Dict
        :param env_var: string
        :return:
        """
        try:
            var, value = env_var.replace(' ', '').replace('\n', '').split('=')
        except:
            var = None
            value = None

        if var:
            del self.maya_env_dict[var]

    def write_env_file(self, maya_version='2022'):
        """
        Write Data to Maya.env in Documents folder
        :param maya_version:
        :return:
        """

        user_home = pathlib.Path.home()
        user_documents = 'Documents'
        maya_env_path = user_home / user_documents / 'maya' / maya_version / 'maya.env'
        model.write_maya_env(str(maya_env_path), self.maya_env_dict)
        print('Wrote file: ', maya_env_path)


if __name__ == '__main__':
    # parser = ProjectParser()
    maya_env = EnvVarManager()
