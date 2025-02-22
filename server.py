import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  
CHANNEL_ID = str(os.getenv("CHANNEL_ID")) 
GITHUB_TOKEN = str(os.getenv("GITHUB_TOKEN"))

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}
teams = {
    "Golden Bytes": {"repo_url": "https://github.com/M-a-a-d-man/Golden_bytes", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340458507060776970/goldenbyte.jpg?ex=67b26ec4&is=67b11d44&hm=f9e72bc9df4b9c2f96742f61b4f27f518dbce7b8f180c629bd0c824e34bf5e70&"},
    "Amicae": {"repo_url": "https://github.com/phmarcel0x/amicae", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340459095328559156/amicae.png?ex=67b26f50&is=67b11dd0&hm=11bae23fcca846b107968f2c9b1888d786a09284e96e3f63235611ad66c0e92d&"},
    "team m8te": {"repo_url": "https://github.com/daliabtnj/teamUp", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340458795742003200/user_icon.png?ex=67b26f09&is=67b11d89&hm=7c700551416e1f1055650c99b1b7f44f012b14a9d186e11b2bda72d4f7470416&"},
    "InnovateIQ": {"repo_url": "https://github.com/kvvyas/Smart-Space", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340458795742003200/user_icon.png?ex=67b26f09&is=67b11d89&hm=7c700551416e1f1055650c99b1b7f44f012b14a9d186e11b2bda72d4f7470416&"},
    "Code Syndicate ": {"repo_url": "https://github.com/Apoorva231/team10-frontend", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340458795742003200/user_icon.png?ex=67b26f09&is=67b11d89&hm=7c700551416e1f1055650c99b1b7f44f012b14a9d186e11b2bda72d4f7470416&"},
    "405 found":  {"repo_url": "None", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340458795742003200/user_icon.png?ex=67b26f09&is=67b11d89&hm=7c700551416e1f1055650c99b1b7f44f012b14a9d186e11b2bda72d4f7470416&"},
    "SageMode": {"repo_url": "None", "image_url": "https://cdn.discordapp.com/attachments/1155595152753176616/1340459238551588977/sagemode.png?ex=67b26f72&is=67b11df2&hm=6b2b2c8eb5fc82ff050227be5faeccfd123ef91cfe865196504e5f69b66a2219&"},
}

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():

    # Get the guild object using guild_id
    guild = client.get_guild(int(GUILD_ID))

    if guild is None:
        print("Guild not found!")
        return  # Exit if the guild is not found

    print(f"Logged in as {client.user}!")
    channel = client.get_channel(int(CHANNEL_ID))

    # Start the message with the title
    message_content = "**📌 GDSC Project Team Metric Board**\n\n"  # Title added

    for team, data in teams.items():
        repo_url = data["repo_url"]
        image_url = data["image_url"]
        if repo_url == "None" or repo_url == "Unavailable":
            message_content += f"❌ **{team}** repositories are unavailable.\n\n"
            continue

        # Safely extract the repo name
        try:
            repo_name = repo_url.split("/")[-1]
        except IndexError:
            repo_name = "N/A"  # Default value in case of any issue with URL format

        # Fetch repository information for each team
        repo_info = await fetch_repo_info(team, repo_name, repo_url)

        # Create the embed message with the team link
        embed = discord.Embed(title=f"🔹 **{team}**", description=f"[Visit {team}'s Repo]({repo_url})\n\n{repo_info}", color=discord.Color.blue())
        embed.set_thumbnail(url=image_url)  # Add the image under the team name

        # Send the embed
        await channel.send(embed=embed)
    print(f"Code Execution Complete")

async def fetch_repo_info(team, repo_name, repo_url):
    # Fetch repo details
    commits_url = f"https://api.github.com/repos/{repo_url.split('/')[-2]}/{repo_name}/commits"
    pulls_url = f"https://api.github.com/repos/{repo_url.split('/')[-2]}/{repo_name}/pulls"
    
    commits_response = requests.get(commits_url, headers=HEADERS)
    commit_count = len(commits_response.json()) if commits_response.status_code == 200 else "N/A"
    
    pulls_response = requests.get(pulls_url, headers=HEADERS)
    pull_request_count = len(pulls_response.json()) if pulls_response.status_code == 200 else "N/A"

    # Prepare message for this specific repository with Pull Requests on a new line
    repo_info = f"   - 📜 Commits: {commit_count}\n"
    repo_info += f"   - 🔄 Pull Requests: {pull_request_count}\n"

    return repo_info

client.run(TOKEN)