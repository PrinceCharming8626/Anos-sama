import aiohttp
import discord
import datetime
import animec
from discord.ext import commands
# import xml.etree.ElementTree as ET


class anime(commands.Cog):
    '''Alles rund um Animes'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @commands.command(aliases=['anilist'])
    async def anime(self, ctx, *, animeName: str):
        '''search anime from anilist.com
        '''
        api = 'https://graphql.anilist.co'
        query = """
        query ($name: String){
          Media(search: $name, type: ANIME) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            synonyms
            format
            status
            episodes
            duration
            nextAiringEpisode {
              episode
            }
            averageScore
            meanScore
            source
            genres
            tags {
              name
            }
            studios(isMain: true) {
              nodes {
                name
              }
            }
            siteUrl
          }
        }
        """
        variables = {
            'name': animeName
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api, json={'query': query, 'variables': variables}) as r:
                if r.status == 200:
                    json = await r.json()
                    data = json['data']['Media']

                    embed = discord.Embed(color=ctx.author.colour)
                    embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                    embed.set_thumbnail(url=data['coverImage']['large'])
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        embed.add_field(name='Title', value=data['title']['romaji'], inline=False)
                    else:
                        embed.add_field(name='Title', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)

                    embed.add_field(name='Description', value=data['description'], inline=False)
                    if data['synonyms'] != []:
                        embed.add_field(name='Synonyms', value=', '.join(data['synonyms']), inline=True)

                    embed.add_field(name='Type', value=data['format'].replace('_', ' ').title().replace('Tv', 'TV'), inline=True)
                    if data['episodes'] > 1:
                        embed.add_field(name='Episodes and Durations', value='{} ep and {} min'.format(data['episodes'], data['duration']), inline=True)
                    else:
                        embed.add_field(name='Dauer', value=str(data['duration']) + ' min', inline=True)

                    embed.add_field(name='Start date', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
                    if data['endDate']['day'] == None:
                        embed.add_field(name='Released Folgen', value=data['nextAiringEpisode']['episode'] - 1, inline=True)
                    elif data['episodes'] > 1:
                        embed.add_field(name='End date', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)

                    embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)

                    try:
                        embed.add_field(name='Studio', value=data['studios']['nodes'][0]['name'], inline=True)
                    except IndexError:
                        pass
                    embed.add_field(name='Score', value=data['averageScore'], inline=True)
                    embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    embed.add_field(name='Tags', value=tags[:-2], inline=False)
                    try:
                        embed.add_field(name=' Anime Adaptation', value=data['source'].replace('_', ' ').title(), inline=True)
                    except AttributeError:
                        pass

                    embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                    embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send('❌ No anime found!')

    @commands.command()
    async def manga(self, ctx, *, mangaName: str):
        '''search manga from anilist.com
        '''
        api = 'https://graphql.anilist.co'
        query = """
        query ($name: String){
          Media(search: $name, type: MANGA) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            status
            chapters
            volumes
            averageScore
            meanScore
            genres
            tags {
              name
            }
            siteUrl
          }
        }
        """
        variables = {
            'name': mangaName
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api, json={'query': query, 'variables': variables}) as r:
                if r.status == 200:
                    json = await r.json()
                    data = json['data']['Media']

                    embed = discord.Embed(color=ctx.author.colour)
                    embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                    embed.set_thumbnail(url=data['coverImage']['large'])
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        embed.add_field(name='Title', value=data['title']['romaji'], inline=False)
                    else:
                        embed.add_field(name='Title', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)
                    embed.add_field(name='Description', value=data['description'], inline=False)
                    if data['chapters'] != None:
                        # https://github.com/AniList/ApiV2-GraphQL-Docs/issues/47
                        embed.add_field(name='Kapitel', value=data['chapters'], inline=True)
                    if data['volumes'] != None:
                        embed.add_field(name='Bände', value=data['volumes'], inline=True)
                    embed.add_field(name='Start date', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
                    if data['endDate']['day'] != None:
                        embed.add_field(name='End date', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)
                    embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)
                    embed.add_field(name='Score', value=data['averageScore'], inline=True)
                    embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    embed.add_field(name='Tags', value=tags[:-2], inline=False)
                    embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                    embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send('❌ No manga found!')

    @commands.command()
    async def aninews(self, ctx, amount:int=8):
      '''get latest anime news
      '''
      news=animec.Aninews(amount)
      links=news.links
      titles=news.titles
      descriptions=news.description
      embed = discord.Embed(title="Latest Anime News",color = ctx.author.color,timestamp=datetime.datetime.utcnow())
      embed.set_thumbnail(url=news.images[0])

      for i in range(amount):
        embed.add_field(name=f"{i+1}) {titles[i]}",value=f"{descriptions[i][:200]}...\n[Read more]({links[i]})",inline=False)
      await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(anime(bot))
