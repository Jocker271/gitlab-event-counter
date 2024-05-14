#!/usr/bin/python

import requests
import env

# This script counts the number of GitLab events from certain users within a
# certain period of time. To run it, you need to add an access token with the
# "read_user" permission in your GitLab user settings and save it with other
# parameters in env.py file.

# Add API token: https://gitlab.com/-/user_settings/personal_access_tokens
# More information about GitLab API: https://docs.gitlab.com/ee/api/events.html


def print_event_counts(
    gitlab_url, oauth_token, names_list, date_after, date_before, action
):
    """Prints the user event count for each user in the given names_list"""
    gitlab = GitLabRequest(gitlab_url, oauth_token)
    print(
        f"User Events between {date_after} and {date_before} "
        f"filtered by action '{action}':"
    )
    for user in names_list:
        count = gitlab.search_count_user_event(
            user,
            date_after=date_after,
            date_before=date_before,
            action=action,
        )
        print(f"{user}: {count}")


class GitLabRequest:
    def __init__(self, gitlab_url, oauth_token):
        self.gitlab_url = gitlab_url
        self.oauth_token = oauth_token

    def get_user_id_by_name(self, username):
        """Returns the if of the user with the given username"""
        user_url = f"{self.gitlab_url}/api/v4/users?username={username}"
        user_data = requests.get(
            user_url, headers={"Private-Token": self.oauth_token}
        ).json()
        user_id = user_data[0].get("id") if user_data else False
        return user_id

    def get_user_event_count(
        self, user_id, date_after=None, date_before=None, action=None
    ):
        """Returns the count of events (int) of a given user in a period"""
        event_count = 0
        event_url = f"{self.gitlab_url}/api/v4/users/{user_id}/events?"
        if date_after:
            event_url += f"after={date_after}&"
        if date_before:
            event_url += f"before={date_before}&"
        if action:
            event_url += f"action={action}&"
        page = 1
        limit = 20
        last_response = limit
        while not last_response < limit:
            event_batch_url = f"{event_url}page={page}&per_page={limit}"
            data = requests.get(
                event_batch_url, headers={"Private-Token": self.oauth_token}
            ).json()
            last_response = len(data)
            event_count += last_response
            page += 1
        return event_count

    def search_count_user_event(
        self,
        username,
        date_after="2024-05-06",
        date_before="2024-05-30",
        action=None,
    ):
        """Handels the user event cound for a given username and period"""
        user_id = self.get_user_id_by_name(username)
        if user_id:
            event_count = self.get_user_event_count(
                user_id, date_after, date_before, action
            )
            search_result = event_count
        else:
            search_result = "ERROR - User not found"
        return search_result


if __name__ == "__main__":
    try:
        print_event_counts(
            gitlab_url=env.GITLAB_URL,
            oauth_token=env.OAUTH_TOKEN,
            names_list=env.NAMES_LIST,
            date_after=env.DATE_AFTER,
            date_before=env.DATE_BEFORE,
            action=env.ACTION,
        )
    except AttributeError:
        print("You must first setup the env.py")
    except requests.exceptions.ConnectionError:
        print("Failed to establish a connection. Check you URL and token!")
    exit()