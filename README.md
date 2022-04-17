# download-github-repos

This repo contains the source code for the research paper **Towards predicting architectural design patterns: a machine learning approach**.

## The description of the files:
- **down_repos.py** - Deprecated! (do not use this script, since this script is limited because it does not support authentication  use instead **down_pygithub.py**) script to download repositories from github with the tag android, MVVM, MVP and programming language: java
- **down_pygithub.py** - script that uses **pygithub** package to download repositories from github with the tag android, MVVM, MVP and programming language: java and given time interval (time interval to avoid the github API restrictions). 
- **extract_ck.py** - script for extracting the results of the CK metrics applied on the downloaded repositories. As a result of this script, the **mvp_ck.zip** and **mvvm_ck.zip** files are generated that contains the zipped CK metrics results for repositories under MVP and MVVM architecture, respectively.
- **upload_to_dropbox.py** - optional script for uploading the CK metrics result files (**mvp_ck.zip** and **mvvm_ck.zip**), in case if these scripts are being used in the cloud servers.
- **requirements.txt** - requirements file that contains the list of python packages used by the scripts above


## The steps to run the scripts (from the root directory of the repo):

- create a python environment: `python3 -m venv ./env`
- activate the python environment `source env/bin/activate`
- install the packages: `pip install -r requirements.txt`
- run the **down_pygithub.py** script to download repos: `python down_pygithub.py`
- run the **extract_ck.py** script to apply the CK metrics and extract the results (results are saved in **mvp_ck.zip** and **mvvm_ck.zip**): `python extract_ck.py`
- (optional) run **upload_to_dropbox.py** to upload the scripts to your dropbox: `python upload_to_dropbox.py`
