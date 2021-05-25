# Use the package we installed
import os
import spreadsheet
import time
import re
from slackclient import SlackClient
from typing import List, Dict, Any
from datetime import date, timedelta



# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )



def message_send_today(lst_dict: List[Dict[str, Any]]) -> List[Any]:
    """
    Converting data into lists.

    """
    out_list = []
    count = 2
    for dit in lst_dict:
        if date(dit['Year'], dit['Month'], dit['Day']) + timedelta(
                days=30) == date.today():
            temp_list = [
                dit["Date"], dit["username"], dit["Channel_Flag"],
                dit["Channel_id"], dit["Message"]
            ]
            out_list.append(temp_list)
            count += 1
    spreadsheet.sheet.delete_rows(2, count - 1)

    return out_list




# Start your app

###############################################################################
# ------------------------------helper functions-------------------------------#
def convert_data(lst_dict: List[Dict[str, Any]]) -> List[Any]:
    """
    Converting data into lists.

    """
    out_list = []

    for dit in lst_dict:
        if dit["Date"] == date.today() + timedelta(days=30):
            temp_list = [
                dit["Date"], dit["username"], dit["Channel_Flag"],
                dit["Channel_id"], dit["Message"]
            ]
            out_list.append(temp_list)
    return out_list




if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")



# .\env\Scripts\activate
# # Initializes your app with your bot token and signing secret
# app = App(
#     token=os.environ.get("SLACK_BOT_TOKEN"),
#     signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
# )
#
#
# # Add functionality here
# # @app.event("app_home_opened") etc
#
#
# @app.message("!cap")
# def say_hello(message, say):
#     user = message['user']
#     say(f"Hi there, <@{user}>!")
#     spreadsheet.append_data([date.today().isoformat(), date.today().year, date.today().month, date.today().day, user, "channel_id", "DM_F", "DM_id", "measfhjlaoishjfloscv"]))
#     )
#
#
# # Listens for messages containing "knock knock" and responds with an italicized "who's there?"
# @app.message("knock knock")
# def ask_who(message, say):
#     say("_Who's there?_")
#
#
# # Listens to incoming messages that contain "hello"
# @app.message("hello")
# def message_hello(message, say):
#     # say() sends a message to the channel where the event was triggered
#     say(f"Hey there <@{message['user']}>!")

# @app.event("app_home_opened")
# def update_home_tab(client, event, logger):
#     try:
#         # views.publish is the method that your app uses to push a view to the Home tab
#         client.views_publish(
#             # the user that opened your app's app home
#             user_id=event["user"],
#             # the view object that appears in the app home
#             view={
#                 "type": "home",
#                 "callback_id": "home_view",
#
#                 # body of the view
#                 "blocks": [
#                     {
#                         "type": "section",
#                         "text": {
#                             "type": "mrkdwn",
#                             "text": "*Welcome to your _App's Home_* :tada:"
#                         }
#                     },
#                     {
#                         "type": "divider"
#                     },
#                     {
#                         "type": "section",
#                         "text": {
#                             "type": "mrkdwn",
#                             "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
#                         }
#                     },
#                     {
#                         "type": "actions",
#                         "elements": [
#                             {
#                                 "type": "button",
#                                 "text": {
#                                     "type": "plain_text",
#                                     "text": "Click me!"
#                                 }
#                             }
#                         ]
#                     }
#                 ]
#             }
#         )
#
#     except Exception as e:
#         logger.error(f"Error publishing home tab: {e}")
