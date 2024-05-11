import discord
from discord.ext import commands, tasks
import generate_wargame_count_data
import generate_user_index_data
import discordbot_data
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


korea_timezone = ZoneInfo('Asia/Seoul')    
begin_datetime = datetime(discordbot_data.begin_datetime[0],
                            discordbot_data.begin_datetime[1],
                            discordbot_data.begin_datetime[2],
                            discordbot_data.begin_datetime[3],
                            discordbot_data.begin_datetime[4],
                            tzinfo=korea_timezone)
end_datetime = datetime(discordbot_data.end_datetime[0],
                            discordbot_data.end_datetime[1],
                            discordbot_data.end_datetime[2],
                            discordbot_data.end_datetime[3],
                            discordbot_data.end_datetime[4],
                            tzinfo=korea_timezone)

def get_score_from_wargame_count_data(wargame_count:list[int]) -> int:
    score = 0
    for i in range(len(wargame_count)):
        score += 2**(i+1)*wargame_count[i]
    return score


async def time_scheduler():
    await bot.wait_until_ready()

    current_time = datetime.now(korea_timezone)
    if current_time < begin_datetime:
        sleep_seconds = (begin_datetime - current_time).total_seconds()
        print("waiting for competition to begin... remaining time:", sleep_seconds)
        await asyncio.sleep(sleep_seconds)
        generate_user_index_data.run()
        generate_wargame_count_data.run()
        initialize_competition()
        channel = bot.get_channel(discordbot_data.TARGET_CHANNEL_ID)
        await channel.send("**Competition has begun!**")
        await get_leaderboard()

    current_time = datetime.now(korea_timezone)
    if current_time < end_datetime:
        sleep_seconds = (end_datetime - current_time).total_seconds()
        print("waiting for competition to end... remaining time:", sleep_seconds)
        await asyncio.sleep(sleep_seconds)
        channel = bot.get_channel(discordbot_data.TARGET_CHANNEL_ID)
        await channel.send("**Competition has finished!**")
        data = await get_leaderboard()
        file = open("final_wargame_count_data.json", "w")
        file.write(json.dumps(data, indent=2, ensure_ascii=False))
        file.close()

async def setup():
    asyncio.create_task(time_scheduler())

@bot.event
async def on_ready():
    channel = bot.get_channel(discordbot_data.TARGET_CHANNEL_ID)
    await channel.send(f"I'm ready! \n usage: type '!leaderboard' on this channel\ncompetition starts at: {begin_datetime}")

@bot.event
async def on_message(message):
    if message.channel.id == discordbot_data.TARGET_CHANNEL_ID:
        await bot.process_commands(message)

def get_leaderboard_str_from_sorted_score_dict(sorted_score_dict:dict, wargame_count_dict:dict) -> str:
    message = ""
    message += "```\n"
    message += "Leaderboard\n"
    datetime_str_format = '%Y-%m-%d %H:%M:%S'
    current_time = datetime.now(korea_timezone)
    if current_time <begin_datetime:
        message += "competition starts at: " + begin_datetime.strftime(datetime_str_format) + "\n"
        message += "competition ends at: " + end_datetime.strftime(datetime_str_format) + "\n"
        message += "current time: "+current_time.strftime(datetime_str_format)+ "\n"

    elif current_time < end_datetime:
        message += "competition started at: " + begin_datetime.strftime(datetime_str_format) + "\n"
        message += "competition ends at: " + end_datetime.strftime(datetime_str_format) + "\n"
        message += "current time: "+current_time.strftime(datetime_str_format)+ "\n"
    else:
        message += "competition started at: " + begin_datetime.strftime(datetime_str_format) + "\n"
        message += "competition ended at: " + end_datetime.strftime(datetime_str_format) + "\n"
        message += "The competition has finished!\n"
    message += "\n"
    rank = 0
    last_score = -1
    tie_count = 1
    for username, score in sorted_score_dict.items():
        if score != last_score:
            rank += tie_count
            tie_count = 1
            last_score = score
        else:
            tie_count += 1
        message += f"{rank}. {username}: {score} \n"
        wargame_count_list = wargame_count_dict[user_index_dict[username]]
        initial_wargame_count_list = initial_wargame_count_dict[username]
        solved_any = False
        for i in range(10):
            if(wargame_count_list[i] - initial_wargame_count_list[i]!=0):
                if not solved_any:
                    solved_any = True
                    message += "   ∟ "
                else:
                    message +=", "
                message += f"Lv{i+1}: {wargame_count_list[i] - initial_wargame_count_list[i]}"
        if solved_any:
            message += "\n"
    message+="```"
    return message

@bot.command("leaderboard")
async def leaderboard(ctx):
    await get_leaderboard()

async def get_leaderboard():
    wargame_count = generate_wargame_count_data.get_score_list_by_user_index_list(user_index_list)
    score_list = list(map(get_score_from_wargame_count_data, wargame_count))
    score_dict = {}
    for i in range(len(username_list)):
        score_dict[username_list[i]] = score_list[i]  - initial_score_dict[username_list[i]]
    
    sorted_score_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
    print(sorted_score_dict)
    wargame_count_dict = {}
    for i in range(len(user_index_list)):
        wargame_count_dict[user_index_list[i]] = wargame_count[i]
    message = get_leaderboard_str_from_sorted_score_dict(sorted_score_dict, wargame_count_dict)

    channel = bot.get_channel(discordbot_data.TARGET_CHANNEL_ID)
    await channel.send(message)
    return wargame_count


def initialize_competition():
    global username_list
    global user_index_list
    global user_index_dict
    global initial_score_dict
    global initial_wargame_count_dict
    # get user index list
    user_index_json_file = open("user_index.json", 'r')
    user_index_dict = json.load(user_index_json_file)
    user_index_json_file.close()
    username_list = list(user_index_dict.keys())
    user_index_list = list(user_index_dict.values())
    
    # get initial score
    initial_wargame_count_file = open("initial_wargame_count_data.json", 'r')
    initial_wargame_count_dict = json.load(initial_wargame_count_file)
    initial_wargame_count_file.close()
    initial_score_dict = {}
    for username, score_list in initial_wargame_count_dict.items():
        initial_score_dict[username] = get_score_from_wargame_count_data(score_list)


if __name__ == "__main__":
    initialize_competition()

    bot.setup_hook = setup
    bot.run(discordbot_data.DISCORD_TOKEN)