# **youtube_crawler**

유튜브 API를 이용하여 <b>매우 쉽게! 여러 텍스트 정보를 크롤링하고 저장합니다</b>

정식 api를 이용하여 크롤링하기에 안정성이 높습니다

할당량을 모두 사용하면 크롤링이 되지 않기에 api키를 여러개 가지고 있으면 좋습니다

구글 계정당 1개씩 발급 가능하니 구글 계정이 많다면 여러개의 키를 사용 가능합니다

발급 방법

https://velog.io/@yhe228/Youtube-API%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%B4-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0

처음에 API key리스트를 입력받아 자동으로 <b>할당량이 끝나면 다른 키로 바꿔줍니다.</b>

크롤링 항목

-   영상 id (URL)
-   제목
-   상세정보
-   댓글
-   자막 - pytube 라이브러리 사용

### 아래 코드로 모든 크롤링이 끝납니다

```jsx
from youtube_crawler import Crawler

key_list=[ "asdasd", "bddfg", "hgfd"]

# 크롤러 호출
c = Crawler("D:/youtube_crawler", key_list)

# 블랙핑크로 유튜브 검색 , id, 제목 크롤링
df = c.youtube_search("블랙핑크")

# 블랙핑크 영상 자막 크롤링
cap_no = c.make_captions(df)

# 영상 댓글 크롤링
com_no = c.get_comments(df)

# 상세정보 크롤링
desc = c.get_descriptions(df)
```
## 폴더 구조

--지정한 폴더

     :--videoIds
  
     :--captions
     
     :--comments
  
     :--description

## 개발 동기

유튜브 크롤링을 하는데 공식 문서를 참조하여 코드를 짜고

내가 원하는 형태로 만들고 API의 할당량이 끝나면 손수 바꿔줘야 하고

어디부터 끊겼는지 찾기 귀찮아서 라이브러리를 직접 개발하였습니다.

검색부터 csv파일로의 저장까지 한번에 해주기 때문에 사용자는 별다른 설정이 필요 없는것이 장점입니다.

많이 사용해주시고 문제점은 Issue를 통해 말씀해주시면 조치하겠습니다

감사합니다


## 사용 라이브러리

라이브러리 설치 시 자동으로 설치 됩니다

-   google-api-python-client
-   oauth2client
-   pytube
-   tqdm
-   pandas

# 기능 상세 설명

## Crawler

```python
yc = Crawler(path , key_list, key_index=0)

#예시

key_list=[ "asdasd", "bddfg", "hgfd"]
# "D:/youtube_crawler"에 파일들 저장
# api는 key_list로 사용
# 2번째 인덱스에 해당되는 키부터 사용
yc = Crawler("D:/youtube_crawler", key_list, 2)
```

Crawler 를 불러옵니다

### parameter

-   path
    -   정보를 저장할 위치
-   key_list
    -   사용할 API key list
-   key_index
    -   처음 사용할 key의 index

## yotube_search

```python
df = yc.youtube_search(query, topicId=None, videoCaption=None, regionCode="KR")

#예시

# 대한민국 영상 중 nlp 강의를 검색해서 가져오는데
# topic정하지 않고 자막여부 상관없이 가져온다
df = yc.youtbue_search("nlp 강의")

# 대한민국 영상 중 블랙핑크를 검색해서 가져오는데
# Music 과 Entertainment에 관련된 영상을 가져옴
df = yc.youtube_search("블랙핑크",topicId="/m/04rlf, /m/02jjt")
```

query로 검색하고 관련 영상의 id들을 저장하고 DataFrame을 반환합니다

### parameter

-   query
    -   검색어
-   topicId

    -   주제 선택 - 여러개 가능
    -   topicId

        **Music topics**

        -   /m/04rlf Music
        -   /m/05fw6t Children's music
        -   /m/02mscn Christian music
        -   /m/0ggq0m Classical music
        -   /m/01lyv Country
        -   /m/02lkt Electronic music
        -   /m/0glt670 Hip hop music
        -   /m/05rwpb Independent music
        -   /m/03_d0 Jazz
        -   /m/028sqc Music of Asia
        -   /m/0g293 Music of Latin America
        -   /m/064t9 Pop music
        -   /m/06cqb Reggae
        -   /m/06j6l Rhythm and blues
        -   /m/06by7 Rock music
        -   /m/0gywn Soul music

        **Gaming topics**

        -   /m/0bzvm2 Gaming
        -   /m/025zzc Action game
        -   /m/02ntfj Action-adventure game
        -   /m/0b1vjn Casual game
        -   /m/02hygl Music video game
        -   /m/04q1x3q Puzzle video game
        -   /m/01sjng Racing video game
        -   /m/0403l3g Role-playing video game
        -   /m/021bp2 Simulation video game
        -   /m/022dc6 Sports game
        -   /m/03hf_rm Strategy video game

        **Sports topics**

        -   /m/06ntj Sports
        -   /m/0jm\_ American football
        -   /m/018jz Baseball
        -   /m/018w8 Basketball
        -   /m/01cgz Boxing
        -   /m/09xp\_ Cricket
        -   /m/02vx4 Football
        -   /m/037hz Golf
        -   /m/03tmr Ice hockey
        -   /m/01h7lh Mixed martial arts
        -   /m/0410tth Motorsport
        -   /m/066wd Professional wrestling
        -   /m/07bs0 Tennis
        -   /m/07_53 Volleyball

        **Entertainment topics**

        -   /m/02jjt Entertainment
        -   /m/095bb Animated cartoon
        -   /m/09kqc Humor
        -   /m/02vxn Movies
        -   /m/05qjc Performing arts

        **Lifestyle topics**

        -   /m/019_rr Lifestyle
        -   /m/032tl Fashion
        -   /m/027x7n Fitness
        -   /m/02wbm Food
        -   /m/0kt51 Health
        -   /m/03glg Hobby
        -   /m/068hy Pets
        -   /m/041xxh Physical attractiveness [Beauty]
        -   /m/07c1v Technology
        -   /m/07bxq Tourism
        -   /m/07yv9 Vehicles

        **Other topics**

        -   /m/01k8wb Knowledge
        -   /m/098wr Society

-   videoCaption
    -   None – 캡션 사용 여부에 따라 결과를 필터링하지 않습니다.
    -   closedCaption – 캡션이 있는 동영상만 포함합니다.
    -   none – 캡션이 없는 동영상만 포함합니다.
-   regionCode
    -   KR - 한국
    -   US - 미국
    -   [https://ko.wikipedia.org/wiki/ISO_3166-1_alpha-2#KR](https://ko.wikipedia.org/wiki/ISO_3166-1_alpha-2#KR) 참조

### return

-   지정한 경로 내 videoIds폴더에 저장
    -   파일이름 : 실행한 시간\_videoIds.csv
-   pandas.DataFrame 반환


## make_caption

```python
cap_no = c.make_captions(df)

#영어 자막도 가져오기
cap_no = c.make_captions(df,True)
```

해당 영상들의 자막을 가져온다

### parameter

-   df
    -   youtube_search를 통해 반환된 DataFrame
    -   columns= [ ' id', 'title']
-   if_En
    -   영어 자막 가져올지 말지

### return

-   지정한 경로 내 catptions폴더에 저장
-   자막이 없는 영상 id 리스트 반환
-   columns=['index', 'contents']

## get_comments

```java
com_no = c.get_comments(df)
```

해당 영상들의 댓글들과 좋아요 수(댓글)를 가져옵니다

### parameter

-   df
    -   youtube_search를 통해 반환된 DataFrame
    -   columns = ['id' ,'title]

### return

-   지정한 경로 내 comments폴더에 저장
-   columns = ['author','comment','like']

## get_descriptions

```java
desc = c.get_descriptions(df)
```

해당 영상들의 상세정보를 가져옵니다.

### parameter

-   df
    -   youtube_search를 통해 반환된 DataFrame
    -   columns = ['id' ,'title]

### return

-   지정한 경로 내 description폴더에 저장
-   columns=['id', 'title', 'desc']


### Disclaimer
사용자가 해당 프로그램을 사용함으로서 생기는 불이익 또는 책임에 개발자는 책임을 지지 않습니다.
