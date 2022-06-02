# This program is free software. It comes without any warranty, to

#     * the extent permitted by applicable law. You can redistribute it
#     * and/or modify it under the terms of the Do What The Fuck You Want
#     * To Public License, Version 2, as published by Sam Hocevar. See
#     * http://www.wtfpl.net/ for more details.

import typing
import disnake

from config import botconfig

client = disnake.Client()

intents = disnake.Intents.default()
intents.reactions = True

messageId = botconfig["messageId"]
channelId = botconfig["channelId"]
reactionRoles = botconfig["reactionRoles"]

async def add_reactions() -> None:

    channel = await client.fetch_channel(channelId)

    message = await channel.fetch_message(messageId)


    for i in reactionRoles:
        await message.add_reaction(i)

    print('client is ready')

@client.event
async def on_ready() -> None:
    await add_reactions()

@client.event
async def on_raw_reaction_add(event: disnake.RawReactionActionEvent) -> None:

    print('event add triggered')

    channel = await client.fetch_channel(channelId)

    if event.message_id == messageId:

        print('1')
        emoji = event.emoji.name
        print('2')
        roleToGive = disnake.utils.get(channel.guild.roles, id=reactionRoles[emoji])
        print('3')
        await event.member.add_roles(roleToGive)

@client.event
async def on_raw_reaction_remove(event: disnake.RawReactionActionEvent) -> None:

    channel = await client.fetch_channel(channelId)
    member = await channel.guild.fetch_member(event.user_id)
    print('event remove triggered')

    if event.message_id == messageId:

        emoji = event.emoji.name
        roleToGive = disnake.utils.get(channel.guild.roles, id=reactionRoles[emoji])

        await member.remove_roles(roleToGive)