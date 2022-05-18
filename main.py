import requests
import json


def get_page(page: int) -> dict:
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


def get_data() -> dict:
    colleges = {}
    page = 1
    json = get_page(page)
    while len(json['data']['items']) != 0:
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
    return colleges


def get_by_state(colleges, state) -> list:
    state = state.upper()
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['state'] == state:
                ret.append(college)
    return ret


def get_by_city(colleges, city: str) -> list:
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['city'] == city:
                ret.append(college)
    return ret


def get_by_name(colleges, name: str) -> list:
    name = name.lower()
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['name'].lower() == name:
                ret.append(college)
    return ret


def get_by_score(colleges, score: float) -> list:
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if college['score'] == score:
                ret.append(college)
    return ret


def get_by_score_within(colleges, minimum: float, maximum: float) -> list:
    ret = []
    for college_info in colleges.values():
        for college in college_info:
            if minimum <= college['score'] <= maximum:
                ret.append(college)
    return ret


def get_by_id(colleges, college_id: str) -> dict:
    for college_info in colleges.values():
        for college in college_info:
            if college['id'] == college_id:
                return college
    return {}


def get_by_fice(colleges, fice_code: str) -> dict:
    for college_info in colleges.values():
        for college in college_info:
            if college['fice_code'] == fice_code:
                return college
    return {}


def get_by_rank(colleges, pos) -> list:
    return colleges[pos] or None


def dump_data(colleges, timestamp: str = None):
    if timestamp is None:
        try:
            from datetime import datetime
        except ImportError:
            print("Can't import datetime!")
            return
        timestamp = datetime.timestamp(datetime.now())
    j = json.load(open("./colleges.json", "r"))
    j[timestamp] = colleges
    json.dump(j, open("./colleges.json", "w+"), indent=4, ensure_ascii=True)
    print("dumped JSON data to ./colleges.json")


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
            colleges = get_by_rank(data, rank_)
            print(f"".join([x['name'] for x in colleges]))
        elif choice == "9":
            dump_data(data)
            print("")
        else:
            break
        print("\n")
