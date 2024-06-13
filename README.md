# CTF-leaderboard-from-dreamhack
드림핵 유저 정보에서 볼 수 있는 워게임 풀이 개수를 통해 순위표를 생성할 수 있는 도구입니다.

소소하게 내부 CTF를 열거나, 서로 공부하면서 경쟁심을 느끼기 위해 만들었습니다.

스코어는 1레벨 문제는 2점, 2레벨 문제는 4점,..., n레벨 문제는 2^n점, 10레벨 문제는 1024점이에요.

한번 이 배점 시스템으로 경쟁해보니까 재밌더라구요. 더 어려운 문제를 도전해볼만한 동기부여도 마구 생기구요.

## Set Up
우선 아래의 내용을 담은 discordbot.py를 생성해야 합니다.
```
DISCORD_TOKEN = <discord_token:str>
TARGET_CHANNEL_ID = <channer_id:int>
begin_datetime = (2024, 5, 11, 7, 6)
end_datetime = (2024, 5, 11, 7, 10)
```
그리고 아래처럼 username_list.txt를 만들어줍니다.

순위를 매길 유저들의 닉네임을 담은 텍스트 파일입니다.

아래는 eumppe와 준화준화의 닉네임을 담은 얘시이며 원하는 닉네임으로 채우시면 됩니다.

닉네임간 구분은 줄바꿈으로 합니다.
```
eumppe
준화준화
```
username_list.txt에 적힌 닉네임을 바탕으로 유저의 인덱스를 추출해야 하므로 다음 명령어를 실행합니다.

결과물은 user_index.json에 저장됩니다.
```
python generate_user_index_data.py
```
현재 시점에 사용자별로 난이도별 문제를 얼마나 풀었는지 저장하고 싶다면 아래 명령어를 실행합니다.

결과물은 initial_wargame_count_data.json에 저장됩니다.
```
python generate_wargame_count_data.py
```
아래 명령어를 통해 디스코드봇을 실행하면 됩니다.

discordbot.py에 저장한 begin_datetime이 아직 지나지 않은 시점에 디스코드봇을 실행한다면, begin_datetime에 또한번 generate_wargame_count_data.py를 다시 실행합니다.
```
python discordbot.py
```

## Usage
디스코드봇의 타겟 채널에서 !leaderboard 명령어를 입력하면 리더보드를 출력합니다.
