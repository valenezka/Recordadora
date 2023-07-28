import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime

# Configura el prefijo que el bot usará para reconocer comandos
prefix = "!"
# Nombre de la base de datos
db_name = "event_reminder.db"

# Define los intents que utilizará el bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Crea una instancia del bot con los intents definidos
bot = commands.Bot(command_prefix=prefix, intents=intents)


# Función para crear la tabla en la base de datos si no existe
def create_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 event_text TEXT,
                 event_time TIMESTAMP)''')
    conn.commit()
    conn.close()

# Función para agregar un evento a la base de datos
def add_event(user_id, event_text, event_time):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO events (user_id, event_text, event_time) VALUES (?, ?, ?)",
              (user_id, event_text, event_time))
    conn.commit()
    conn.close()

# Función para obtener los eventos para un usuario en un momento dado
def get_events_for_user(user_id, event_time):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT event_text FROM events WHERE user_id=? AND event_time <= ?",
              (user_id, event_time))
    events = c.fetchall()
    conn.close()
    return events

# Evento que se ejecuta cuando el bot está listo y conectado a Discord
@bot.event
async def on_ready():
    print(f'¡El bot está listo! Conectado como {bot.user}')
    create_table()
    check_events.start()

# Comando para que el usuario agregue un evento
@bot.command()
async def recordar(ctx, tiempo, *, evento):
    try:
        event_time = datetime.strptime(tiempo, '%Y-%m-%d %H:%M')
        user_id = ctx.author.id
        add_event(user_id, evento, event_time)
        await ctx.send(f"Evento recordado: '{evento}' a las {tiempo}")
    except ValueError:
        await ctx.send("Formato de tiempo incorrecto. Utiliza el formato 'YYYY-MM-DD HH:MM'.")

# Función para comprobar y recordar los eventos programados
@tasks.loop(minutes=1)  # Comprobar eventos cada 1 minuto
async def check_events():
    now = datetime.now()
    events = get_events_for_user(1133872391991345262, now)  # Reemplaza 1234567890 con tu ID de usuario de Discord
    for event in events:
        event_text = event[0]
        user = bot.get_user(1133872391991345262)  # Reemplaza 1234567890 con tu ID de usuario de Discord
        if user:
            await user.send(f"Recuerdo: '{event_text}'")

# Reemplaza 'TOKEN' con el token que obtuviste en el paso 1
bot.run('MTEzMzg3MjM5MTk5MTM0NTI2Mg.GpTuBj.ktKue1h_GdcJyITZH28rDdvLB5JmiJSNaWEoCc')
