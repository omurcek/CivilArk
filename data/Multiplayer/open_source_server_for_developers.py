from flask import Flask, request
import os, json, random, time
from PIL import Image

class CivilArk_Local_Server:
	def __init__(self, image):
		self.map = Image.open(image)
		self.width = self.map.width
		self.height = self.map.height
		self.users = {}
		self.bots = []
	def load(self):
		if os.path.exists("data.json"):
			with open("data.json", "r") as f:
				data = json.loads(f.read())
				self.users = data["users"]
				self.bots = data["bots"]
	def save(self):
		with open("data.json", "w") as f:
			f.write(json.dumps({"users": self.users, "bots": self.bots}))
	def get(self):
		users = {};self.check_all()
		for user, data in list(self.users.items()).copy(): 
			dataa = data.copy()
			dataa["key"] = "Github_aertsimon90_FollowMeHacker!"
			users[user] = dataa
		return json.dumps({"users": users, "bots": self.bots})
	def check_is_legal_land(self, x, y):
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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
	def real_position(self, x, y, screen_width, screen_height):
		width_real = (self.width/screen_width)*x
		height_real = (self.height/screen_height)*y
		return int(width_real), int(height_real)
	def new_user(self, user, key, start_x, start_y):
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
		if user in self.users:
			if self.users[user]["key"] == key:
				return True
			else:
				raise SystemError("Invalid key.")
		else:
			raise SystemError("Not found user.")
	def attack(self, user, key, x, y):
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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
		try:
			user = user[:16]
		except:
			pass
		try:
			key = key[:32]
		except:
			pass
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

root = CivilArk_Local_Server("civilark_map.jpg")
root.load()
app = Flask(__name__)

@app.route("/get", methods=["CIVILARK"])
def get_data():
	global root
	root.save()
	return root.get()

@app.route("/check_is_legal_land", methods=["CIVILARK"])
def check_is_legal_land_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.check_is_legal_land(data["x"], data["y"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/legal_lander", methods=["CIVILARK"])
def legal_lander_api():
	global root
	data = request.get_json()
	return json.dumps({"result": root.legal_lander(data["user"])})

@app.route("/check_is_legal_target_land", methods=["CIVILARK"])
def check_is_legal_target_land_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.check_is_legal_target_land(data["user"], data["key"], data["x"], data["y"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/check_is_have_host", methods=["CIVILARK"])
def check_is_have_host_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.check_is_have_host(data["x"], data["y"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/real_position", methods=["CIVILARK"])
def real_position_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.real_position(data["x"], data["y"], data["screen_width"], data["screen_height"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/new_user", methods=["CIVILARK"])
def new_user_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.new_user(data["user"], data["key"], data["start_x"], data["start_y"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/login", methods=["CIVILARK"])
def login_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.login(data["user"], data["key"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/attack", methods=["CIVILARK"])
def attack_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.attack(data["user"], data["key"], data["x"], data["y"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/check", methods=["CIVILARK"])
def check_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.check(data["user"], data["key"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/new_soldier", methods=["CIVILARK"])
def new_soldier_api():
	global root
	try:
		data = request.get_json()
		return json.dumps({"result": root.new_soldier(data["user"], data["key"])})
	except Exception as e:
		return json.dumps({"result": str(e)})

@app.route("/check_all", methods=["CIVILARK"])
def check_all_api():
	global root
	try:
		root.check_all()
		root.save()
		return ""
	except Exception as e:
		return ""

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")