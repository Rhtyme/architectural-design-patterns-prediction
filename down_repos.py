import requests
import re
import os
import pathlib
import zipfile
import time

import uuid

mvvm_keyword = 'mvvm'
mvp_keyword = 'mvp'

pathlib.Path('./mvvm/repos').mkdir(parents=True, exist_ok=True)

pathlib.Path('./mvp/repos').mkdir(parents=True, exist_ok=True)

# full url in the example of mvvm: https://api.github.com/search/repositories?l=Java&q=mvvm+android&page=1
search_url_1 = 'https://api.github.com/search/repositories?l=Java&q=android+'
search_url_2 = '+language:Java&page='

# repo_zip_url_postfix = '/archive/refs/heads/master.zip'
repo_zip_url_postfix_start = '/archive/refs/heads/'

mvvm_search_url = search_url_1 + mvvm_keyword + search_url_2
mvp_search_url = search_url_1 + mvp_keyword + search_url_2


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
        if not repo_name:
            raise Exception('repo name can not be fetched')
        repo_name = uuid.uuid4().hex + repo_name
        repo_zipfile_full_path = os.path.join(folder_to, repo_name)
        open(repo_zipfile_full_path, 'wb').write(repo_request.content)
    except Exception as e:
        print('can\'t download repo: ', repo_zip_url, ', error:', e)
        return False
    return True


def validate_dict(repos_dict):
    try:
        total_count = repos_dict['total_count']
        current_page_count = len(repos_dict['items'])
        if total_count > 0 and current_page_count > 0:
            return True
    except Exception as e:
        print('can\'t validate repos: ', e)
        return False
    return False


def download_repos(folder_to, search_url):
    total_count = -1
    counter_repos = 0
    failed_repos_counter = 0
    pattern_folder = os.path.join(os.getcwd(), folder_to)
    failed_repos_break_limit = 40
    # when the program fails to validate the repos dictionary (from request),
    # the below variable will be increased every time, and once succeeded, zero will be set as a value
    fail_validate_counter = 0
    # when the value of fail_validate_counter reaches the value of fail_validate_limit, then no promise for luck,
    # the program will be terminated
    fail_validate_limit = 10

    page_counter = 0

    for i in range(1, 10000):
        page_counter += 1
        final_search_url = search_url + str(page_counter)
        search_page = requests.get(final_search_url)
        repos_dict = search_page.json()

        validated = validate_dict(repos_dict)
        if validated:
            fail_validate_counter = 0
        else:
            fail_validate_counter += 1
            page_counter -= 1

            if failed_repos_counter >= fail_validate_limit:
                print('too many failures on validating dict, tried ', failed_repos_counter, ' times')
                break
            else:
                continue

        total_count = repos_dict['total_count']
        current_page_count = len(repos_dict['items'])
        counter_repos += current_page_count
        inner_page_counter = 0
        for repo_item in repos_dict['items']:
            repo_url = repo_item['html_url']
            default_branch = repo_item['default_branch']
            inner_page_counter += 1

            print('downloading repo# ', ((page_counter - 1) * current_page_count + inner_page_counter), ' out of# ', total_count,
                  ', repo_name: ',
                  repo_url)
            succeed = download_repo(pattern_folder, repo_url, default_branch)
            time.sleep(2)
            if not succeed:
                failed_repos_counter += 1
                print('can\'t downloaded repo: ', repo_url)
            if failed_repos_counter >= failed_repos_break_limit:
                break
        else:
            if counter_repos >= total_count:
                break
            continue
        break


def unzip_repos(root_folder, repo_folder='repos'):
    root_path = pathlib.Path(root_folder)
    target_folder_to_unzip = root_path / repo_folder
    target_folder_to_unzip.mkdir(parents=True, exist_ok=True)
    for zipped_repo in root_path.glob('*.zip'):
        with zipfile.ZipFile(zipped_repo, 'r') as zipfile_repo:
            zipfile_repo.extractall(target_folder_to_unzip)


if __name__ == '__main__':
    download_repos(mvvm_keyword, mvvm_search_url)
    download_repos(mvp_keyword, mvp_search_url)

    unzip_repos(mvvm_keyword)
    unzip_repos(mvp_keyword)
