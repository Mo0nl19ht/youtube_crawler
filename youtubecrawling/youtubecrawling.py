from unicodedata import name
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from pytube import YouTube
from xml.etree import ElementTree
from tqdm import tqdm
import pandas as pd
import os
import html
from datetime import datetime


class Crawler:

    def __init__(self, path, key_list, key_index=0):
        """
        경로, apikey_list, 사용할 키의 index
        """
        self.service_name = "youtube"
        self.api_version = "v3"
        # 저장할 곳의 경로
        self.path = path
        self.key_list = key_list
        self.key_len = len(self.key_list)
        self.key_index = key_index
        self.key_cnt = 0
        self.youtube = self.get_youtube(self.key_list[self.key_index])

    def get_youtube(self, key):
        return build(self.service_name, self.api_version,
                     developerKey=key)

    def change_key(self):

        self.key_index += 1
        self.key_index %= self.key_len

        self.key_cnt += 1

        if self.key_cnt >= self.key_len:  # key 한바퀴 다 돌았을 때 프로그램 종료
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("주어진 키를 모두 사용 했습니다")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            return 0

        print(f"{self.key_index} 으로 키를 교체합니다.")
        print(f"키를 {self.key_cnt}번 바꿨습니다.")

        return 1

    def get_search_list(self, query, topicId=None, videoCaption=None, regionCode="KR", nextPageToken=None):

        return self.youtube.search().list(
            q=query,
            part="id,snippet",
            topicId=topicId,  # "/m/019_rr, /m/07bxq, /m/03glg",  # lifestyle, tourism, hobby
            type="video",
            videoCaption=videoCaption,  # 캡션 있는 동영상만
            maxResults=50,
            regionCode=regionCode,
            pageToken=nextPageToken
        ).execute()

    def youtube_search(self, query, topicId=None, videoCaption=None, regionCode="KR"):
        """
        topicId

        사용예시:

        topicId = "/m/019_rr, /m/07bxq, /m/03glg"

        Music

        - /m/04rlf Music
        - /m/05fw6t Children's music
        - /m/02mscn Christian music
        - /m/0ggq0m Classical music
        - /m/01lyv Country
        - /m/02lkt Electronic music
        - /m/0glt670 Hip hop music
        - /m/05rwpb Independent music
        - /m/03_d0 Jazz
        - /m/028sqc Music of Asia
        - /m/0g293 Music of Latin America
        - /m/064t9 Pop music
        - /m/06cqb Reggae
        - /m/06j6l Rhythm and blues
        - /m/06by7 Rock music
        - /m/0gywn Soul music

        Gaming

        - /m/0bzvm2 Gaming
        - /m/025zzc Action game
        - /m/02ntfj Action-adventure game
        - /m/0b1vjn Casual game
        - /m/02hygl Music video game
        - /m/04q1x3q Puzzle video game
        - /m/01sjng Racing video game
        - /m/0403l3g Role-playing video game
        - /m/021bp2 Simulation video game
        - /m/022dc6 Sports game
        - /m/03hf_rm Strategy video game

        Sports

        - /m/06ntj Sports
        - /m/0jm_ American football
        - /m/018jz Baseball
        - /m/018w8 Basketball
        - /m/01cgz Boxing
        - /m/09xp_ Cricket
        - /m/02vx4 Football
        - /m/037hz Golf
        - /m/03tmr Ice hockey
        - /m/01h7lh Mixed martial arts
        - /m/0410tth Motorsport
        - /m/066wd Professional wrestling
        - /m/07bs0 Tennis
        - /m/07_53 Volleyball

        Entertainment

        - /m/02jjt Entertainment
        - /m/095bb Animated cartoon
        - /m/09kqc Humor
        - /m/02vxn Movies
        - /m/05qjc Performing arts

        Lifestyle

        - /m/019_rr Lifestyle
        - /m/032tl Fashion
        - /m/027x7n Fitness
        - /m/02wbm Food
        - /m/0kt51 Health
        - /m/03glg Hobby
        - /m/068hy Pets
        - /m/041xxh Physical attractiveness [Beauty]
        - /m/07c1v Technology
        - /m/07bxq Tourism
        - /m/07yv9 Vehicles

        ETC

        - /m/01k8wb Knowledge
        - /m/098wr Society




        videoCaption:

        None – 캡션 사용 여부에 따라 결과를 필터링하지 않습니다.
        closedCaption – 캡션이 있는 동영상만 포함합니다.
        none – 캡션이 없는 동영상만 포함합니다.



        regionCode:

        KR - 대한민국
        US - 미국

        https://ko.wikipedia.org/wiki/ISO_3166-1_alpha-2#KR 참조





        참조 :
        https://developers.google.com/youtube/v3/docs/search/list?hl=ko
        """

        print(f"검색어 : {query}")
        print("검색을 시작합니다")
        try:
            print(f"사용중인 키 : {self.key_list[self.key_index]}")
            print("검색중")
            search_response = self.get_search_list(
                query, topicId, videoCaption, regionCode)
        except:
            if self.change_key() == 0:
                return 0

            self.youtube = self.get_youtube(self.key_list[self.key_index])

            print("다시 검색중")
            search_response = self.get_search_list(
                query, topicId, videoCaption, regionCode)

        videos = []

        while search_response:

            for search_result in search_response['items']:
                if search_result["id"]["kind"] == "youtube#video":
                    videos.append(
                        (search_result["id"]["videoId"], search_result["snippet"]["title"]))
            try:
                if 'nextPageToken' in search_response:
                    search_response = self.get_search_list(
                        query, topicId, videoCaption, regionCode, search_response['nextPageToken'])
                else:

                    break
            except:
                if self.change_key() == 0:
                    return 0

                self.youtube = self.get_youtube(self.key_list[self.key_index])
                # 다음 키를 가져와서 다시 실행
                if 'nextPageToken' in search_response:
                    search_response = self.get_search_list(
                        query, topicId, videoCaption, regionCode, search_response['nextPageToken'])
                else:
                    break

        folder_ids = f'{self.path}/videoIds'
        os.makedirs(folder_ids, exist_ok=True)
        df = pd.DataFrame(videos, columns=['id', 'title'])
        df = df.drop_duplicates()  # 혹시 모를 중복 제거

        cnt_videos = len(df)

        df.index = range(cnt_videos)

        for i, v in enumerate(df['title']):
            df.loc[i, 'title'] = (html.unescape(v))

        # 직접 csv까지 만들어주기엔 폴더명 등 제약사항있음

        now = datetime.now()
        mic = now.microsecond//10000
        n = f"{now.month}{now.day}_{now.hour}_{now.minute}_{mic}"
        df.to_csv(f"{folder_ids}/{n}_videoIds.csv",
                  index=False, encoding="utf-8-sig")

        print(f"검색어 : {query} 영상 갯수 : {cnt_videos}")

        return df

    def get_by_language(self, yt, language, id, folder):
        caption = yt.captions[language]

        if caption != None:

            xml = caption.xml_captions

            root = ElementTree.fromstring(xml)
            captions = []
            iter_element = root.iter(
                tag="p")

            for i, element in enumerate(iter_element):
                caption = {}
                caption['index'] = i
                caption['contents'] = html.unescape(element.text)  # 자막 내용 저장
                captions.append(caption)

            out_df = pd.DataFrame(captions, columns=['index', 'contents'])

            out_df.to_csv(f"{folder}/caption_{id}.csv",
                          index=False, encoding="utf-8-sig")

    def make_captions(self, df, is_En=False):
        """
        자막을 만들어 폴더에 저장합니다

        자막이 없는 id들을 반환합니다

        """

        print()
        print(f"자막을 가져옵니다")
        print()

        url = "https://youtube.com/watch?v="

        ko_no = []
        en_no = []

        cnt_ko = 0
        cnt_en = 0

        cnt_ko_no = 0
        cnt_en_no = 0
        folder_en = f'{self.path}/captions/'+'en'
        folder_ko = f'{self.path}/captions/'+'ko'
        os.makedirs(folder_en, exist_ok=True)
        os.makedirs(folder_ko, exist_ok=True)

        now = datetime.now()
        micro = now.microsecond//10000
        na = f"{now.month}{now.day}_{now.hour}_{now.minute}_{micro}"

        folder_ko = folder_ko+"/"+na

        os.makedirs(folder_ko, exist_ok=True)
        if is_En:
            folder_en = folder_en+"/"+na
            os.makedirs(folder_en, exist_ok=True)

        for id in tqdm(df['id']):
            try:
                yt = YouTube(url+id)
            except:
                print(f"id : {id} 이 영상은 외부 접근이 불가합니다")
            # 한글 자막 확인
            try:
                language = "ko"
                self.get_by_language(yt, language, id, folder_ko)
                cnt_ko += 1
            except:
                cnt_ko_no += 1
                ko_no.append(id)
                pass
            # 영어 자막
            if is_En:
                try:
                    language = "en"
                    self.get_by_language(yt, language, id, folder_en)
                    cnt_en += 1
                except:
                    cnt_en_no += 1
                    en_no.append(id)
                    pass

        print(f"한글자막 : {cnt_ko}개 , 영어자막 : {cnt_en}개\n")
        print(f"한글자막 없음: {cnt_ko_no}개 , 영어자막 없음 : {cnt_en_no}개")

        if is_En:
            return ko_no, en_no
        else:
            return ko_no

    def get_search_list_desc(self, id):
        return self.youtube.videos().list(
            part='snippet',
            id=id
        ).execute()

    def get_descriptions(self, df):
        """
        영상의 상세정보를 받아와서
        csv파일을 만들고
        DataFrame을 반환합니다
        """
        print("영상의 상세정보를 가져옵니다")
        videos = []

        for index in tqdm(df.index):
            id = df.loc[index, 'id']
            title = df.loc[index, 'title']

            try:
                search_response = self.get_search_list_desc(id)
            except:
                if self.change_key() == 0:
                    return 0
                self.youtube = self.get_youtube(self.key_list[self.key_index])

                print("키 변경\n다시 검색중...\n")
                search_response = self.get_search_list_desc(id)

            try:
                search_result = search_response['items'][0]
            # 영상이 접근 불가 처리된 경우
            except:
                print(f"id : {id} 영상 접근 불가(비공개 or 삭제))")
                pass

            videos.append((id, title, search_result["snippet"]["description"]))

        df = pd.DataFrame(videos, columns=['id', 'title', 'desc'])
        df = df.drop_duplicates()  # 혹시 모를 중복 제거

        now = datetime.now()
        mic = now.microsecond//10000
        n = f"{now.month}{now.day}_{now.hour}_{now.minute}_{mic}"
        path = f"{self.path}/description"
        os.makedirs(path, exist_ok=True)
        df.to_csv(f"{path}/{n}_title_desc.csv",
                  index=False, encoding="utf-8-sig")

        return df

    def get_search_list_comment(self, id, pageToken=None):
        return self.youtube.commentThreads().list(
            part='snippet',
            videoId=id,
            pageToken=pageToken,
            maxResults=100
        ).execute()

    def get_comments(self, df):
        """
        영상의 댓글을 가져와서 저장합니다.
        댓글을 가져오는데 실패한 영상의 id들을 반환합니다

        """
        path = f"{self.path}/comments"
        os.makedirs(path, exist_ok=True)
        cnt = 0
        no = []
        print("댓글 정보를 가져옵니다")

        for index in tqdm(df.iterrows()):
            id = index[1]['id']
            try:
                search_response = self.get_search_list_comment(id)
            except:
                if self.change_key() == 0:
                    return 0
                self.youtube = self.get_youtube(self.key_list[self.key_index])

                print("키 변경\n다시 검색중...\n")
                search_response = self.get_search_list_comment(id)

            comments = []

            while search_response:

                for search_result in search_response['items']:
                    comment = search_result['snippet']['topLevelComment']['snippet']
                    comments.append([html.unescape(comment['authorDisplayName']), html.unescape(
                        comment['textDisplay']), comment['likeCount']])
                try:
                    if 'nextPageToken' in search_response:
                        search_response = self.get_search_list_comment(
                            id, search_response['nextPageToken'])
                    else:
                        break
                except:
                    if self.change_key() == 0:
                        return 0
                    self.youtube = self.get_youtube(
                        self.key_list[self.key_index])
                    # 다음 키를 가져와서 다시 실행
                    if 'nextPageToken' in search_response:
                        search_response = self.get_search_list_comment(
                            id, search_response['nextPageToken'])
                    else:
                        break
            try:
                df = pd.DataFrame(comments)
                df.columns = ['author', 'comment', 'like']
                df.to_csv(f"{path}/{id}_comments.csv",
                          index=False, encoding="utf-8-sig")
            except:
                cnt += 1
                no.append(id)
                pass

        print(f"{len(df)}중의 {cnt}개의 영상의 댓글을 불러오는데 실패하였습니다")

        return no
