import requests
import os
import json

bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


def create_url(usernames):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = f"usernames={','.join(usernames)}"
    user_fields = "user.fields=public_metrics,id,name"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request(
        "GET",
        url,
        auth=bearer_oauth,
    )
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main(usernames):
    url = create_url(usernames)
    json_response = connect_to_endpoint(url)

    return json_response["data"]


if __name__ == "__main__":
    main()
