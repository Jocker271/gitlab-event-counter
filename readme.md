# GitLab Event Counter


![Python](https://img.shields.io/badge/Python-v3.10-informational)
![Author](https://img.shields.io/badge/made_by-Jocker271-871c1c)

This script counts the number of GitLab events from certain users within a certain period of time.

It is particularly suitable for evaluating useless KPIs at the end of the year within a team. 😉

## Setup
To run this script, you need to add an access token with the "read_user" permission in your GitLab user settings and save it with other parameters in env.py file. See env.py for more information or just take a look in the simple script code.

## Usefull Links
- Add API token: https://gitlab.com/-/user_settings/personal_access_tokens
- More information about GitLab API: https://docs.gitlab.com/ee/api/events.html