import ntpath
from base64 import b64encode
from typing import Union
from urllib.parse import quote_plus

import requests

from src.root_log import logger


class GitLabManager:
    """单个项目的gitlab管理器"""

    def __init__(self, private_token: str, project_id: int):
        self._host = "https://gitlab.com/api/v4/"
        self._version = "v4"
        self._private_token = private_token
        self._project_id = project_id
        self._ref = "main"
        self._headers = {
            "Private-Token": self._private_token
        }
        # self._project_info = self._get_project_info()
        self._raw_host = "https://gitlab.com/{}/-/raw/main/{}"
        self._proxies = {"http": None, "https": None}

    def projects_access_requests(self):
        url = f"projects/{self._project_id}/access_requests"
        resp = self.get(url, timeout=3)
        if resp.status_code == 200:
            return True, "ok"
        result = resp.json()
        return False, result.get("message")

    def get_file_address(self, file_path):
        return self._host + f"projects/{self._project_id}/repository/files/{quote_plus(file_path)}/raw"

    def post(self, url, data=None, headers=None, **kwargs):
        headers = {**self._headers, **(headers or {})}
        logger.info("%s, data %s, headers %s" % (self._host + url, data, headers))
        return requests.post(self._host + url, headers=headers, data=data, proxies=self._proxies, **kwargs)

    def get(self, url, params=None, headers=None, **kwargs):
        headers = {**self._headers, **(headers or {})}
        logger.info("%s, params %s, headers %s" % (self._host + url, params, headers))
        return requests.get(self._host + url, headers=headers, params=params, proxies=self._proxies, **kwargs)

    def head(self, url, params=None, data=None, headers=None, **kwargs):
        logger.info(self._host + url)
        return requests.head(self._host + url, headers={**self._headers, **(headers or {})}, params=params, data=data,
                             proxies=self._proxies, **kwargs)

    def _get_project_info(self):
        return self.get(f"projects/{self._project_id}").json()

    def uploads(self, file_path: str):
        """上传文件"""
        resp = self.post(f"projects/{self._project_id}/uploads", files={'file': open(file_path, 'rb')})
        return resp.json()

    def create_file(self, file_name: str, file_content: Union[bytes, str], commit_message="create new file: {}"):
        if isinstance(file_content, str):
            file_content = file_content.encode("utf-8")
        file_content = b64encode(file_content).decode()
        url = f"projects/{self._project_id}/repository/files/{quote_plus(file_name)}"
        data = {"branch": self._ref,
                "author_email": "1032939141@qq.com",
                "author_name": "GitLabManager",
                "encoding": "base64",
                "content": file_content,
                "commit_message": commit_message.format(file_name)}
        resp = self.post(url, json=data, timeout=10)
        status_code = resp.status_code
        result = resp.json()
        if status_code == 201:
            link = self.get_file_address(result.get("file_path"))

            return True, link
        return False, result.get("message")

    def create_file_from_path(self, file_path):
        return self.create_file(ntpath.basename(file_path), open(file_path, "rb").read())

    def get_file(self, file_name: str):
        """
        {'blob_id': '0b5119d31fa2c023ecce0977aed2ed350485bebc',
         'commit_id': '012b7cf97d4ce429c63e7efd7d944272eb9b0971',
         'content': '5oiR5LiK6K++55S16K+d5Y2h5Yeg6IqC6K++5aSn5YGl5bq355m+',
         'content_sha256': '4f6a319aeb143daa8fddefdd59b25190f67d7b28c06474bb4002d8547ce30ee4',
         'encoding': 'base64',
         'execute_filemode': False,
         'file_name': '3.txt',
         'file_path': '3.txt',
         'last_commit_id': '55f7098923095eacbe681d4a26983c23c913bcd5',
         'ref': 'main',
         'size': 39}
        """
        url = f"projects/{self._project_id}/repository/files/{quote_plus(file_name)}"
        resp = self.get(url, params={"ref": self._ref})
        return resp.json()

    def head_file(self, file_name: str):
        """
        {'X-Gitlab-Blob-Id': '0b5119d31fa2c023ecce0977aed2ed350485bebc',
         'X-Gitlab-Commit-Id': '012b7cf97d4ce429c63e7efd7d944272eb9b0971',
         'X-Gitlab-Content-Sha256': '4f6a319aeb143daa8fddefdd59b25190f67d7b28c06474bb4002d8547ce30ee4',
         'X-Gitlab-Encoding': 'base64',
         'X-Gitlab-Execute-Filemode': 'false',
         'X-Gitlab-File-Name': '3.txt',
         'X-Gitlab-File-Path': '3.txt',
         'X-Gitlab-Last-Commit-Id': '55f7098923095eacbe681d4a26983c23c913bcd5',
         'X-Gitlab-Ref': 'main',
         'X-Gitlab-Size': '39'}
        """
        url = f"projects/{self._project_id}/repository/files/{quote_plus(file_name)}"
        return self.head(url, params={"ref": self._ref}).headers

    def get_file_content(self, file_name) -> bytes:
        url = f"projects/{self._project_id}/repository/files/{quote_plus(file_name)}/raw"
        resp = self.get(url, params={"ref": self._ref})
        return resp.content


if __name__ == '__main__':
    manager = GitLabManager('glpat-rQEUwmCQdz6htzU6sNze', 42641795)
    # manager = GitLabManager('glpat-rQEUwmCQdz6htzU6sN', 42641123)
    # print(manager.project_info)
    # print(manager.uploads("2.svg"))
    # print(manager.create_file("robot_maze2.png", open("robot_maze.png", "rb").read()))
    # print(manager.create_file("3.txt", "我上课电话卡几节课大健康百"))
    # x_png = manager.get_raw_file("20230117114646.png")
    # open("x.png", "wb").write(x_png)
    # print(manager.head_file("3.txt"))
    # print(manager.get_file("3.txt"))
    print(manager.projects_access_requests())
