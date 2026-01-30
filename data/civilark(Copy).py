# Modules
import signal
import random
import time
import os
import threading
import sys, psutil
import json
import keyboard
import requests
from PIL import Image
try:
	from googletrans import Translator
	translator_engine = Translator()
	translator_saves = {}
except Exception as e:
	print(e)
	translator_engine = None
	translator_saves = {}
try:
	os.chdir("CivilArk")
except:
	pass

def translate(text, target):
	global translator_engine, translator_saves
	oldtext = text
	if target == "en":
		return text
	if (text, target) in translator_saves:
		return translator_saves[(text, target)]
	try:
		text = translator_engine.translate(text, dest=target).text
	except:
		text = text
	translator_saves[(oldtext, target)] = text
	return text

# Screen and Game Engine
class AertScreenEngine:
	def __init__(self, width=512, height=512, title="AertScreenEngine - Project"):
		import pygame as engineroot
		from PIL import Image
		import numpy as np
		import time
		import random
		import requests
		import threading
		engineroot.mixer.init()
		engineroot.mixer.set_num_channels(1001)
		self.engineroot = engineroot
		self.engineroot.init()
		self.device_width = engineroot.display.Info().current_w
		self.device_height = engineroot.display.Info().current_h
		self.engineroot_Image = Image
		self.engineroot_random = random
		self.engineroot_requests = requests
		self.engineroot_threading = threading
		self.np = np
		self.engineroot_time = time
		self.width = width
		self.height = height
		self.screen = engineroot.display.set_mode((width, height))
		self.images = {}
		self.sounds = {}
		self.auto_update = False
		self.auto_image_save = True
		self.debug_run = True
		self.set_screen_title(title=title)
	def set_screen_size(self, width=512, height=512):
		self.engineroot.display.set_mode((width, height))
		self.width = width
		self.height = height
	def set_screen_title(self, title="AertScreenEngine - Project"):
		self.engineroot.display.set_caption(title=title, icontitle=title)
		if self.auto_update:
			self.update()
	def set_screen_fullscreen(self):
		self.engineroot.display.set_mode(flags=self.engineroot.FULLSCREEN)
		if self.auto_update:
			self.update()
	def set_screen_resizable(self):
		self.engineroot.display.set_mode(flags=self.engineroot.RESIZABLE)
		if self.auto_update:
			self.update()
	def set_screen_noframe(self):
		self.engineroot.display.set_mode(flags=self.engineroot.NOFRAME)
		if self.auto_update:
			self.update()
	def set_screen_icon(self, imagename):
		self.engineroot.display.set_icon(self.images[imagename])
		if self.auto_update:
			self.update()
	def delete(self):
		self.engineroot.quit()
		del self
	def draw_all(self, color=(128, 128, 128)):
		self.screen.fill(color)
		if self.auto_update:
			self.update()
	def draw_cube(self, color=(128, 128, 128), x=0, y=0, width=64, height=64):
		self.engineroot.draw.rect(self.screen, color, (x, y, width, height))
		if self.auto_update:
			self.update()
	def draw_circle(self, color=(128, 128, 128), x=0, y=0, width=64, height=64):
		self.engineroot.draw.circle(self.screen, color, (x, y), (width+height)/2)
		if self.auto_update:
			self.update()
	def draw_stick(self, color=(128, 128, 128), start_x=0, start_y=0, end_x=0, end_y=0, width=64, height=64):
		self.engineroot.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), (width+height)//2)
		if self.auto_update:
			self.update()
	def draw_ellipse(self, color=(128, 128, 128), x=0, y=0, width=64, height=64):
		self.engineroot.draw.ellipse(self.screen, color, (x, y, width, height))
		if self.auto_update:
			self.update()
	def draw_polygon(self, color=(128, 128, 128), targets=[(0, 0), (64, 32), (32, 64)]):
		self.engineroot.draw.polygon(self.screen, color, targets)
		if self.auto_update:
			self.update()
	def draw_text(self, color=(128, 128, 128), x=0, y=0, font="", text="Hello, World!", alpha=255, width=64, height=64):
		imagename = (color, font, text, alpha, (width+height)//2)
		if imagename not in self.images:
			if not os.path.exists(font):
				font = self.engineroot.font.SysFont(font, (width+height)//2)
			else:
				font = self.engineroot.font.Font(font, (width+height)//2)
			surface = font.render(text, True, color)
			surface = surface.convert_alpha()
			surface.fill((255, 255, 255, alpha), special_flags=self.engineroot.BLEND_RGBA_MULT)
			if self.auto_image_save:
				self.images[imagename] = surface
		else:
			surface = self.images[imagename]
		self.screen.blit(surface, (x, y))
		if self.auto_update:
			self.update()
	def load_image(self, imagename, image, width=64, height=64, alpha=255, colorchanger=False, colorchanger_color=(255, 255, 255), colorchanger_force=64, internet=False, rotate=0):
		if internet:
			content = self.engineroot_requests.get(image).content
			ender = image[image.rfind(".")+1:]
			image = str(self.engineroot_random.randint(0, 1000000))+"."+ender
			with open(image, "wb") as f:
				f.write(content)
		if colorchanger:
			original = self.engineroot_Image.open(image)
			original = original.convert("RGBA")
			pixels = list(original.getdata())
			newpixels = []
			for r, g, b, a in pixels:
				if r > colorchanger_color[0]:
					r -= colorchanger_force
				else:
					r += colorchanger_force
				r = max(min(r, 255), 0)
				if g > colorchanger_color[1]:
					g -= colorchanger_force
				else:
					g += colorchanger_force
				g = max(min(g, 255), 0)
				if b > colorchanger_color[2]:
					b -= colorchanger_force
				else:
					b += colorchanger_force
				b = max(min(b, 255), 0)
				newpixels.append((r, g, b, a))
			original.putdata(newpixels)
			original = original.resize((width, height), self.engineroot_Image.LANCZOS)
			surface = self.engineroot.image.fromstring(original.tobytes(), original.size, original.mode)
			surface.set_alpha(alpha)
			surface = self.engineroot.transform.rotate(surface, rotate)
			self.images[imagename] = surface
		else:
			surface = self.engineroot.image.load(image)
			surface = self.engineroot.transform.smoothscale(surface, (width, height))
			surface = surface.convert_alpha()
			surface.set_alpha(alpha)
			surface = self.engineroot.transform.rotate(surface, rotate)
			self.images[imagename] = surface
	def draw_image(self, imagename, x=0, y=0):
		self.screen.blit(self.images[imagename], (x, y))
		if self.auto_update:
			self.update()
	def draw(self, color=(128, 128, 128), x=0, y=0):
		self.screen.set_at((x, y), color)
		if self.auto_update:
			self.update()
	def events(self):
		return self.engineroot.event.get()
	def events_checkquit(self, events):
		for event in events:
			if event.type == self.engineroot.QUIT:
				return True
		return False
	def events_checkmouse(self, events):
		results = []
		for event in events:
			if event.type == self.engineroot.MOUSEBUTTONDOWN:
				results.append((event.pos, "down"))
			if event.type == self.engineroot.MOUSEBUTTONUP:
				results.append((event.pos, "up"))
		return results
	def events_checkkeyboard(self, events):
		results = []
		for event in events:
			if event.type == self.engineroot.KEYDOWN:
				results.append(self.engineroot.key.name(event.key))
		return results
	def mouse_position(self):
		return self.engineroot.mouse.get_pos()
	def music_load(self, soundname, music, volume=1):
		sound = self.engineroot.mixer.Sound(music)
		sound.set_volume(volume)
		self.sounds[soundname] = sound
	def music_manual_load(self, soundname, hz=100, samplerate=44100, volume=1, seconds=0.1):
		samples = self.np.arange(samplerate*seconds)
		wave = self.np.sin(2*self.np.pi*hz*samples/samplerate)*volume
		wave = self.np.column_stack((wave, wave))
		sound_array = self.np.array(wave * 32767, dtype=self.np.int16)
		sound = self.engineroot.sndarray.make_sound(sound_array)
		self.sounds[soundname] = sound
	def music_play(self, soundname, channel=0, loop=False, volume=1):
		target = self.engineroot.mixer.Channel(channel)
		if loop:
			loop = -1
		else:
			loop = 0
		sound = self.sounds[soundname].get_raw()
		ss = self.engineroot.mixer.Sound(buffer=sound)
		ss.set_volume(volume)
		target.play(ss, loops=loop)
	def music_play_list(self, soundnames, channel=0, volume=1):
		for sound, waiting in soundnames:
			self.music_play(sound, channel=channel, volume=volume)
			self.engineroot_time.sleep(waiting)
	def music_stop(self, channel=0):
		target = self.engineroot.mixer.Channel(channel)
		target.stop()
	def update(self):
		self.engineroot.display.flip()
	def __debug(self, quiting=True):
		while self.debug_run:
			events = self.events()
			if self.events_checkquit(events):
				if quiting:
					self.debug_run = False
	def debug(self, quiting=True):
		self.__debug(quiting=quiting)
# Screen and Game Engine

# Main Variables

# Variable - Game Details
screen_icon = "data/Pictures/civilark_small.png"
syshanbur_logo = "data/Pictures/syshanbur.png"
civilark_full = "data/Pictures/civilark_full.png"
menu_bg = "data/Pictures/menu_bg.png"
map_image = "data/Pictures/civilark_map.jpg"
button_image = "data/Pictures/button.png"
screen_loading = "data/Pictures/loading.png"
background_musics = [["data/Music/Sg0A3.mp3", 60*4], ["data/Music/Sg0A4.mp3", 60*4], ["data/Music/Sg0A5.mp3", 60*4], ["data/Music/Sg0B1.mp3", 60+27], ["data/Music/Sg0B2.mp3", (60*3)+28], ["data/Music/Sg0A1.mp3", 4*60], ["data/Music/Sg0A2.mp3", (2*60)+46]]
random.shuffle(background_musics)
click_sounds = ["click1", "click2", "click3", "click4"]
music_volume = 0.3
soundeffect_volume = 0.1
english_words = list(json.loads(open("data/Detail/words_en.json").read()))
try:
	with open("data/Detail/game_language.txt", "r") as f:
		lang = f.read()
except:
	lang = "en"

# Variable - Game Engine
screen_root = AertScreenEngine(title="CivilArk")

screen_root.set_screen_size(screen_root.device_width, screen_root.device_height)
screen_root.set_screen_fullscreen()
try:
	screen_root.load_image("screen_icon", screen_icon)
	screen_root.set_screen_icon("screen_icon")
except Exception as e:
	print(f"Error on icon loading: {e}")
try:
	screen_root.load_image("loading", screen_loading, alpha=200, width=screen_root.width, height=screen_root.height)
except Exception as e:
	print(f"Error on loading screen loading: {e}")
	
# Loading SCREEN
def loading_screen():
	global screen_root
	screen_root.update()
	try:
		screen_root.draw_image("loading")
	except:
		pass
	text = random.choice(['The birds are singing, the flowers are blooming... - Undertale (Sans)', 'Everyone was a child once. - The Lion King (Movie)', 'Take one step, the world is yours. - The Matrix (Movie)', 'Life is like a box of chocolates. - Forrest Gump (Movie)', 'A long journey begins with a single step. - Yoda, Star Wars', 'Good-hearted people always lose. - V for Vendetta (Movie)', "We can't live forever, but we can live a beautiful life together. - Harry Potter and the Deathly Hallows (Movie)", "Don't forget me. - The Notebook (Movie)", 'Life goes on. - Friends (TV show)', 'Understanding time is impossible before you lose it. - Back to the Future (Movie)', 'I am Groot. - Guardians of the Galaxy (Movie)', 'I’m the one who knocks. - Breaking Bad (TV show)', 'What’s in the box? - Se7en (Movie)', 'It’s alive! - Frankenstein (Movie)', "You're gonna need a bigger boat. - Jaws (Movie)", 'Just do it! - Nike (Ad slogan)', 'I’ve always depended on the kindness of strangers. - A Streetcar Named Desire (Movie)', 'I coulda been a contender. - On the Waterfront (Movie)', "You had me at 'hello.' - Jerry Maguire (Movie)", 'Keep calm and carry on. - WWII British Propaganda Slogan', 'You can’t handle the truth! - A Few Good Men (Movie)', 'I love the smell of napalm in the morning. - Apocalypse Now (Movie)', 'Nobody calls me chicken. - Back to the Future (Movie)', 'I feel the need… the need for speed. - Top Gun (Movie)', 'This is Sparta! - 300 (Movie)', 'Why so serious? - The Dark Knight (Movie)', 'I’ll be back. - The Terminator (Movie)', 'This is the way. - The Mandalorian (TV show)', 'Show me the money! - Jerry Maguire (Movie)', 'I am Groot. - Guardians of the Galaxy (Movie)', 'I’m the one who knocks. - Breaking Bad (TV show)', 'What’s in the box? - Se7en (Movie)', 'It’s alive! - Frankenstein (Movie)', "You're gonna need a bigger boat. - Jaws (Movie)", 'Just do it! - Nike (Ad slogan)', 'I’ve always depended on the kindness of strangers. - A Streetcar Named Desire (Movie)', 'I coulda been a contender. - On the Waterfront (Movie)', "You had me at 'hello.' - Jerry Maguire (Movie)", 'Keep calm and carry on. - WWII British Propaganda Slogan', 'The only thing we have to fear is fear itself. - Franklin D. Roosevelt', 'In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.', "That's one small step for [a] man, one giant leap for mankind. - Neil Armstrong", 'I think, therefore I am. - René Descartes', 'To be, or not to be, that is the question. - William Shakespeare', 'An eye for an eye only ends up making the whole world blind. - Mahatma Gandhi', 'Not all those who wander are lost. - J.R.R. Tolkien', 'Give me liberty, or give me death! - Patrick Henry', 'Power tends to corrupt, and absolute power corrupts absolutely. - Lord Acton', 'The unexamined life is not worth living. - Socrates', 'Be the change that you wish to see in the world. - Mahatma Gandhi', 'Imagination is more important than knowledge. - Albert Einstein', 'The only way to do great work is to love what you do. - Steve Jobs', "Life is what happens when you're busy making other plans. - John Lennon", 'The truth will set you free, but first it will make you miserable. - James A. Garfield', 'Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson', 'To thine own self be true. - William Shakespeare', 'It does not matter how slowly you go as long as you do not stop. - Confucius', 'The only thing that is constant is change. - Heraclitus', 'That which does not kill us makes us stronger. - Friedrich Nietzsche', 'The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela', 'What we think, we become. - Buddha', 'You miss 100% of the shots you don’t take. - Wayne Gretzky', 'Imagination is more important than knowledge. - Albert Einstein', 'Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill', "Life is what happens when you're busy making other plans. - John Lennon", 'The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb', 'Act as if what you do makes a difference. It does. - William James', 'I am not a product of my circumstances. I am a product of my decisions. - Stephen R. Covey', 'The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt', 'You only live once, but if you do it right, once is enough. - Mae West', "Believe you can and you're halfway there. - Theodore Roosevelt", 'The journey of a thousand miles begins with one step. - Lao Tzu', 'You are never too old to set another goal or to dream a new dream. - C.S. Lewis', 'Don’t wait. The time will never be just right. - Napoleon Hill', 'The best way to predict the future is to create it. - Abraham Lincoln', 'The only impossible journey is the one you never begin. - Tony Robbins', 'You don’t have to be great to start, but you have to start to be great. - Zig Ziglar', 'We are what we repeatedly do. Excellence, then, is not an act, but a habit. - Aristotle', 'Life is either a daring adventure or nothing at all. - Helen Keller', 'Success doesn’t come from what you do occasionally, it comes from what you do consistently. - Marie Forleo', 'In the end, we only regret the chances we didn’t take. - Lewis Carroll', "I don't like philosophy, I will fuck your mother. - aertsimon90"])
	screen_root.draw_text(text=text, color=(255, 255, 255), width=int(32/(len(text)/60)), height=int(32/(len(text)/60)), x=0, y=0)
	screen_root.update()
# Loading SCREEN

loading_screen()
try:
	screen_root.load_image("civilark_full", civilark_full, width=screen_root.width/2.5, height=screen_root.height/4.5)
except Exception as e:
	print(f"Error on civilark full logo loading: {e}")
try:
	screen_root.load_image("menu_civilark", civilark_full, width=screen_root.width/3, height=screen_root.height/4.5)
except Exception as e:
	print(f"Error on civilark full logo for menu loading: {e}")
try:
	screen_root.load_image("menu_bg", menu_bg, width=screen_root.width/3, height=screen_root.height)
except Exception as e:
	print(f"Error on menu background loading: {e}")
try:
	screen_root.load_image("settings_bg", menu_bg, width=screen_root.width/2, height=screen_root.height)
except Exception as e:
	print(f"Error on menu background loading: {e}")
try:
	screen_root.load_image("ongame_bg", menu_bg, width=550, height=192+32, alpha=150)
except Exception as e:
	print(f"Error on game background loading: {e}")
try:
	screen_root.load_image("map", map_image, width=screen_root.width, height=screen_root.height)
except Exception as e:
	print(f"Error on map image loading: {e}")
try:
	screen_root.load_image("button", button_image, width=screen_root.width/5.0, height=screen_root.height/20)
except Exception as e:
	print(f"Error on map image loading: {e}")
for music, _ in background_musics:
	try:
		screen_root.music_load(music, music)
	except Exception as e:
		print(f"Error on {music} loading: {e}")
screen_root.music_manual_load("click1", hz=465, seconds=0.03)
screen_root.music_manual_load("click2", hz=445, seconds=0.04)
screen_root.music_manual_load("click3", hz=475, seconds=0.02)
screen_root.music_manual_load("click4", hz=500, seconds=0.025)

# Main Functions

def play_click():
	global soundeffect_volume, click_sounds, screen_root
	screen_root.music_play(random.choice(click_sounds), volume=soundeffect_volume, channel=random.randint(1, 999))

def play_background_auto_thread():
	global background_musics, screen_root, music_volume
	while True:
		random.shuffle(background_musics)
		for music, wait in background_musics:
			screen_root.music_play(music, volume=music_volume, channel=0)
			time.sleep(wait)
		

def opening_screen():
	global screen_root
	for n in range(1, 128):
		screen_root.draw_all((0, 0, 0))
		try:
			screen_root.load_image("syshanbur", syshanbur_logo, width=screen_root.width, height=screen_root.height/1.5, alpha=n)
		except Exception as e:
			print(f"Error on syshanbur logo loading: {e}")
		screen_root.draw_image("syshanbur", x=(screen_root.width/2)-(screen_root.width/2), y=(screen_root.height/2)-(screen_root.height/3))
		screen_root.update()
		time.sleep(0.0005)
		screen_root.events()
	for n in range(0, 128)[::-1]:
		screen_root.draw_all((0, 0, 0))
		try:
			screen_root.load_image("syshanbur", syshanbur_logo, width=screen_root.width/1, height=screen_root.height/1.5, alpha=n)
		except Exception as e:
			print(f"Error on syshanbur logo loading: {e}")
		screen_root.draw_image("syshanbur", x=(screen_root.width/2)-(screen_root.width/2), y=(screen_root.height/2)-(screen_root.height/3))
		screen_root.update()
		time.sleep(0.0005)
		screen_root.events()
	screen_root.draw_all((0, 0, 0))
	screen_root.update()

def settings():
	global screen_root, music_volume, soundeffect_volume, lang
	loading_screen()
	textsize = 30
	textcolor = (255, 255, 255)
	clickcolor = (255, 255, 0)
	settings_text = translate("Game Settings", lang)
	setlangtext = translate(f"[ Change the language ({lang}) ]", lang)
	setsingletext = translate(f"[ Change the Singleplayer account ]", lang)
	setmultitext = translate(f"[ Change the Multiplayer account ]", lang)
	exittext = translate(f"[ Exit from settings ]", lang)
	sound_effect_volume_text = translate(f"Sound Effect Volume", lang)
	music_volume_text = translate(f"Music Volume", lang)
	while True:
		screen_root.draw_all((0, 0, 0))
		screen_root.draw_image("map")
		screen_root.draw_image("settings_bg", x=screen_root.width/5)
		logox = (screen_root.width/2)-(screen_root.width/4)
		logoy = ((screen_root.height/2)-(screen_root.width/12))/5
		screen_root.draw_image("civilark_full", x=logox, y=logoy)
		screen_root.draw_text(text=settings_text, x=logox, y=logoy+(screen_root.height/6)+100, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=f"{music_volume_text}: {music_volume*100:.0f}%", x=logox, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=f"+", x=logox+230, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"-", x=logox+250, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"{sound_effect_volume_text}: {soundeffect_volume*100:.0f}%", x=logox, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=f"+", x=logox+300, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"-", x=logox+320, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=setlangtext, x=logox, y=logoy+(screen_root.height/6)+270, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=setsingletext, x=logox, y=logoy+(screen_root.height/6)+300, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=setmultitext, x=logox, y=logoy+(screen_root.height/6)+330, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=exittext, x=logox, y=logoy+(screen_root.height/6)+370, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		events = screen_root.events()
		for pos, _ in screen_root.events_checkmouse(events):
			x = pos[0]
			y = pos[1]
			if x >= logox+230:
				if x <= logox+230+textsize:
					if y >= logoy+(screen_root.height/6)+190:
						if y <= logoy+(screen_root.height/6)+190+(textsize/3):
							play_click()
							music_volume += 0.01
							screen_root.engineroot.mixer.Channel(0).set_volume(music_volume)
							screen_root.draw_text(text=f"+", x=logox+230, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=clickcolor)
							time.sleep(0.01)
			if x >= logox+250:
				if x <= logox+250+textsize:
					if y >= logoy+(screen_root.height/6)+190:
						if y <= logoy+(screen_root.height/6)+190+textsize:
							play_click()
							music_volume -= 0.01
							screen_root.engineroot.mixer.Channel(0).set_volume(music_volume)
							screen_root.draw_text(text=f"-", x=logox+250, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=clickcolor)
							time.sleep(0.01)
			if x >= logox+300:
				if x <= logox+300+textsize:
					if y >= logoy+(screen_root.height/6)+190+32:
						if y <= logoy+(screen_root.height/6)+190+32+(textsize/3):
							play_click()
							soundeffect_volume += 0.01
							screen_root.draw_text(text=f"+", x=logox+300, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=clickcolor)
							time.sleep(0.01)
			if x >= logox+320:
				if x <= logox+320+textsize:
					if y >= logoy+(screen_root.height/6)+190+32:
						if y <= logoy+(screen_root.height/6)+190+32+textsize:
							play_click()
							soundeffect_volume -= 0.01
							screen_root.draw_text(text=f"-", x=logox+320, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=clickcolor)
							time.sleep(0.01)
			if logox <= x <= logox + (textsize * len(setlangtext)):
				if logoy + (screen_root.height / 6) + 270 <= y <= logoy + (screen_root.height / 6) + 270 + textsize:
					play_click()
					screen_root.draw_text(text=setlangtext, x=logox, y=logoy+(screen_root.height/6)+270, width=textsize, height=textsize, color=clickcolor, font="Font Squirrel")
					screen_root.update()
					time.sleep(0.01)
					edit_gui("data/Detail/game_language.txt", lang)
					with open("data/Detail/game_language.txt", "r") as f:
						lang = f.read()
			if logox <= x <= logox + (textsize * len(setsingletext)):
				if logoy + (screen_root.height / 6) + 300 <= y <= logoy + (screen_root.height / 6) + 300 + textsize:
					play_click()
					screen_root.draw_text(text=setsingletext, x=logox, y=logoy+(screen_root.height/6)+300, width=textsize, height=textsize, color=clickcolor, font="Font Squirrel")
					screen_root.update()
					time.sleep(0.01)
					if not os.path.exists("data/Singleplayer/player_account.txt"):
						with open("data/Singleplayer/player_account.txt", "w") as f:
							f.write("USERNAME: single_player\nPASSWORD: password")
					os.system("notepad.exe data/Singleplayer/player_account.txt")
			if logox <= x <= logox + (textsize * len(setmultitext)):
				if logoy + (screen_root.height / 6) + 330 <= y <= logoy + (screen_root.height / 6) + 330 + textsize:
					play_click()
					screen_root.draw_text(text=setmultitext, x=logox, y=logoy+(screen_root.height/6)+330, width=textsize, height=textsize, color=clickcolor, font="Font Squirrel")
					screen_root.update()
					time.sleep(0.01)
					if not os.path.exists("data/Multiplayer/player_account.txt"):
						with open("data/Multiplayer/player_account.txt", "w") as f:
							f.write(f"USERNAME: {randomusername()}\nPASSWORD: {randompassword()}")
					os.system("notepad.exe data/Multiplayer/player_account.txt")
			if logox <= x <= logox + (textsize * len(exittext)):
				if logoy + (screen_root.height / 6) + 370 <= y <= logoy + (screen_root.height / 6) + 370 + textsize:
					play_click()
					screen_root.draw_text(text=exittext, x=logox, y=logoy+(screen_root.height/6)+370, width=textsize, height=textsize, color=clickcolor, font="Font Squirrel")
					screen_root.update()
					time.sleep(0.01)
					return
		screen_root.update();time.sleep(1/40)
	screen_root.draw_all((0, 0, 0))
	screen_root.update()

def credits():
	global screen_root, music_volume, soundeffect_volume, lang
	loading_screen()
	clicknext = translate("[ Click and next! ]", lang)
	textsize = 50
	textcolor = (255, 255, 255)
	names = ["omurcek_ - Studio Owner", "aertsimon90 - Coder", "kka0023 - Financial Supporter", "denizbt_0 - Design", "kurusoup - Design", "Ege Yonar - Soundover"]
	emoji_and_colors = [(':)', (127, 111, 93)), (':D', (127, 112, 51)), (':)?', (127, 102, 51)), ('B)', (76, 76, 127)), ('^_^', (127, 76, 51)), ('>:( ', (127, 51, 51)), ('-_-', (102, 102, 102)), ('<3', (127, 0, 0))]
	random.shuffle(emoji_and_colors)
	for i, name in enumerate(names):
		target = emoji_and_colors[i]
		emoji = target[0]
		color = target[1]
		screen_root.draw_all(color)
		for _ in range(64):
			screen_root.draw_text(text=emoji, x=random.randint(0, screen_root.width), y=random.randint(0, screen_root.height), width=random.randint(0, 64), color=(color[0]+50, color[1]+50, color[2]+50))
		screen_root.draw_text(text=name, x=(screen_root.width/2)-(len(name)*textsize/6), y=screen_root.height/2, color=textcolor, width=textsize, height=textsize)
		screen_root.draw_text(text=clicknext, x=(screen_root.width/2)-(len(name)*textsize/6), y=screen_root.height/2+(textsize*5), color=textcolor, width=textsize, height=textsize)
		screen_root.update()
		for _ in range(10):
			screen_root.update()
			events = screen_root.events()
			events = events[::-1]
			if len(screen_root.events_checkmouse(events)) >= 1:
				play_click()
				break
			time.sleep(0.5)
def singleplayer():
	global screen_root, map_image, lang
	loading_screen()
	root = CivilArk_Local(map_image, screen_root.width, screen_root.height)
	if not os.path.exists("data/Singleplayer/player_account.txt"):
		with open("data/Singleplayer/player_account.txt", "w") as f:
			f.write("USERNAME: single_player\nPASSWORD: password")
			username = "single_player"
			password = "password"
	else:
		with open("data/Singleplayer/player_account.txt", "r") as f:
			data = f.read().split("\n")
		username = data[0][data[0].find("USERNAME: ")+10:]
		password = data[1][data[1].find("PASSWORD: ")+10:]
	for _ in range(random.randint(5, 15)):
		root.new_bot()
	try:
		root.load()
	except:
		pass
	n = 1
	usernametext = translate("Username: ", lang)+username
	startgame = translate("Select a land for start the game.", lang)
	sourcetext = translate("Source", lang)
	populationtext = translate("Population", lang)
	soldierstext = translate("Soldiers", lang)
	trainsoldiertext = translate("[ Train the Soldier ]", lang)
	ctrlstext = translate("Press CTRL+S for Training the soldier", lang)
	while True:
		try:
			screen_root.draw_all((0, 0, 0))
			root.upload_image(screen_root.mouse_position())
			screen_root.load_image("map_for_now", "data/Singleplayer/map_for_now.jpg", width=screen_root.width, height=screen_root.height)
			screen_root.draw_image("map_for_now")
			try:
				if keyboard.is_pressed("esc"):
					settings()
			except:
				pass
			try:
				if keyboard.is_pressed("tab"):
					yyy = 0
					for user, _ in root.users.items():
						screen_root.draw_text(text=user, x=screen_root.width/2, y=yyy, width=30, height=30, color=(0, 0, 0))
						yyy += 20
			except:
				pass
			try:
				for user, data in root.users.items():
					lander = None
					for land in data["lands"]:
						if lander == None:
							lander = land
						lander = ((lander[0]+land[0])/2, (lander[1]+land[1])/2)
					if lander != None:
						x = lander[0]
						x = (root.screen_width/root.width)*x
						y = lander[1]
						y = (root.screen_height/root.height)*y
						size = min(int(len(data["lands"])/32), 32)
						if size >= 1:
							screen_root.draw_text(text=user, x=x-(size), y=y-(size/2), color=(0, 0, 0), width=size, height=size)
			except:
				pass
			events = screen_root.events()
			if username not in root.users:
				screen_root.draw_text(text=startgame, color=(0, 0, 0))
				for pos, _ in screen_root.events_checkmouse(events):
					play_click()
					try:
						x, y = root.real_position(pos[0], pos[1])
						root.new_user(username, password, x, y)
					except Exception as e:
						pass
			else:
				screen_root.draw_image(x=0, y=0, imagename="ongame_bg")
				screen_root.draw_text(text=usernametext, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=f"{sourcetext}: {root.users[username]['source']}", y=32, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=f"{populationtext}: {root.users[username]['population']}", y=64, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=f"{soldierstext}: {root.users[username]['soldiers']}", y=64+32, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=trainsoldiertext, y=128, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=ctrlstext, y=128+32, color=(0, 0, 0), width=32, height=32)
				try:
					if keyboard.is_pressed("ctrl+s"):
						root.new_soldier(username, password)
						screen_root.draw_text(text=trainsoldiertext, y=128, color=(255, 255, 0), width=0)
				except:
					pass
				for pos, _ in screen_root.events_checkmouse(events):
					play_click()
					if pos[0] >= 0:
						if pos[0] <= len(trainsoldiertext)*32:
							if pos[1] >= 128:
								if pos[1] <= 128+32:
									root.new_soldier(username, password)
									screen_root.draw_text(text=trainsoldiertext, y=128, color=(255, 255, 0), width=0)
					try:
						x, y = root.real_position(pos[0], pos[1])
						root.attack(username, password, x, y)
					except Exception as e:
						pass
				if screen_root.events_checkquit(events):
					root.save()
					break
			screen_root.update()
			root.check_all()
			root.save()
			time.sleep(1/70)
		except Exception as e:
			try:
				screen_root.load_image("map_for_now", "data/Singleplayer/map_for_now.jpg", width=screen_root.width, height=screen_root.height)
				screen_root.draw_image("map_for_now")
			except:
				pass
			print(str(e));screen_root.events();screen_root.update()
def edit_gui(file, text):
	global screen_root
	chars = "qwertyuiopasdfghjklzxcvbnm1234567890!?., "
	lastchar_i = time.time();time.sleep(0.1)
	while True:
		for char in chars:
			try:
				if keyboard.is_pressed(char):
					if time.time()-lastchar_i >= 1/18:
						lastchar_i = time.time()
						text += char;play_click()
			except:
				pass
		screen_root.draw_cube(y=screen_root.height-70, width=screen_root.width, height=70, color=(0, 0, 0))
		screen_root.draw_text(y=screen_root.height-64, width=64, height=64, color=(255, 255, 255), text="Enter: "+text)
		screen_root.update()
		events = screen_root.events()
		if screen_root.events_checkquit(events):
			with open(file, "w") as f:
				f.write(text)
			return text
		try:
			if keyboard.is_pressed("backspace"):
				text = text[:-1]
		except:
			pass
		try:
			if keyboard.is_pressed("enter"):
				with open(file, "w") as f:
					f.write(text)
				return text
		except:
			pass
		time.sleep(1/20)
def randomusername():
	username = ""
	for _ in range(random.randint(1, 2)):
		username += random.choice(english_words).lower()
	return (username+str(random.randint(0, 900)))[:16]
def randompassword():
	password = ""
	for _ in range(random.randint(10, 32)):
		password += random.choice(list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890()<>[]{}/!?;:.,_+-*"))
	return password
def multiplayer():
	global screen_root, map_image, lang
	loading_screen()
	root = CivilArk_Global(map_image, screen_root.width, screen_root.height)
	if not os.path.exists("data/Multiplayer/player_account.txt"):
		with open("data/Multiplayer/player_account.txt", "w") as f:
			username = randomusername()
			password = randompassword()
			f.write(f"USERNAME: {username}\nPASSWORD: {password}")
	else:
		with open("data/Multiplayer/player_account.txt", "r") as f:
			data = f.read().split("\n")
		username = data[0][data[0].find("USERNAME: ")+10:]
		password = data[1][data[1].find("PASSWORD: ")+10:]
	try:
		root.load()
	except:
		pass
	usernametext = translate("Username: ", lang)+username
	startgame = translate("Select a land for start the game.", lang)
	sourcetext = translate("Source", lang)
	populationtext = translate("Population", lang)
	soldierstext = translate("Soldiers", lang)
	trainsoldiertext = translate("[ Train the Soldier ]", lang)
	ctrlstext = translate("Press CTRL+S for Training the soldier", lang)
	ctrlttext = translate("Press CTRL+T for Show message", lang)
	n = time.time()
	while True:
		if time.time()-n >= 0.5:
			try:
				threading.Thread(target=root.load).start()
			except:
				pass
			n = time.time()
		try:
			screen_root.draw_all((0, 0, 0))
			root.upload_image(screen_root.mouse_position())
			screen_root.load_image("map_for_now", "data/Multiplayer/map_for_now.jpg", width=screen_root.width, height=screen_root.height)
			screen_root.draw_image("map_for_now")
			try:
				if keyboard.is_pressed("esc"):
					settings()
			except:
				pass
			try:
				if keyboard.is_pressed("tab"):
					yyy = 0
					for user, _ in root.users.items():
						screen_root.draw_text(text=user, x=screen_root.width/2, y=yyy, width=30, height=30, color=(0, 0, 0))
						yyy += 20
			except:
				pass
			try:
				for user, data in root.users.items():
					lander = None
					for land in data["lands"]:
						if lander == None:
							lander = land
						lander = ((lander[0]+land[0])/2, (lander[1]+land[1])/2)
					if lander != None:
						x = lander[0]
						x = (root.screen_width/root.width)*x
						y = lander[1]
						y = (root.screen_height/root.height)*y
						size = min(int(len(data["lands"])/32), 32)
						if size >= 1:
							screen_root.draw_text(text=user, x=x-(size), y=y-(size/2), color=(0, 0, 0), width=size, height=size)
			except:
				pass
			try:
				for x, y, text, _ in root.texts:
					x = (root.screen_width/root.width)*x
					y = (root.screen_height/root.height)*y
					screen_root.draw_text(text=text, x=x-32, y=y, color=(0, 0, 0), width=32, height=32)
			except Exception as e:
				print(e)
			events = screen_root.events()
			if username not in root.users:
				screen_root.draw_text(text=startgame, color=(0, 0, 0))
				for pos, _ in screen_root.events_checkmouse(events):
					play_click()
					try:
						x, y = root.real_position(pos[0], pos[1])
						root.new_user(username, password, x, y)
					except Exception as e:
						pass
			else:
				screen_root.draw_image(x=0, y=0, imagename="ongame_bg")
				screen_root.draw_text(text=usernametext, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=f"{sourcetext}: {root.users[username]['source']}", y=32, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=f"{populationtext}: {root.users[username]['population']}", y=64, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=f"{soldierstext}: {root.users[username]['soldiers']}", y=64+32, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=trainsoldiertext, y=128, color=(255, 255, 255), width=0)
				screen_root.draw_text(text=ctrlstext, y=128+32, color=(0, 0, 0), width=32, height=32)
				screen_root.draw_text(text=ctrlttext, y=128+64, color=(0, 0, 0), width=32, height=32)
				try:
					if keyboard.is_pressed("ctrl+s"):
						threading.Thread(target=root.new_soldier, args=(username, password)).start()
						screen_root.draw_text(text=trainsoldiertext, y=128, color=(255, 255, 0), width=0)
				except:
					pass
				try:
					if keyboard.is_pressed("ctrl+t"):
						edit_gui("data/Detail/your_message.txt", open("data/Detail/your_message.txt").read())
						threading.Thread(target=root.new_text, args=(username, password)).start()
				except Exception as e:
					print(e)
				for pos, _ in screen_root.events_checkmouse(events):
					play_click()
					if pos[0] >= 0:
						if pos[0] <= len(trainsoldiertext)*32:
							if pos[1] >= 128:
								if pos[1] <= 128+32:
									threading.Thread(target=root.new_soldier, args=(username, password)).start()
									screen_root.draw_text(text=trainsoldiertext, y=128, color=(255, 255, 0), width=0)
					try:
						x, y = root.real_position(pos[0], pos[1])
						threading.Thread(target=root.attack, args=(username, password, x, y)).start()
					except Exception as e:
						pass
				if screen_root.events_checkquit(events):
					break
			screen_root.update()
			time.sleep(1/70)
		except Exception as e:
			print(str(e));screen_root.events();screen_root.update()

def exit():
	psutil.Process(os.getpid()).kill()
	sys.exit()
def main_menu():
	global screen_root, lang
	loading_screen()
	buttons = [["Singleplayer", singleplayer], ["Multiplayer", multiplayer], ["Settings", settings], ["Creators", credits], ["Exit", exit]]
	textsize = int(((screen_root.width/4)+(screen_root.height/20))/10)
	textcolor = (255, 255, 255)
	while True:
		screen_root.draw_all((0, 0, 0))
		screen_root.draw_image(x=0, y=0, imagename="map")
		screen_root.draw_image(x=0, y=0, imagename="menu_bg")
		screen_root.draw_image(x=0, y=0, imagename="menu_civilark")
		x = screen_root.width/20
		y = screen_root.height/4.5
		for title, command in buttons:
			title = translate(title, lang)
			button_start_x = x
			button_start_y = y
			button_end_x = x+(screen_root.width/5)
			button_end_y = y+(screen_root.height/20)
			screen_root.draw_image(x=x, y=y, imagename="button")
			screen_root.draw_text(x=x+(textsize*1.2), y=y+(textsize/10), text=title, width=textsize, height=textsize, color=textcolor)
			y += (screen_root.height/10)
		x = screen_root.width/20
		y = screen_root.height/4.5
		eventsq = screen_root.events()
		events = screen_root.events_checkmouse(eventsq)
		for title, command in buttons:
			title = translate(title, lang)
			button_start_x = x
			button_start_y = y
			button_end_x = x+(screen_root.width/5)
			button_end_y = y+(screen_root.height/20)
			for pos, _ in events:
				print(pos)
				if pos[0] >= button_start_x:
					if pos[0] <= button_end_x:
						if pos[1] >= button_start_y:
							if pos[1] <= button_end_y:
								play_click()
								screen_root.draw_text(x=x+(textsize*1.2), y=y+(textsize/10), text=title, width=textsize, height=textsize, color=(255, 255, 0))
								screen_root.update()
								time.sleep(0.15)
								screen_root.events()
								command()
			y += (screen_root.height/10)
		if screen_root.events_checkquit(eventsq):
			exit()
		screen_root.update()
		time.sleep(1/60)

class CivilArk_Local:
	def __init__(self, image, screen_width, screen_height):
		self.map = Image.open(image)
		self.width = self.map.width
		self.height = self.map.height
		self.users = {}
		self.bots = []
		self.screen_width = screen_width
		self.screen_height = screen_height
	def load(self):
		if os.path.exists("data/Singleplayer/data.json"):
			with open("data/Singleplayer/data.json", "r") as f:
				data = json.loads(f.read())
				self.users = data["users"]
				self.bots = data["bots"]
	def save(self):
		with open("data/Singleplayer/data.json", "w") as f:
			f.write(json.dumps({"users": self.users, "bots": self.bots}))
	def upload_image(self, pos):
		image = self.map.copy()
		dataimage = image.load()
		for user, data in self.users.items():
			value = 0
			for h in user:
				value += ((ord(h)**2)+value)/2
			r = int(value*7373)%256
			g = int(value*7286)%256
			b = int(value*8193)%256
			color = (r, g, b)
			for x, y in data["lands"]:
				dataimage[x, y] = color
		x, y = self.real_position(pos[0], pos[1])
		x = int(x)
		y = int(y)
		dataimage[x, y] = (0, 0, 0)
		for h in range(-3, 4):
			dataimage[x+h, y] = (64, 0, 0)
			dataimage[x, y+h] = (64, 0, 0)
		image.save("data/Singleplayer/map_for_now.jpg", format="JPEG", quality=100)
	def check_is_legal_land(self, x, y):
		image_data = self.map.load()
		try:
			color = image_data[x, y]
			r = abs(color[0]-255)
			g = abs(color[1]-255)
			b = abs(color[2]-255)
			if r+g+b <= 30:
				return True
			else:
				return False
		except:
			return False
	def legal_lander(self, user):
		legal = []
		lands = self.users[user]["lands"]
		for xx, yy in lands:
			legal.append([xx+1, yy])
			legal.append([xx, yy+1])
			legal.append([xx+1, yy+1])
			legal.append([xx-1, yy])
			legal.append([xx, yy-1])
			legal.append([xx-1, yy-1])
			legal.append([xx+1, yy-1])
			legal.append([xx-1, yy+1])
		return legal
	def check_is_legal_target_land(self, user, key, x, y):
		legal = []
		lands = self.users[user]["lands"]
		for xx, yy in lands:
			legal.append([xx+1, yy])
			legal.append([xx, yy+1])
			legal.append([xx+1, yy+1])
			legal.append([xx-1, yy])
			legal.append([xx, yy-1])
			legal.append([xx-1, yy-1])
			legal.append([xx+1, yy-1])
			legal.append([xx-1, yy+1])
		if [x, y] in legal:
			return True
		else:
			raise SystemError("This land not legal to attack.")
	def check_is_have_host(self, x, y):
		for username, data in self.users.items():
			if [x, y] in data["lands"]:
				return username
		return None
	def real_position(self, x, y):
		width_real = (self.width/self.screen_width)*x
		height_real = (self.height/self.screen_height)*y
		return int(width_real), int(height_real)
	def new_user(self, user, key, start_x, start_y):
		if self.check_is_legal_land(start_x, start_y):
			if user not in self.users:
				host = self.check_is_have_host(start_x, start_y)
				if host != None:
					data = self.users[host]
					data["lands"].remove([start_x, start_y])
					self.users[host] = data
				self.users[user] = {"lands": [[start_x, start_y]], "key": key, "population": 1, "soldiers": 1, "source": 10, "last_mine": time.time(), "last_popup": time.time()}
			else:
				raise SystemError("User using now.")
		else:
			raise SystemError("Please select a 'land'.")
	def login(self, user, key):
		if user in self.users:
			if self.users[user]["key"] == key:
				return True
			else:
				raise SystemError("Invalid key.")
		else:
			raise SystemError("Not found user.")
	def attack(self, user, key, x, y):
		if self.check_is_legal_land(x, y):
			self.login(user, key)
			if self.check_is_legal_target_land(user, key, x, y):
				host = self.check_is_have_host(x, y)
				if host == None:
					data = self.users[user]
					if data["source"] >= 1 and data["soldiers"] >= 1 and [x, y] not in data["lands"]:
						data["source"] -= 1
						data["soldiers"] -= 1
						data["lands"].append([x, y])
						self.users[user] = data
				elif host != user:
					data = self.users[user]
					hostdata = self.users[host]
					if data["soldiers"] < hostdata["soldiers"]:
						hostdata["soldiers"] -= data["soldiers"]
						data["soldiers"] = 0
						self.users[host] = hostdata
						self.users[user] = data
					else:
						data["soldiers"] -= hostdata["soldiers"]
						hostdata["soldiers"] = 0
						hostdata["lands"].remove([x, y])
						data["lands"].append([x, y])
						self.users[host] = hostdata
						self.users[user] = data
		else:
			raise SystemError("Please select a 'land'.")
	def check(self, user, key):
		self.login(user, key)
		data = self.users[user]
		miner = time.time()-data["last_mine"]
		miner_int = int(miner/60)
		last_miner = miner-miner_int
		data["last_mine"] = time.time()-last_miner
		data["source"] += (len(data["lands"]))*miner_int
		popuper = time.time()-data["last_popup"]
		popuper_int = int(popuper/30)
		last_popuper = popuper-popuper_int
		data["last_popup"] = time.time()-last_popuper
		data["population"] += popuper_int
		self.users[user] = data
	def new_soldier(self, user, key):
		self.login(user, key)
		data = self.users[user]
		if data["population"] >= 1 and data["source"] >= 1:
			data["population"] -= 1
			data["source"] -= 1
			data["soldiers"] += 1
	def new_bot(self):
		while True:
			name = ""
			for _ in range(random.randint(1, 4)):
				name += random.choice(list("qwrtypsdfgjklhzxcvbnm"))+random.choice(list("euioa"))
			name = name[0].upper()+name[1:]
			if name not in self.users:
				break
		password = str(random.randint(1, 100000000000000000000000))
		self.bots.append(name)
		while True:
			try:
				self.new_user(name, password, random.randint(0, self.width), random.randint(0, self.height))
				break
			except Exception as e:
				print(e)
	def check_all(self):
		for user, data in list(self.users.items()).copy():
			self.check(user, data["key"])
			if user in self.bots:
				while True:
					try:
						x, y = random.choice(self.legal_lander(user))
						self.attack(user, data["key"], x, y)
						break
					except Exception as e:
						print(e)
					
				self.new_soldier(user, data["key"])
			if len(data["lands"]) <= 0:
				del self.users[user]
				try:
					self.bots.remove(user)
				except:
					pass

class CivilArk_Global:
	def __init__(self, image, screen_width, screen_height):
		self.map = Image.open(image)
		self.width = self.map.width
		self.height = self.map.height
		self.users = {}
		self.bots = []
		self.screen_width = screen_width
		self.screen_height = screen_height
		with open("data/Multiplayer/target_server.txt") as f:
			self.server = f.read()
	def request(self, path, data):
		try:
			return requests.request("CIVILARK", self.server+path, json=data, timeout=5).json()
		except Exception as e:
			print(e)
			return {"result": str(e)}
	def load(self):
		data = self.request("/get", {})
		self.users = data["users"]
		self.bots = data["bots"]
		self.texts = data["texts"]
	def save(self):
		pass
	def upload_image(self, pos):
		image = self.map.copy()
		dataimage = image.load()
		for user, data in self.users.items():
			value = 0
			for h in user:
				value += ((ord(h)**2)+value)/2
			r = int(value*7373)%256
			g = int(value*7286)%256
			b = int(value*8193)%256
			color = (r, g, b)
			for x, y in data["lands"]:
				dataimage[x, y] = color
		x, y = self.real_position(pos[0], pos[1])
		x = int(x)
		y = int(y)
		dataimage[x, y] = (0, 0, 0)
		image.save("data/Multiplayer/map_for_now.jpg", format="JPEG", quality=100)
	def check_is_legal_land(self, x, y):
		return self.request("/check_is_legal_land", {"x": x, "y": y})["result"]
	def legal_lander(self, user):
		return self.request("/legal_lander", {"user": user})["result"]
	def check_is_legal_target_land(self, user, key, x, y):
		return self.request("/check_is_legal_target_land", {"user": user, "key": key, "x": x, "y": y})["result"]
	def check_is_have_host(self, x, y):
		return self.request("/check_is_have_host", {"x": x, "y": y})["result"]
	def real_position(self, x, y):
		width_real = (self.width/self.screen_width)*x
		height_real = (self.height/self.screen_height)*y
		return int(width_real), int(height_real)
	def new_user(self, user, key, start_x, start_y):
		return self.request("/new_user", {"user": user, "key": key, "start_x": start_x, "start_y": start_y})["result"]
	def login(self, user, key):
		return self.request("/login", {"user": user, "key": key})["result"]
	def attack(self, user, key, x, y):
		return self.request("/attack", {"user": user, "key": key, "x": x, "y": y})["result"]
	def check(self, user, key):
		return self.request("/check", {"user": user, "key": key})["result"]
	def new_soldier(self, user, key):
		return self.request("/new_soldier", {"user": user, "key": key})["result"]
	def new_bot(self):
		pass
	def new_text(self, user, key):
		try:
			with open("data/Detail/your_message.txt", "r", encoding="utf-8") as f:
				self.request("/new_text", {"user": user, "key": key, "text": f.read()})
		except Exception as e:
			print(e)
	def check_all(self):
		return self.request("/check_all", {})
print(randomusername())
print(randompassword())
threading.Thread(target=play_background_auto_thread).start()
opening_screen()
main_menu()