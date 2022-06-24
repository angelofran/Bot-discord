import datetime
import requests
import random
from decouple import config
import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

bot = commands.Bot("@")

@bot.event
async def on_ready():
    activity = discord.Game(name='@ajuda| Ângelo😁', type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f"Estamos no ar!, estou conenctado como {bot.user}")
    current_time.start()


@bot.command(name="ajuda", help="Mostra tudo sobre os comandos")
async def help(ctx):
    embed = discord.Embed(
        color=0x000FF,
        title="Painel de Ajuda",
        description="Lista todos os comandos")
    embed.set_author(name="bot commands", icon_url=ctx.author.avatar_url)
    embed.add_field(
        name="binance", value="| Verifica o preço de um par na binance.Requer argumentos", inline=False)
    embed.add_field(
        name="calcular", value="| Calcula uma expressão. Argumentos: Expressão")
    embed.add_field(name="ajuda", value="| Mostra está mensagem")
    embed.add_field(
        name="foto", value="| Envia uma foto no privado. Não requer argumento")
    embed.add_field(
        name="oi", value="| Envia um Oi (Não requer argumento)")
    embed.add_field(
        name="segredo", value="| Envia um segredo no privado. Não requer argumento")
    embed.add_field(
        name="dado", value="| gira um dado e mostra um número aleatório (Requer argumentos)")
    embed.add_field(name="say", value="| Escreve ou fala")
    embed.add_field(
        name="suggest", value="| Faça uma sugestão.Requer argumentos")
    embed.add_field(
        name="ping", value="| Mostra o ping.Não requer argumentos")
    embed.add_field(name="limpar", value="| Limpa o chat")

    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "palavrão" in message.content:
        await message.channel.send(f"Por favor, {message.author.name}, não ofenda nesse servidor!")
    await message.delete()

    await bot.process_commands(message)


@bot.command(name="oi", help="Envia um Oi (Não requer argumento)")
async def send_hello(ctx):
    embed = discord.Embed(
        color=0x0000F
    )
    embed.add_field(name="Saudação", value="Olá, eu sou o Ângelo-bot!")
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Por favor, envie todos os argumentos. Digite @ajuda para ver os parâmetros de cada comando.")
    elif isinstance(error, CommandNotFound):
        await ctx.send("O comando não existe! Digite !help para ver todos os comandos.")
    else:
        raise error


@bot.command(name="calcular", help="Calcula uma expressão. Argumentos: Expressão")
async def calculate_expression(ctx, *expression):
    expression = "".join(expression)
    print(expression)
    response = eval(expression)
    await ctx.send("A resposta é: " + str(response))


@bot.command(
    nome="binance", help="Verifica o preço de um par na binance. Argumentos: moeda, base")
async def binance(ctx, coin, base):
    try:
        response = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}")
        data = response.json()  # {"symbol":"BNBBTC","price":"0.00837200"}
        price = data.get("price")  # "0.00837200"

        if price:
            await ctx.send(f"O valor do par {coin}/{base} é {price}")
        else:
            await ctx.send(f"O  par {coin}/{base} é inválido")
    except Exception as error:
        await ctx.send("Ops... Deu algum erro!")
        print(error)


@bot.command(
    name="segredo", help="Envia um segredo no privado. Não requer argumento")
async def secret(ctx):
    try:
        await ctx.author.send("Curta o Small programmer!")
        await ctx.author.send("Lá tem vários conteúdos legais!")
        await ctx.author.send("Siga o instagram do criador @xspacey, já você vai encontrar disponível o link do meu site.")
    except discord.errors.Forbidden:
        await ctx.send("Não posso te contar o segredo, habilite receber mensagens de qualquer pessoa do servidor (Opções > Privacidade)")


@bot.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)
    if reaction.emoji == "✅":
        role = user.guild.get_role(964561692644241448)
        await user.add_roles(role)
    elif reaction.emoji == "❌":
        role = user.guild.get_role(964562107418959942)
        await user.add_roles(role)


@bot.command(name="foto", help="Envia uma foto no privado. Não requer argumento")
async def get_random_image(ctx):
    url_image = "https://picsum.photos/1920/1080"

    embed_image = discord.Embed(
        title="Resultado da busca de imagem",
        description="PS: A busca é totalmente aleatória",
        color=0x0000FF,
    )

    embed_image.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed_image.set_footer(text="Feito por " +
                           bot.user.name, icon_url=bot.user.avatar_url)

    embed_image.add_field(
        name="API", value="Usamos a API do https://picsum.photos")
    embed_image.add_field(name="Parâmetros", value="{largura}/{altura}")

    embed_image.add_field(name="Exemplo", value=url_image, inline=False)

    embed_image.set_image(url=url_image)

    await ctx.send(embed=embed_image)


@bot.command(name="kick", help="Dá um kick em algum membro")
async def kick(ctx, membro: discord.Member, *, motivo=None):
    channel = bot.get_channel(964546215133982778)
    msg = f'{ctx.author.mention} expulsou o {membro.mention} por {motivo}'
    await channel.send(msg)


@bot.command(name="Ban", help="Dá um kick em algum membro")
async def Ban(ctx, membro: discord.Member, *, motivo=None):
    channel = bot.get_channel(964546215133982778)
    msg = f'{ctx.author.mention} Baniu o {membro.mention} por {motivo}'
    await channel.send(msg)


@bot.command(help="Mostra um número aleatório")
async def dado(ctx, numero):
    variavel = random.randint(1, int(numero))
    await ctx.send(f'O número que saiu no dado é {variavel}')


@bot.command(nome="say", help="Escreve ou fala")
async def say(ctx, *, mensagem):
    embed = discord.Embed(
        title=f"{mensagem}",
        description=f"Enviada por {ctx.author.name}",
        color=discord.Color.purple())
    await ctx.send(embed=embed)


@bot.command(nome="suggest", help="Manda uma sugestão")
async def suggest(ctx, *, suggestion):
    channel = bot.get_channel(964546215133982777)
    embed = discord.Embed(color=0x000FF)
    embed.set_author(
        name=f"Sugestão de {ctx.message.author}", icon_url=f"{ctx.author.avatar_url}")
    embed.add_field(name="Nova sugestão", value=f"{suggestion}")
    await ctx.send(embed=embed)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(964546214836195368)
    regras = bot.get_channel(964546214102204525)
    msg = await channel.send(f"Bem vindo {member.mention}!, Leia as regras {regras.mention}")


@bot.command(help="Mostra o ping")
async def ping(ctx):
    await ctx.send(f"Meu ping é {round(bot.latency * 1000)}ms")


@bot.command(nome="Limpar", help="Limpa o chat")
async def clear(ctx, amount=100):
    if ctx.author.guild_permissions.ban_members:
        await ctx.channel.purge(limit=amount)
        await ctx.send('**As mensagens foram apagadas com sucesso!**', delete_after=20)
    else:
        falta = 'você não tem permissão para usar o comando! '
        embed = discord.Embed(title=f"{falta}", color=0x000FF)
        await ctx.send(embed=embed)

@tasks.loop(hours=1)
async def current_time():
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y às %H:%M")
    channel = bot.get_channel(964546214102204518)
    await channel.send("Data actual: " + now)

TOKEN = config("TOKEN")
bot.run(TOKEN)
