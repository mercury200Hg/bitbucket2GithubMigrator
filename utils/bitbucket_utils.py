import json
import os
from typing import List, Dict

from atlassian import rest_client


class Bitbucket:

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = os.environ.get('BITBUCKET_TOKEN', password)
        self.bitbucket_api_url = 'https://api.bitbucket.org'
        self.api_version = '2.0'
        self.rest_client = rest_client.AtlassianRestAPI(url=self.bitbucket_api_url, username=self.username,
                                                        password=self.password)

    @staticmethod
    def get_instance(username, password):
        return Bitbucket(username=username, password=password)

    def get_projects_in_workspace(self, workspace: str) -> List[Dict]:
        """
        Provides list of projects in a workspace
        :param workspace: Name of workspace
        :type workspace: str
        :return: List of Dict having Key and Name of projects in given workspace
        :rtype: list(dict())
        """
        result = list()
        try:
            data = self.rest_client.get(path='{}/workspaces/{}/projects'.format(self.api_version, workspace))
            values = data.get('values', list())
            for item in values:
                result.append({
                    'Key': item.get('key'),
                    'Name': item.get('name')
                })
        except Exception as e:
            print(e.__traceback__)
        return result

    def get_repositories_in_workspace(self, workspace: str) -> List[Dict]:
        """
        Provides list of repositories in a given workspace
        :param workspace: Name of workspace
        :type workspace: str
        :return: List of dict having Repository Name, CLONE URL for both https and ssh
        :rtype: list(dict())
        """
        result = list()
        try:
            data = self.rest_client.get(path='{}/repositories/{}'.format(self.api_version, workspace))
            values = data.get('values', list())

            for item in values:
                https_clone_url = ''
                ssh_clone_url = ''
                clone_links = item.get('links', dict()).get('clone', list())
                for cl in clone_links:
                    if cl.get('name') == 'https':
                        https_clone_url = cl.get('href')
                    elif cl.get('name') == 'ssh':
                        ssh_clone_url = cl.get('href')

                result.append({
                    'Name': item.get('name'),
                    'HTTPS_CLONE_URL': https_clone_url,
                    'SSH_CLONE_URL': ssh_clone_url
                })
                # print(json.dumps(item, sort_keys=True, indent=4))
        except Exception as e:
            print(e.__traceback__)
        return result

    def get_workspaces(self) -> List:
        """
        Returns the list of all workspaces of which a user is part of
        :return: Returns the list of all workspaces of which a user is part of
        :rtype: list
        """
        result = list()
        try:
            data = self.rest_client.get(path='{}/user/permissions/workspaces'.format(self.api_version))
            values = data.get('values', list())
            for item in values:
                result.append(item.get('workspace', dict()).get('slug'))
        except Exception as e:
            print(e.__traceback__)
        return result


if __name__ == '__main__':
    bitbucket = Bitbucket.get_instance(username='mercury200hg-freelancer', password=None)
    workspaces = bitbucket.get_workspaces()
    # print(workspaces)
    for ws in workspaces:
        projects = bitbucket.get_projects_in_workspace(workspace=ws)
        # print(ws, projects)
        repos = bitbucket.get_repositories_in_workspace(workspace=ws)
        print('Workspace: {}'.format(ws))
        print('Projects: {}'.format(json.dumps(projects, indent=4, sort_keys=True)))
        print('Repositories: {}'.format(json.dumps(repos, indent=4, sort_keys=True)))
        print("################################################")
