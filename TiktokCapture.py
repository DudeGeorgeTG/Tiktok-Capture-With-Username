import datetime
import json
import pycountry
import requests
import re


def extract(pattern, text, default=None, yesno=False):
    match = re.search(pattern, text)
    if match:
        value = match.group(1)
        if yesno:
            return value.lower() == "true"
        return value
    return default if not yesno else False


def TikTok_Info(username):
    try:
        headers = {
            "Host": "www.tiktok.com",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Plume L2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9"
        }

        response = requests.get(f'https://www.tiktok.com/@{username}', headers=headers)
        tikinfo = response.text

        try:
            getting = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]

            user_info = {
                "user_id": extract(r'"id":"(.*?)"', getting, ""),
                "nickname": extract(r'"nickname":"(.*?)"', getting, ""),
                "signature": extract(r'"signature":"(.*?)"', getting, ""),
                "region": extract(r'"region":"(.*?)"', getting, ""),
                "following": extract(r'"followingCount":(\d+)', getting, "0"),
                "followers": extract(r'"followerCount":(\d+)', getting, "0"),
                "likes": extract(r'"heart":(\d+)', getting, "0"),
                "videos": extract(r'"videoCount":(\d+)', getting, "0"),
                "friends": extract(r'"friendCount":(\d+)', getting, "0"),
                "private": extract(r'"privateAccount":(true|false)', getting, yesno=True),
                "verified": extract(r'"verified":(true|false)', getting, yesno=True),
                "seller": extract(r'"commerceInfo":{"seller":(true|false)', getting, yesno=True),
                "language": extract(r'"language":"(.*?)"', getting, ""),
                "created": extract(r'"createTime":(\d+)', getting, "0"),
                "secuid": extract(r'"secUid":"(.*?)"', getting, "")
            }

            try:
                country_obj = pycountry.countries.get(alpha_2=user_info["region"])
                country_name = country_obj.name
                country_flag = country_obj.flag
            except:
                country_name = user_info["region"]
                country_flag = ""

            binary = "{0:b}".format(int(user_info["user_id"])) if user_info["user_id"].isdigit() else ""
            timestamp = int(binary[:31], 2) if len(binary) >= 31 else 0
            try:
                created_date = datetime.datetime.fromtimestamp(timestamp)
            except:
                created_date = ""

            return {
                "username": username,
                "secuid": user_info["secuid"],
                "name": user_info["nickname"],
                "followers": int(user_info["followers"]),
                "following": int(user_info["following"]),
                "likes": int(user_info["likes"]),
                "videos": int(user_info["videos"]),
                "private": user_info["private"],
                "country": country_name,
                "flag": country_flag,
                "date_created": created_date.strftime("%Y-%m-%d %H:%M:%S") if created_date else None,
                "user_id": user_info["user_id"],
                "bio": user_info["signature"] or "",
                "verified": user_info["verified"],
                "tiktok_shop": user_info["seller"],
                "language": user_info["language"]
            }

        except Exception as inner_exception:
            return {"error": "Invalid username or data format", "details": str(inner_exception)}

    except Exception as e:
        return {"status": "bad", "error": str(e)}

result = TikTok_Info("asd")
print(json.dumps(result, indent=4, ensure_ascii=False))
