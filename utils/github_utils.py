import os
import json
from github import Github , Organization


class GithubUtils:
    def __init__(self, username: str = None, access_token: str = None):
        self.username = username
        self.access_token = os.environ.get('GITHUB_ACCESS_TOKEN', access_token)
        self.github = Github(login_or_token=access_token)

    @staticmethod
    def get_instance(username, access_token):
        return GithubUtils(username=username, access_token=access_token)

    def import_repository_in_org(self, org_name: str = None):
        data = self.github.get_organization(login='mercury200Hg-freelancer-ws1')

        print(data.__dict__)
        pass


if __name__ == '__main__':
    github_utils = GithubUtils.get_instance(username='mercury200hg-freelancer',
                                            access_token=None)
    # github_utils.create_organisation()
