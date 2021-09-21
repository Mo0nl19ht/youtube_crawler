from apiclient.discovery import build


class Crawler:
    def __init__(self, key_list, key_index=0):
        self.service_name = "youtube"
        self.api_version = "v3"
        self.key_list = key_list
        self.key_len = len(self.key_list)
        self.key_index = key_index
        self.key_cnt = 0
        self.youtube = build(self.service_name, self.api_version,
                             developerKey=self.key_list[self.key_index])

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

    def get_search_list(self, query, topicId=None, videoCaption=any, maxResult=50, regionCode="KR", nextPageToken=None):

        return self.youtube.search().list(
            q=query,
            part="id,snippet",

            topicId=topicId,  # "/m/019_rr, /m/07bxq, /m/03glg",  # lifestyle, tourism, hobby
            type="video",
            videoCaption=videoCaption,  # 캡션 있는 동영상만
            maxResults=maxResult,  # max == 50
            regionCode=regionCode,
            pageToken=nextPageToken
        ).execute()

    def youtube_search(self, query, topicId=None, videoCaption=any, maxResult=50, regionCode="KR"):
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

        any – 캡션 사용 여부에 따라 결과를 필터링하지 않습니다.
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
            # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            #                 developerKey=key_list[key_index])

            print("검색중...")
            search_response = self.get_search_list(
                self.youtube, query, topicId, videoCaption, maxResult, regionCode)
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
