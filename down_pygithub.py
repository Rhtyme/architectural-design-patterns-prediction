import time

import github.PaginatedList
import requests
import re
import os
import pathlib
import zipfile
from github import Github

from datetime import date, timedelta

mvvm_keyword = 'mvvm'
mvp_keyword = 'mvp'

pathlib.Path('./mvvm/repos').mkdir(parents=True, exist_ok=True)

pathlib.Path('./mvp/repos').mkdir(parents=True, exist_ok=True)

query_android = 'android'

query_language = 'language:Java'

repo_zip_url_postfix_start = '/archive/refs/heads/'

# using an access token
g = Github("")


def get_query_created(start_date, end_date):
    return "created:" + start_date.strftime("%Y-%m-%d") + ".." + end_date.strftime("%Y-%m-%d")


def get_filename_from_cd(content_disposition):
    """
    Get filename from content-disposition
    """
    if not content_disposition:
        return None
    fname = re.findall('filename=(.+)', content_disposition)
    if len(fname) == 0:
        return None
    return fname[0]


def download_repo(folder_to, repo_url, default_branch):
    repo_zip_url = repo_url + repo_zip_url_postfix_start + default_branch + '.zip'
    try:
        repo_request = requests.get(str(repo_zip_url), allow_redirects=True)
        repo_name = get_filename_from_cd(repo_request.headers.get('content-disposition'))
        print('downloading repo: ', repo_url)
        if not repo_name:
            raise Exception('repo name can not be fetched')
        repo_zipfile_full_path = os.path.join(folder_to, repo_name)
        open(repo_zipfile_full_path, 'wb').write(repo_request.content)
    except Exception as e:
        print('can\'t download repo: ', repo_zip_url, ', error:', e)
        return False
    return True


def download_repos_by_query(folder_to, full_query):
    q_repos = g.search_repositories(query=full_query)
    if q_repos.totalCount <= 0:
        return
    print('downloading for period: ', full_query, ', total: ', q_repos.totalCount)

    for i in range(0, 33):
        p_repos = q_repos.get_page(i)
        if len(p_repos) == 0:
            break
        for repo in p_repos:
            download_repo(folder_to, repo.html_url, repo.default_branch)
            time.sleep(1)
        time.sleep(1)


def download_repos_between_date_range(folder_to, pattern_query):
    start_date = date(2013, 1, 1)
    end_date = date(2022, 3, 16)
    delta = timedelta(days=180)
    delta_period = timedelta(days=179)

    while start_date <= end_date:
        next_date = start_date + delta_period
        created_query = get_query_created(start_date, next_date)
        full_query = query_android + " " + pattern_query + " " + query_language + " " + created_query
        download_repos_by_query(folder_to, full_query)
        start_date += delta


def unzip_repos(root_folder, repo_folder='repos'):
    root_path = pathlib.Path(root_folder)
    target_folder_to_unzip = root_path / repo_folder
    target_folder_to_unzip.mkdir(parents=True, exist_ok=True)
    for zipped_repo in root_path.glob('*.zip'):
        with zipfile.ZipFile(zipped_repo, 'r') as zipfile_repo:
            zipfile_repo.extractall(target_folder_to_unzip)


if __name__ == '__main__':
    download_repos_between_date_range(mvvm_keyword, mvvm_keyword)
    download_repos_between_date_range(mvp_keyword, mvp_keyword)

    unzip_repos(mvvm_keyword)
    unzip_repos(mvp_keyword)
