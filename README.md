# download-github-repos

This repo contains the source code for the research paper **Towards predicting architectural design patterns: a machine learning approach**.

## The description of the files:
- **utils/down_repos.py** - Deprecated! (do not use this script, since this script is limited because it does not support authentication  use instead **utils/down_pygithub.py**) script to download repositories from github with the tag android, MVVM, MVP and programming language: java
- **utils/down_pygithub.py** - script that uses **pygithub** package to download repositories from github with the tag android, MVVM, MVP and programming language: java and given time interval (time interval to avoid the github API restrictions). 
- **utils/extract_ck.py** - script for extracting the results of the CK metrics applied on the downloaded repositories. As a result of this script, the **mvp_ck.zip** and **mvvm_ck.zip** files are generated that contains the zipped CK metrics results for repositories under MVP and MVVM architecture, respectively.
- **utils/upload_to_dropbox.py** - optional script for uploading the CK metrics result files (**mvp_ck.zip** and **mvvm_ck.zip**), in case if these scripts are being used in the cloud servers.
- **utils/requirements.txt** - requirements file that contains the list of python packages used by the scripts above
- **utils/utils.py** - the script that preprocesses the dataset and trains the ML models
- **src** folder contains the script (**main.py**) to run the training process in the **utils/utils.py** file
- **Data** folder contains the dataset
- **Notebooks** folder contains the Jupyter notebook file which we carried out the experiements.

## The steps to run the scripts (from the root directory of the repo):

- create a python environment: `python3 -m venv ./env`
- activate the python environment `source env/bin/activate`
- install the packages: `pip install -r requirements.txt`
- run the **utils/down_pygithub.py** script to download repos: `python down_pygithub.py`
- run the **utils/extract_ck.py** script to apply the CK metrics and extract the results (results are saved in **mvp_ck.zip** and **mvvm_ck.zip**): `python extract_ck.py`
- (optional) run **utils/upload_to_dropbox.py** to upload the scripts to your dropbox: `python upload_to_dropbox.py`
