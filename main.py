import requests
import json
from datetime import datetime


def get_page(page: int) -> dict:
    """
    Get the specified page from the US News endpoint.
    :param page: the page number to get
    :return: the json data of that page.
    """
    r = requests.get(
        f"https://www.usnews.com/best-graduate-schools/api/search?program=top-science-schools&specialty=computer-science&_page={page}",
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",

        })
    return r.json()


def get_data(max_pages: int = 100) -> dict:
    """
    Gets up to the 200 colleges from the US News computer science endpoint. Sorts relevant info into a dict.
    :param max_pages: the max amount of pages to go through (I.E u only want the first 3 pages)
    :return: the dict it creates bound to max pages
    """
    colleges = {}
    page = 1
    json = get_page(page)
    while len(json['data']['items']) != 0 and page <= max_pages:
        for college in json['data']['items']:
            rank = college['ranking']['display_rank']
            if rank not in colleges:
                colleges[rank] = []
            colleges[rank].append({'name': college['name'], 'city': college['city'],
                                   'state': college['state'], 'url': college['url'],
                                   'score': float(college['schoolData']['c_avg_acad_rep_score']),
                                   'id': college['id'], 'fice_code': college['fice_code'], 'rank': int(rank)
                                   })
        page += 1
        json = get_page(page)
        print(page)
    return colleges


def get_by_state(colleges, state) -> list:
    """
    Find all college in a certain state
    :param colleges: the data to look through.
    :param state: the state to look for
    :return: all colleges in the given state
    """
    state = state.upper()
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['state'] == state:
                ret.append(college)
    return ret


def get_by_city(colleges, city: str) -> list:
    """
    Find all colleges by the city it's in
    :param colleges: the data to look through.
    :param city: the city to look for
    :return: all colleges that city matches the given city
    """
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['city'] == city:
                ret.append(college)
    return ret


def get_by_name(colleges, name: str) -> list:
    """
    Find a college by it's name.
    :param colleges: the data to look through.
    :param name: the name of the college to look for
    :return: the college that matches the name
    """
    name = name.lower()
    for college_info in colleges.values():
        for college in college_info:
            if college['name'].lower() == name:
                return college
    return []


def get_by_score(colleges, score: float) -> list:
    """
    Find all colleges that has the given score.
    :param colleges: the data to look through.
    :param score: the score to look for.
    :return: all colleges that has the given score.
    """
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['score'] == score:
                ret.append(college)
    return ret


def get_by_score_within(colleges, minimum: float, maximum: float) -> list:
    """
    Find all colleges within two scores (max 5.0)
    :param colleges: the data to look through.
    :param minimum: the minimum score to look for.
    :param maximum: the maximum score to look for.
    :return: all colleges within the given score range.
    """
    ret = []
    if max(maximum, minimum) > 5.0:
        raise Exception("The max score can only be 5.0.")
    for college_info in colleges.values():
        for college in college_info:
            if minimum <= college['score'] <= maximum:
                ret.append(college)
    return ret


def get_by_id(colleges, college_id: str) -> dict:
    """
    Find a college by the college's ID.
    :param colleges: the data to look through.
    :param college_id: The college ID to look for.
    :return: the college that matches the given ID.
    """
    for college_info in colleges.values():
        for college in college_info:
            if college['id'] == college_id:
                return college
    return {}


def get_by_fice(colleges, fice_code: str) -> dict:
    """
    Find a college by it's FICE code.
    :param colleges: the data to look through.
    :param fice_code: the FICE code to look for.
    :return: the college that matches the FICE code.
    """
    for college_info in colleges.values():
        for college in college_info:
            if college['fice_code'] == fice_code:
                return college
    return {}


def get_by_rank(colleges, pos) -> list:
    """
    Gives colleges that have a certain rank.
    :param colleges: the data to look through.
    :param pos: the position to search for.
    :return: list of all colleges with that rank.
    """
    try:
        return colleges[pos]
    except KeyError:
        return []


def dump_data(colleges, file_name: str = "colleges", timestamp: str = None):
    """
    Dumps the given data to a specified json file.
    :param colleges: the data to dump.
    :param file_name: the file  name to dump the data to default is colleges.json.
    :param timestamp: non default timestamp if you'd like the key for the data to be different.
    :return: None.
    """
    if timestamp is None:
        timestamp = datetime.timestamp(datetime.now())
    j = json.load(open(f"./{file_name}.json", "r"))
    j[timestamp] = colleges
    json.dump(j, open(f"./{file_name}.json", "w+"), indent=4, ensure_ascii=True)
    print(f"dumped JSON data to ./{file_name}.json")


if __name__ == '__main__':
    data = get_data()
    while True:
        choice = input("Select an option\n1. Search by name\n2. Search by state\n3. Search by city\n4. Get a certain "
                       "score\n5. Get by score within ranges\n6. Get by FICE Score\n7. Get by ID\n8. Get all colleges "
                       "in a certian rank\n9. Dump data to JSON\n")
        if choice == "1":
            name_ = input("Enter the name to search: ")
            print(get_by_name(data, name_))
        elif choice == "2":
            state_ = input("Enter the state to search: ")
            print(get_by_state(data, state_))
        elif choice == "3":
            city_ = input("Enter the city to search: ")
            print(get_by_city(data, city_))
        elif choice == "4":
            score_match = float(input("Enter score to match (1 decimal): "))
            print(get_by_score(data, score_match))
        elif choice == "5":
            score_match_min = float(input("Enter the minimum score (1 decimal): "))
            score_match_max = float(input("Enter the maximum score (1 decimal): "))
            print(get_by_score_within(data, score_match_min, score_match_max))
        elif choice == "6":
            FICE_code = input("Enter the FICE Code")
            print(get_by_fice(data, FICE_code))
        elif choice == "7":
            id_ = input("Enter the college ID: ")
            print(get_by_id(data, id_))
        elif choice == "8":
            rank_ = input("Enter the rank: ")
            colleges_ = get_by_rank(data, rank_)
            print(f" ".join([x['name'] for x in colleges_]))
        elif choice == "9":
            dump_data(data)
        else:
            break
        print("\n")
