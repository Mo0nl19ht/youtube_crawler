from warnings import catch_warnings
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from pytube import YouTube
from xml.etree import ElementTree
from tqdm import tqdm
import pandas as pd
import os
import pprint

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

global key_cnt
key_cnt = 0


key_list = [

]
key_len = len(key_list)

# 한국어 or 영어 자막 선택


# 유튜브 영상 리스트 반환
# 다음 페이지 가져오는거는 nextPageToken할당해줘야함


def get_search_list(youtube, id):
    return youtube.videos().list(
        part='snippet',
        id=id
    ).execute()


# 할당량이 끝난 키를 바꿔준다


def change_key():
    global key_index
    global key_cnt

    key_index += 1
    key_index %= key_len
    key_cnt += 1

    if key_cnt >= key_len:  # key 한바퀴 다 돌았을 때 프로그램 종료

        print("\n주어진 키 모두사용\n")

        return 0

    print(f"{key_index} 으로 키 바꿈")
    print(f"key_cnt == {key_cnt}")

    return 1

# 영상 찾기를 시작함


def youtube_search(spot, df):

    global key_index
    global key_cnt

    query = spot + "브이로그"

    videos = []

    for index in tqdm(df.index):
        id = df.loc[index, 'id']
        title = df.loc[index, 'title']

        try:

            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=key_list[key_index])
            search_response = get_search_list(youtube, id)
        except:
            if change_key() == 0:
                return 0
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=key_list[key_index])

            print("키 변경\n다시 검색중...\n")
            search_response = get_search_list(youtube, id)

        try:
            search_result = search_response.get(
                "items", [])[0]  # 영상이 접근 불가 처리된 경우
        except:
            print(f"{id}")
            print("영상 접근 불가(비공개 or 삭제))")
            pass

        videos.append((id, title, search_result["snippet"]["description"]))

    df = pd.DataFrame(videos, columns=['id', 'title', 'desc'])
    df = df.drop_duplicates()  # 혹시 모를 중복 제거
    df.to_csv(f"description/{spot}_title_desc.csv",  # "지역 여행 브이로그" 라고 검색
              index=False, encoding="utf-8-sig")

    cnt_videos = len(df)
    print(f"{spot}지역 관련 영상 갯수 : {cnt_videos}\n")


if __name__ == "__main__":
    spot_list = ((input('지역을 입력해주세요: ')).split())
    global key_index
    key_index = int(input("사용할 키의 인덱스 적어 : "))
    # language = input('언어를 입력해주세요(ko or en):')

    # argparser.add_argument("--q", help="Search spot", default=spot)
    # args = argparser.parse_args()

    # print(args)
    try:
        for spot in spot_list:
            folder_desc = './description'

            os.makedirs(folder_desc, exist_ok=True)
            df = pd.read_csv(f"videoIds/{spot}여행_videoIds.csv")
            youtube_search(spot, df)
            print(f"{spot} 완료\n")

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" %
              (e.resp.status, e.content))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print()
        print(f"입력한 {spot_list} 중에서 {spot}을 검색하다가 꺼짐")
        print()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    cnt = key_index % key_len
    print(f"마지막으로 사용한 key_index == {cnt}")
    print(key_list[cnt])
    print(f"사용한 키 갯수 == {key_cnt}")
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
