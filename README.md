# Gitlab-Searcher
python3 script that pulls gitlab data of interest using a gitlab personal access token

Pre-req:
`pip3 install requirements.txt` (will install the requests library)


To run:
`python3 gitlab-searcher.py -s [base_gitlab_url] -t [personal_access_token]`
Example: 
`python3 gitlab-searcher.py -s https://api.gitlab.com -t reallycooltoken`

This script currently attempts to collect the following:

- List projects
- List branches and permission info per branch
- List jobs
- List groups that the user (who's token you are using) is a part of 
- List PeronsalAccessToken info (names, permissions, and active/inactive info for each of the user's PATs)
- List Project Variables (might find interesting info)
- List Project Pipeline Variables (might find interesting info)
