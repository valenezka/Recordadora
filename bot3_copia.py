import discord
from discord.ext import commands, tasks
import json
from datetime import datetime
intents= discord.Intents.all()
# Nombre del archivo JSON para guardar los eventos
json_file = "event_reminder.json"

bot=commands.Bot(
    command_prefix="!",
    description="Bot Recordador de eventos",
    intents=intents,
)
# Función para cargar los eventos desde el archivo JSON
def load_events():
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Función para guardar los eventos en el archivo JSON
def save_events(events):
    with open(json_file, 'w') as file:
        json.dump(events, file)
@bot.event
async def on_ready():
    print(f"Bot conectado {len(bot.guilds)} ")
    check_events.start()

@bot.event
async def on_message(message):
    print("message:", message)
    print(f"USER-{message.author}texted - {message.content}")
    await bot.process_commands(message)
@bot.command()
async def recordar(ctx, tiempo, *, evento):
    
        event_time = datetime.strptime("2003-06-03-14:00", r'%Y-%m-%d-%H:%M') 
        user_id = ctx.author.id
        print(tiempo)
        print(evento)
        # Carga los eventos existentes desde el archivo JSON
        events = load_events()

    

        # Agrega el nuevo evento al diccionario
        if user_id not in events:
            events[str(user_id)] = []
        events[str(user_id)].append({"event_text": evento, "event_time": tiempo})


        # Guarda los eventos actualizados en el archivo JSON
        save_events(events)

        await ctx.send(f"Evento recordado: '{evento}' a las {tiempo}")
   

# Función para comprobar y recordar los eventos programados
@tasks.loop(seconds=30)  # Comprobar eventos cada 30 segundos
async def check_events():
    
    now = datetime.now()
    events = load_events()

    for user_id, user_events in events.items():
        for index, event in enumerate(user_events):
            event_time = datetime.strptime(event["event_time"], r'%Y-%m-%d-%H:%M')

            if event_time <= now:
                event_text = event["event_text"]
                user = bot.get_user(int(user_id))
                if user:
                    await user.send(f"Recuerdo: '{event_text}'")

                # Eliminar el evento de la lista de eventos del usuario
                user_events.pop(index)
                save_events(events)  # Guardar la lista actualizada en el archivo JSON

    # now = datetime.now()
    # print(now)
    # # Cargar eventos desde el archivo JSON
    # events = load_events()
    # print(events)

    # # Recorrer todos los usuarios y verificar eventos
    # for user_id, user_events in events.items():
    #     for event in user_events:
    #         event_time = datetime.strptime(event["event_time"], r'%Y-%m-%d-%H:%M')
    #         print(f"\n",event_time, end="\n")
    #         if event_time <= now:
    #             event_text = event["event_text"]
    #             user = bot.get_user(int(user_id))
    #             if user:
    #                 await user.send(f"Recuerdo: '{event_text}'")

                
                
#Eliminar recordatorio
# @bot.command()
# async def eliminar_recordatorio(ctx, index):
#     user_id = str(ctx.author.id)

#     # Cargar los eventos existentes desde el archivo JSON
#     events = load_events()

#     if user_id not in events:
#         await ctx.send("No tienes eventos recordados.")
#         return

#     user_events = events[user_id]

#     try:
#         index = int(index) - 1  # Ajustar el índice para que empiece en 0
#         if 0 <= index < len(user_events):
#             evento_eliminado = user_events.pop(index)
#             save_events(events)
#             await ctx.send(f"Evento recordado eliminado: '{evento_eliminado['event_text']}' a las {evento_eliminado['event_time']}")
#         else:
#             await ctx.send("El índice del evento recordado es inválido.")
#     except ValueError:
#         await ctx.send("Debes proporcionar un número de índice válido.")


@bot.command()
async def saludar(ctx):
    print("comando recibido")
    await ctx.send("Holaaa")

bot.run("MTEzMzg3MjM5MTk5MTM0NTI2Mg.G3Gv_H.sy7iwv_A1p5tESBOr5MeX3XfZOXA4SvWFcv1YQ")