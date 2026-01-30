# Modules
import signal
import random
import time
import os
import threading
import sys, psutil
try:
	os.chdir("CivilArk")
except:
	pass
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
			original = original.resize((width, height))
			surface = self.engineroot.image.fromstring(original.tobytes(), original.size, original.mode)
			surface.set_alpha(alpha)
			surface = self.engineroot.transform.rotate(surface, rotate)
			self.images[imagename] = surface
		else:
			surface = self.engineroot.image.load(image)
			surface = self.engineroot.transform.scale(surface, (width, height))
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
background_musics = ["data/Music/Sg0A3.mp3", "data/Music/Sg0A4.mp3", "data/Music/Sg0A5.mp3"]
background_war_musics = ["data/Music/Sg0A1.mp3"]
background_ending_musics = ["data/Music/Sg0A2.mp3"]
click_sounds = ["click1", "click2", "click3", "click4"]
music_volume = 0.5
soundeffect_volume = 1
background_music_last = 0
on_war = False
on_ending = False

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
	screen_root.load_image("civilark_full", civilark_full, width=screen_root.width/2, height=screen_root.height/4.5)
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
	screen_root.load_image("map", map_image, width=screen_root.width, height=screen_root.height)
except Exception as e:
	print(f"Error on map image loading: {e}")
try:
	screen_root.load_image("button", button_image, width=screen_root.width/5.0, height=screen_root.height/20)
except Exception as e:
	print(f"Error on map image loading: {e}")
for music in background_musics:
	try:
		screen_root.music_load(music, music)
	except Exception as e:
		print(f"Error on {music} loading: {e}")
for music in background_war_musics:
	try:
		screen_root.music_load(music, music)
	except Exception as e:
		print(f"Error on {music} loading: {e}")
for music in background_ending_musics:
	try:
		screen_root.music_load(music, music)
	except Exception as e:
		print(f"Error on {music} loading: {e}")
screen_root.music_manual_load("click1", hz=565, seconds=0.03)
screen_root.music_manual_load("click2", hz=545, seconds=0.04)
screen_root.music_manual_load("click3", hz=575, seconds=0.02)
screen_root.music_manual_load("click4", hz=600, seconds=0.025)

# Main Functions

def play_click():
	global soundeffect_volume, click_sounds, screen_root
	screen_root.music_play(random.choice(click_sounds), volume=soundeffect_volume, channel=random.randint(1, 999))
def play_background_music():
	global screen_root, background_musics, background_music_last
	background_music_last = time.time()
	screen_root.music_play(random.choice(background_musics), volume=music_volume, channel=0)

def play_background_war_music():
	global screen_root, background_war_musics, background_music_last
	background_music_last = time.time()
	screen_root.music_play(random.choice(background_war_musics), volume=music_volume, channel=0)

def play_background_ending_music():
	global screen_root, background_ending_musics, background_music_last
	background_music_last = time.time()
	screen_root.music_play(random.choice(background_ending_musics), volume=music_volume, channel=0)

def play_background_auto_thread():
	global background_music_last, on_war, on_ending
	last_on_war = on_war
	last_on_ending = on_ending
	while True:
		if last_on_war != on_war:
			background_music_last = 0
		if last_on_ending != on_ending:
			background_music_last = 0
		last_on_war = on_war
		last_on_ending = on_ending
		if on_war:
			if time.time()-background_music_last >= 4*60:
				play_background_war_music()
		elif on_ending:
			if time.time()-background_music_last >= (2*60)+40:
				play_background_ending_music()
		else:
			if time.time()-background_music_last >= 4*60:
				play_background_music()
		time.sleep(1)

def opening_screen():
	global screen_root
	for n in range(1, 128):
		screen_root.draw_all((1, 1, 1))
		try:
			screen_root.load_image("syshanbur", syshanbur_logo, width=screen_root.width, height=screen_root.height/1.5, alpha=n)
		except Exception as e:
			print(f"Error on syshanbur logo loading: {e}")
		screen_root.draw_image("syshanbur", x=(screen_root.width/2)-(screen_root.width/2), y=(screen_root.height/2)-(screen_root.height/3))
		screen_root.update()
		time.sleep(0.0005)
		screen_root.events()
	for n in range(0, 128)[::-1]:
		screen_root.draw_all((1, 1, 0))
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
	global screen_root, music_volume, soundeffect_volume
	textsize = 30
	textcolor = (255, 255, 255)
	clickcolor = (255, 255, 0)
	while True:
		screen_root.draw_all((0, 0, 0))
		logox = (screen_root.width/2)-(screen_root.width/4)
		logoy = ((screen_root.height/2)-(screen_root.width/12))/5
		screen_root.draw_image("civilark_full", x=logox, y=logoy)
		screen_root.draw_text(text="Game Settings", x=logox, y=logoy+(screen_root.height/6)+100, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=f"Music Volume: {music_volume*100:.0f}%", x=logox, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=f"+", x=logox+230, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"-", x=logox+250, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"Sound Effect Volume: {soundeffect_volume*100:.0f}%", x=logox, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		screen_root.draw_text(text=f"+", x=logox+300, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"-", x=logox+320, y=logoy+(screen_root.height/6)+190+32, width=textsize, height=textsize, color=textcolor)
		screen_root.draw_text(text=f"[ Exit from settings ]", x=logox, y=logoy+(screen_root.height/6)+270, width=textsize, height=textsize, color=textcolor, font="Font Squirrel")
		events = screen_root.events()
		for pos, _ in screen_root.events_checkmouse(events):
			x = pos[0]
			y = pos[1]
			if x >= logox+230:
				if x <= logox+230+textsize:
					if y >= logoy+(screen_root.height/6)+190:
						if y <= logoy+(screen_root.height/6)+190+(textsize/2):
							play_click()
							music_volume += 0.01
							play_background_music()
							screen_root.draw_text(text=f"+", x=logox+230, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=clickcolor)
							time.sleep(0.01)
			if x >= logox+250:
				if x <= logox+250+textsize:
					if y >= logoy+(screen_root.height/6)+190:
						if y <= logoy+(screen_root.height/6)+190+textsize:
							play_click()
							music_volume -= 0.01
							play_background_music()
							screen_root.draw_text(text=f"-", x=logox+250, y=logoy+(screen_root.height/6)+190, width=textsize, height=textsize, color=clickcolor)
							time.sleep(0.01)
			if x >= logox+300:
				if x <= logox+300+textsize:
					if y >= logoy+(screen_root.height/6)+190+32:
						if y <= logoy+(screen_root.height/6)+190+32+(textsize/2):
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
			if logox <= x <= logox + (textsize * len("[ Exit from settings ]")):
				if logoy + (screen_root.height / 6) + 270 <= y <= logoy + (screen_root.height / 6) + 270 + textsize:
					play_click()
					screen_root.draw_text(text=f"[ Exit from settings ]", x=logox, y=logoy+(screen_root.height/6)+270, width=textsize, height=textsize, color=clickcolor, font="Font Squirrel")
					screen_root.update()
					time.sleep(0.01)
					return
		screen_root.update();time.sleep(1/40)
	screen_root.draw_all((0, 0, 0))
	screen_root.update()

def credits():
	global screen_root, music_volume, soundeffect_volume
	textsize = 50
	textcolor = (255, 255, 255)
	names = ["omurcek_ - Studio Owner", "aertsimon90 - Coder", "kka0023 - Financial Supporter", "denizbt_0 - Design", ]
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
		screen_root.draw_text(text="[ Click and next! ]", x=(screen_root.width/2)-(len(name)*textsize/6), y=screen_root.height/2+(textsize*5), color=textcolor, width=textsize, height=textsize)
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
	pass
def multiplayer():
	pass
def exit():
	psutil.Process(os.getpid()).kill()
	sys.exit()
def main_menu():
	global screen_root
	buttons = [["Singleplayer", singleplayer], ["Multiplayer", multiplayer], ["Settings", settings], ["Credits", credits], ["Exit", exit]]
	textsize = int(((screen_root.width/4)+(screen_root.height/20))/9.7)
	textcolor = (255, 255, 255)
	while True:
		screen_root.draw_all((0, 0, 0))
		screen_root.draw_image(x=0, y=0, imagename="map")
		screen_root.draw_image(x=0, y=0, imagename="menu_bg")
		screen_root.draw_image(x=0, y=0, imagename="menu_civilark")
		x = screen_root.width/20
		y = screen_root.height/4.5
		events = screen_root.events_checkmouse(screen_root.events())
		for title, command in buttons:
			button_start_x = x
			button_start_y = y
			button_end_x = x+(screen_root.width/5)
			button_end_y = y+(screen_root.height/20)
			screen_root.draw_image(x=x, y=y, imagename="button")
			screen_root.draw_text(x=x+(textsize), y=y+(textsize/10), text=title, width=textsize, height=textsize, color=textcolor)
			for pos, _ in events:
				print(pos)
				if pos[0] >= button_start_x:
					if pos[0] <= button_end_x:
						if pos[1] >= button_start_y:
							if pos[1] <= button_end_y:
								play_click()
								screen_root.draw_text(x=x+(textsize), y=y+(textsize/10), text=title, width=textsize, height=textsize, color=(255, 255, 0))
								time.sleep(0.1)
								command()
			y += (screen_root.height/10)
		screen_root.update()
		time.sleep(1/60)

class CivilArk_Local:
	def __init__(self, image, screen_width, screen_height):
		self.map = image.open(image)
		self.width = self.map.width
		self.height = self.map.height
		self.users = {}
		self.screen_width = screen_width
		self.screen_height = screen_height
	def check_is_legal_land(self, x, y):
		image_data = self.map.load()
		try:
			if image_data[x, y] != (0, 0, 0) and image_data[x, y] != (176, 244, 255):
				return True
			else:
				return False
		except:
			return False
	def check_is_have_host(self, x, y):
		for username, data in self.users.items():
			if [x, y] in data["lands"]:
				return username
		return None
	def real_position(self, x, y):
		width_real = (self.width/self.screen_width)*x
		height_real = (self.height/self.screen_height)*y
		return width_real, height_real
	def new_user(self, user, key, start_x, start_y):
		if self.check_is_legal_land(start_x, start_y):
			if user not in self.users:
				host = self.check_is_have_host(start_x, start_y)
				if host != None:
					data = self.users[host]
					data["lands"].remove([start_x, start_y])
					self.users[host] = data
				self.users[user] = {"lands": [[start_x, start_y]], "key": key, "population": 10, "soldiers": 10, "source": 10, "last_mine": 0, "last_popup": time.time()}
			else:
				raise SystemError("User using now.")
		else:
			raise SystemError("Please select a 'land'.")

threading.Thread(target=play_background_auto_thread).start()
main_menu()