import shlex
import subprocess
import datetime
import random
import glob
import json
import sys
import os
import time
from easyprocess import Proc
from threading import Timer

class EntryMusic:
	
	def __init__(self):	    

		self.config = self.load_json('config.json')

		if not 'song_timeout_secs' in self.config:
			sys.exit("song_timeout_secs not set in config")

		if not 'away_timeout_mins' in self.config:
			sys.exit("away_timeout_mins not set in config")

		self.users = self.load_json('users.json')
		self.start_time = datetime.datetime.now()	    

		sys.stdout.flush()
		self.update_console_status() 		
		self.run_loop()	    	

	def audio_player_name(self):
		for name in ['mplayer', 'omxplayer', 'afplay']:
			if self.program_exists(name):
				return name

		sys.exit('No audio player found. We recommend installing mplayer')

	def text_to_speech_name(self):
		for name in ['say', 'espeak']:
			if self.program_exists(name):
				return name

		return False

	@staticmethod
	def program_exists(name):
		try:
			subprocess.check_output("which {0}".format(name), shell=True)
			return True
		except:
			#print "ERROR: {0} Not found".format(name)
			return False

	def load_json(self, file_name):
		json_data=open(file_name)	
		data = json.load(json_data)
		return data

	def greet(user):

		program_name = self.text_to_speech_name()
		if not program_name:
			return False

		if (self.program_exists('say')):
			cmd=shlex.split("{0} \"{1} has entered the building\"".format(program_name, user['name']))
			stdout=Proc(cmd).call(timeout=10).stdout
		

	@staticmethod
	def log(message):
		#print message
		pass	

	def song_for_user(self, user):
		directory="themes/{0}".format(user['name'])
		onlyfiles=glob.glob("{0}/*.*".format(directory))
		if len(onlyfiles)==0:
			return False

		random_index=random.randint(0, len(onlyfiles) - 1)
		return onlyfiles[random_index]	

	def play_song(self, user):	
		
		print "\n\rplay song for {0}".format(user['name'])	
		file_to_play = self.song_for_user(user)
		if not file_to_play:
			return False #greet(user)

		audio_player = self.audio_player_name()
		cmd_string = "{0} \"{1}\"".format(audio_player, file_to_play)
		print cmd_string
		cmd=shlex.split(cmd_string)		

		proc = Process_runner(cmd_string, self.config['song_timeout_secs'])	
		#stdout=Proc(cmd).call(timeout=15).stdout

		#player = subprocess.Popen([audio_player, "-o", "local", file_to_play], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#time.sleep(self.config['song_timeout'])		
		#player.stdin.write("\x03");
		#player.stdin.write("q")
		
		#stdout=Proc(cmd).call(timeout=10).stdout
		#stdout=Proc(["/usr/bin/omxplayer", "-o", "local", file_to_play]).call(timeout=10).stdout	

	@staticmethod
	def green(msg):
		return "\033[92m{0}\033[0m".format(msg)

	@staticmethod
	def red(msg):
		return "\033[91m{0}\033[0m".format(msg)

	def update_console_status(self):
		os.system('clear')
		sys.stdout.flush()
		string=""
		for user in self.users:							
			last_seen = user['last_seen'] if 'last_seen' in user else "Never seen"
			confirmed_not_there = user['confirmed_not_there'] if 'confirmed_not_there' in user else True
			not_here_string = last_seen if 'confirmed_not_there' in user else "Loading..."
			here_or_not = self.red(not_here_string) if confirmed_not_there  else self.green("Here")
			string="{0}\n\r {1}: {2}".format(string, user['name'], here_or_not)					
		sys.stdout.write("\r{0}".format(string))
		sys.stdout.flush()


	def should_play_song(self, user):
		# If we haven't confirmed they aren't there, then don't play
		if not user['confirmed_not_there']:
			self.log("{0} was not confirmed to not be there".format(user['name']))
			return False

		# If we have confirmed they were previously not there and last_seen isn't set then play
		if not 'last_seen' in user:
			# Did we just restart the script?		
			five_mins_ago=datetime.datetime.now() - datetime.timedelta(minutes=5)
			if five_mins_ago > self.start_time:
				return True
			else:
				self.log("{0} was never seen but we just restarted the script".format(user['name']))
				return False

		# if last seen is set and it's older than 15 mins return true
		time_ago=self.config['away_timeout_mins']
		distant_time=datetime.datetime.now() - datetime.timedelta(minutes=time_ago)
		if user['last_seen'] < distant_time:
			self.log("{0} was last seen more than {1} mins ago".format(user['name'], time_ago))
			return True
		else:
			# otherwise dont play
			self.log("Dont play for {0} delta was lest than 1 min {1} - {2}".format(user['name'], user['last_seen'], distant_time))
			return False	

	def run_loop(self):
		while 1:
			for user in self.users:

				if not 'confirmed_not_there' in user:
					user['confirmed_not_there'] = False

				try:
					cmd=shlex.split("ping {0}".format(user['ip']))
					# subprocess.check_output(cmd)
					stdout=Proc(cmd).call(timeout=1.8).stdout	    	

					if "bytes from" in stdout:						
						if self.should_play_song(user):
							self.play_song(user)							
						self.log("User: {0} is Reachable. {1}".format(user['name'], user['ip']))
						user['last_seen'] = datetime.datetime.now()
						user['confirmed_not_there'] = False
					else:
						user['confirmed_not_there'] = True
						last_seen = user['last_seen'] if 'last_seen' in user else "never"
						self.log("User: {0} is NotReachable. last seen: {1}".format(user['name'], last_seen))
					self.update_console_status()
					
				except subprocess.CalledProcessError,e:
				   print "ERROR {0}".format(e)
				else:
				   pass
			
class Process_runner:
	def __init__(self, cmd, timeout):
		self.run(cmd, timeout)

	@staticmethod
	def kill_proc(proc, timeout):
		timeout["value"] = True
		proc.kill()

	def run(self, cmd, timeout_sec):
		proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		timeout = {"value": False}
		timer = Timer(timeout_sec, self.kill_proc, [proc, timeout])
		timer.start()
		stdout, stderr = proc.communicate()
		timer.cancel()
		return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), timeout["value"]

entryMusic = EntryMusic()