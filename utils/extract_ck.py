import os
import pathlib
import subprocess
import shutil
import sys

MVVM_REPOS = '../Data/mvvm/repos'
MVVM_CK_OUT = 'mvvm_ck_out'

MVP_REPOS = '../Data/mvp/repos'
MVP_CK_OUT = 'mvp_ck_out'


def extract_ck(from_folder, to_folder):
    repos_folder = pathlib.Path(from_folder)
    to_folder_path = pathlib.Path(to_folder)

    to_folder_path.mkdir(parents=True, exist_ok=True)

    arg_ck_jar_path = 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
    arg_true = 'true'
    arg_zero = '0'
    java_cmd = 'java'
    arg_jar = '-jar'
    counter = 0
    repos_folder_path = repos_folder.glob('*')
    repos_count = len(list(repos_folder_path))

    for repo_folder in repos_folder.glob('*'):
        counter += 1
        out_dir = pathlib.Path(to_folder) / repo_folder.name
        out_dir.mkdir(parents=True, exist_ok=True)
        print('repo_name: %s step: %d out of %d'%(repo_folder, counter, repos_count))

        try:
            arg_out_dir = str(out_dir) + '/'
            subprocess.call([java_cmd, arg_jar, arg_ck_jar_path, str(repo_folder), arg_true, arg_zero, arg_true, arg_out_dir])
        except Exception as e:
            print('problem occured: ', e)
            shutil.rmtree(out_dir)


if __name__ == '__main__':
    pathlib.Path(MVVM_CK_OUT).mkdir(parents=True, exist_ok=True)
    pathlib.Path(MVP_CK_OUT).mkdir(parents=True, exist_ok=True)

    extract_ck(MVVM_REPOS, MVVM_CK_OUT)
    extract_ck(MVP_REPOS, MVP_CK_OUT)
