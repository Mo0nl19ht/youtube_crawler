from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from pytube import YouTube
from xml.etree import ElementTree
from tqdm import tqdm
import pandas as pd
import os


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

global key_cnt
key_cnt = 0


key_list = [
    'AIzaSyDvYlauzOBv1UPrFDy7LsjNXrsA96ikoiY',
    'AIzaSyAA770s7eAbHt2FInVXW4q5bLBXK9fkDe4'
]
key_len = len(key_list)

# 한국어 or 영어 자막 선택


def get_by_language(yt, language, spot, id):
    #caption = yt.captions.get_by_language_code(language)
    caption = yt.captions[language]

    if caption != None:

        xml = caption.xml_captions

        root_element = ElementTree.fromstring(xml)
        captions = []
        iter_element = root_element.iter(
            tag="p")

        for i, element in enumerate(iter_element):
            caption = {}
            caption['time'] = i
            caption['contents'] = element.text  # 자막 내용 저장
            captions.append(caption)

        out_df = pd.DataFrame(captions, columns=['time', 'contents'])
        out_df.to_csv(f"./captions/{language}/{spot}/caption_{id}.csv",
                      index=False, encoding="utf-8-sig")

# 유튜브 영상 리스트 반환
# 다음 페이지 가져오는거는 nextPageToken할당해줘야함


def get_search_list(youtube, query, nextPageToken=None):
    return youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults="50",  # options.max_results,
        # regionCode="KR" 안해도되려나
        topicId="/m/019_rr, /m/07bxq, /m/03glg",  # lifestyle, tourism, hobby
        type="video",
        videoCaption="closedCaption",  # 캡션 있는 동영상만
        pageToken=nextPageToken
    ).execute()

# 할당량이 끝난 키를 바꿔준다


def change_key():
    global key_index
    global key_cnt

    key_index += 1
    key_index %= key_len
    key_cnt += 1

    if key_cnt >= key_len:  # key 한바퀴 다 돌았을 때 프로그램 종료
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("주어진 키 모두사용")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return 0

    print(f"{key_index} 으로 키 바꿈")
    print(f"key_cnt == {key_cnt}")

    return 1


def youtube_search(spot):

    global key_index
    global key_cnt

    query = spot + "브이로그"

    print(f"{spot}지역 검색 시작")
    try:
        print(f"사용중인 키 : {key_list[key_index]}")
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=key_list[key_index])
        # Call the search.list method to retrieve results matching the specified
        # query term.
        print("검색중...")
        search_response = get_search_list(youtube, query)
    except:
        if change_key() == 0:
            return 0

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=key_list[key_index])

        print("다시 검색중...")
        search_response = get_search_list(youtube, query)

    videos = []

    while search_response:

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":  # 필요없을수도?
                videos.append(
                    (search_result["id"]["videoId"], search_result["snippet"]["title"]))

        try:
            if 'nextPageToken' in search_response:
                search_response = get_search_list(
                    youtube, query, search_response['nextPageToken'])
            else:
                break
        except:
            if change_key() == 0:
                return 0

            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=key_list[key_index])
            # 다음 키를 가져와서 다시 실행
            if 'nextPageToken' in search_response:
                search_response = get_search_list(
                    youtube, query, search_response['nextPageToken'])
            # 새로운 키니까 50개 할당
            else:
                break

    folder_spot = './captions/'+'videoIds'
    os.makedirs(folder_spot, exist_ok=True)

    df = pd.DataFrame(videos, columns=['id', 'title'])
    df.to_csv(f"{folder_spot}/{spot}_videoIds.csv",  # "지역 여행 브이로그" 라고 검색
              index=False, encoding="utf-8-sig")

    li = []
    for index, title in enumerate(df['title']):
        if not (('여행' in title and spot in title) or ('브이로그' in title and spot in title) or ('vlog' in title and spot in title) or ('travel' in title and spot in title)):
            li.append(index)

    df = df.drop(li)

    df = df.drop_duplicates()  # 혹시 모를 중복 제거
    cnt_videos = len(df)
    df.to_csv(f"{folder_spot}/{spot}여행_videoIds.csv", index=False,
              encoding="utf-8-sig")  # 위 Ids를 제목으로 필터링 후
    print(f"{spot}지역 관련 영상 갯수 : {cnt_videos}\n")
    return df


def make_captions(spot, df):

    print()
    print(f"{spot} 지역 자막 생성중")
    print()

    url = "https://youtube.com/watch?v="

    cnt_ko = 0
    cnt_en = 0

    for id in tqdm(df['id']):

        yt = YouTube(url+id)

        # 한글 자막 확인
        try:
            language = "ko"
            get_by_language(yt, language, spot, id)
            cnt_ko += 1
        except:
            pass
        # 영어 자막 확인
        try:
            language = "en"
            get_by_language(yt, language, spot, id)
            cnt_en += 1
        except:
            pass

    print(f"{spot}지역 한글자막 : {cnt_ko}개 영어자막 : {cnt_en}개\n")


if __name__ == "__main__":
    spot_list = ((input('지역을 입력해주세요: ')).split())
    global key_index
    key_index = int(input("사용할 키의 인덱스 적어 : "))
    #language = input('언어를 입력해주세요(ko or en):')

    #argparser.add_argument("--q", help="Search spot", default=spot)
    #args = argparser.parse_args()

    # print(args)
    try:
        for spot in spot_list:
            folder_en = './captions/'+'en'+'/'+spot
            folder_ko = './captions/'+'ko'+'/'+spot
            os.makedirs(folder_en, exist_ok=True)
            os.makedirs(folder_ko, exist_ok=True)
            videos = youtube_search(spot)
            make_captions(spot, videos)
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
