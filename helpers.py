import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment

def request_and_save(url: str, save_path: str):
    '''
    Docstring for request_and_parse
    
    :param url: URL to request
    :return: BeautifulSoup object of the parsed HTML
    '''
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    html_content = response.content
    save_html(html_content, save_path)


def save_html(html: bytes, path: str):
        '''
        Docstring for save_html
        
        :param html: bytes from requests.get().content
        :param path: where to save the html file
        :return: None
        '''
        with open(path, "wb") as f:
            f.write(html)

def isComment(element):
    return isinstance(element, Comment)

def create_parse(file_path: str) -> BeautifulSoup:
    '''
    Docstring for parse_html
    
    :param file_path: path to the HTML file
    :return: BeautifulSoup object of the parsed HTML
    '''
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

def transaction_list_to_table(transaction_list: list[str]) -> pd.DataFrame:
    '''
    Docstring for transaction_list_to_table
    
    :param transaction_list: Description
    :type transaction_list: list[str]
    :return: Description
    :rtype: DataFrame
    '''
    # Logic to convert transaction_list into a structured DataFrame
    # Date is before colon
    # If first word is "Signed", then new team is after "with the". Check if the new team is the same as the old team.
    # If the first word is "Traded", then the new team is after "to the".
    # If the first word is "Waived", then the new team is None.
    # If the first word is "Drafted", then the new team is after "by the". Draft number is after "in the (0-9)** round". Draft year is after "of the" or the year in the date.
    # If the event starts with "As part of a (0-9)-team trade, traded", then the new team is after the first "to the". Can delete everything after ';' and everything before "traded", then do the normal traded logic.
    # If the event starts with "Assigned", then new team is after "to the". Draft number is None. Do not reassign curr_team.
    # If the event starts with "Recalled", then the new team is the current team. Draft number is None.

    dates = []
    event_type = []
    new_teams = []
    supplementary_info = []
    curr_team = ""
    for transaction in transaction_list:
        date, event = transaction.split(":", 1)
        print(date)
        if event.strip().startswith("Drafted"):
            dates.append(date.strip())
            event_type.append("Drafted")
            parts = event.strip().split("by the")
            team_part = parts[1].split("in the")[0].strip()
            new_teams.append(team_part)
            info = parts[1].split("in the")[1].strip()
            supplementary_info.append(info)
            curr_team = team_part
        elif event.strip().startswith("Signed"):
            team_part = event.strip().split("with the")[1].split(".")[0].strip()
            if team_part != curr_team:
                dates.append(date.strip())
                event_type.append("Signed")
                team_part = event.strip().split("with the")[1].split(".")[0].strip()
                new_teams.append(team_part)
                supplementary_info.append(None)
                curr_team = team_part
        elif event.strip().startswith("Traded"):
            dates.append(date.strip())
            event_type.append("Traded")
            team_part = event.strip().split("to the")[1].split("for")[0].strip()
            new_teams.append(team_part)
            with_part = event.strip().split("with")
            info = ("with " + with_part[1].split("to the")[0].strip() if len(with_part) > 1 and len(with_part[1].split("to the")) > 1 else "") + ("for " + event.strip().split("for")[1].strip())
            supplementary_info.append(info)
            curr_team = team_part
        elif event.strip().startswith("Waived"):
            dates.append(date.strip())
            event_type.append("Waived")
            new_teams.append(None)
            supplementary_info.append("from " + curr_team)
        elif event.strip().startswith("As part of a"):
            dates.append(date.strip())
            event_type.append("Traded")
            trade_part = event.strip().split(";")[0]
            team_part = trade_part.split("to the")[1].strip()
            new_teams.append(team_part)
            with_parts = event.strip().split("with")
            info = ("with " + with_parts[1].split("to the")[0].strip() if len(with_parts) > 1 and len(with_parts[1].split("to the")) > 1 else None)
            supplementary_info.append(info)
            curr_team = team_part
        elif event.strip().startswith("Assigned"):
            dates.append(date.strip())
            event_type.append("Assigned")
            team_part = event.strip().split("to the")[1].split('of')[0].strip()
            new_teams.append(team_part)
            supplementary_info.append(curr_team)
        elif event.strip().startswith("Recalled"):
            dates.append(date.strip())
            event_type.append("Recalled")
            new_teams.append(curr_team)
            supplementary_info.append(team_part)
        elif event.strip().startswith("Retired"):
            dates.append(date.strip())
            event_type.append("Retired")
            new_teams.append(None)
            supplementary_info.append('Was with ' + curr_team)

    df = pd.DataFrame({
    "Date": dates,
    "Event": event_type,
    "New Team": new_teams,
    "Supplementary Info": supplementary_info
    })
    df['next'] = df.index + 1
    df['next'] = df['next'].apply(lambda x: x if x < len(df) else None)
    df = df.reset_index(drop=True)
    return df

def transactions_table(soup: BeautifulSoup) -> pd.DataFrame:
    '''
    Docstring for transactions_table
    
    :param soup: BeautifulSoup object of the parsed HTML
    :return: DataFrame containing the transactions data
    '''
    transactions = soup.select_one('#all_transactions')
    comments = transactions.find_all(string=isComment)[0]
    commentsoup = BeautifulSoup(comments, "html.parser").text.strip()
    transaction_list = commentsoup.split('\n')
    return transaction_list_to_table(transaction_list)
