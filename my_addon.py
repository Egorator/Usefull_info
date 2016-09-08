# copy this file to C:\Users\YOUR_USER_NAME\Documents\Anki\addons

# fill  = ctrl+j
# clear = ctrl+k
# add   = ctrl+enter
# to = ctrl+o

from anki.hooks import wrap
from aqt.editor import Editor
from aqt.utils import showInfo
from aqt.qt import QKeySequence
from anki.utils import json

import os.path

# from subprocess import *
from subprocess import call,check_call

def fill_button_pressed(self):
	# Settings:
	WEB_BROWSER = "C:/Program Files (x86)/Mozilla Firefox/firefox.exe"
	UNZIP = "C:/Program Files/Git/usr/bin/unzip"
	SOUNDS = "D:/GoldenDict/GoldenDict_portable/content/sound_en/sound_en.dsl.files.zip"
	MEDIA = "C:/Users/Egorr/Documents/Anki/User 1/collection.media"
	URL_LIGVO_ONLINE = "http://www.lingvo.ua/ru/Translate/en-ru/"
	URL_GOOGLE_TRANSLATE = "https://translate.google.com/#en/ru/"
	URL_GOOGLE_IMAGE_SEARCH = "https://www.google.com/search?tbm=isch&q="
	# Read english word:
	self.web.eval("focusField(%d);" % 1)
	self.web.eval("focusField(%d);" % 0)
	english_word = self.note.fields[0]
	# Translate english word:
	# check_call(["D:\GoldenDict\GoldenDict_portable\GoldenDict.exe", english_word])
	# os.spawnv(os.P_NOWAIT, WEB_BROWSER, ["-new-tab", URL_LIGVO_ONLINE + english_word])
	os.spawnv(os.P_NOWAIT, WEB_BROWSER, ["-new-tab", URL_GOOGLE_TRANSLATE + english_word])
	# Copy english word to newly created data:
	data = []
	data.append(("english", english_word))
	self.note.fields[0] = english_word
	data.append(("russian", ""))
	self.note.fields[1] = ""
	data.append(("usage_example", ""))
	self.note.fields[2] = ""
	# Add audio if available:
	audio_file = MEDIA + "/" + english_word + ".mp3"
	if os.path.isfile(audio_file):
		ret = 0
	else:
		ret = call([UNZIP, SOUNDS, english_word + ".mp3", "-d", MEDIA])
	if ret == 0:
		audio_field_content = "[sound:" + english_word + ".mp3]"
		os.chdir("D:/GoldenDict/mpg123-1.23.4-x86-64")
		check_call(["mpg123.exe", audio_file])
	else:
		audio_field_content = ""
		showInfo("No audio found")
	data.append(("audio", audio_field_content))
	self.note.fields[3] = audio_field_content
	# Search for images:
	os.spawnv(os.P_NOWAIT, WEB_BROWSER, ["-new-tab", URL_GOOGLE_IMAGE_SEARCH + english_word])
	# Add empty image by now:
	self.note.fields[4] = ""
	data.append(("image", self.note.fields[4]))
	# Refresh all fields:
	self.web.eval("setFields(%s, %d);" % (json.dumps(data), 4)) # 4 = field to place cursor to (image)
	self.web.eval("setFonts(%s);" % (json.dumps(self.fonts())))
	# Set focus on translation:
	self.web.eval("focusField(%d);" % 1)

def setup_my_buttons(self):
	setup_fill_button(self)
	setup_clear_button(self)
	setup_to_button(self)

def setup_fill_button(self):
	# size=False tells Anki not to use a small button
	fill_button = self._addButton("fill_button", lambda s=self: fill_button_pressed(self), text="Fill", size=False)
	fill_shortcut = "Ctrl+j"
	fill_button.setShortcut(QKeySequence(fill_shortcut))
	fill_button.setToolTip("Fill all fields: " + fill_shortcut)

def clear_button_pressed(self):
	data = []
	data.append(("english", ""))
	self.note.fields[0] = ""
	data.append(("russian", ""))
	self.note.fields[1] = ""
	data.append(("usage_example", ""))
	self.note.fields[2] = ""
	data.append(("audio", ""))
	self.note.fields[3] = ""
	data.append(("image", ""))
	self.note.fields[4] = ""
	# Refresh fields:
	self.web.eval("setFields(%s, %d);" % (json.dumps(data), 0)) # 0 = field to place cursor to
	self.web.eval("setFonts(%s);" % (json.dumps(self.fonts())))

def setup_clear_button(self):
	# size=False tells Anki not to use a small button
	clear_button = self._addButton("clear_button", lambda s=self: clear_button_pressed(self), text="Clear", size=False)
	clear_shortcut = "Ctrl+k"
	clear_button.setShortcut(QKeySequence(clear_shortcut))
	clear_button.setToolTip("Clear all fields: " + clear_shortcut)

def to_button_pressed(self):
	showInfo("Not implemented")
	# self.note.fields[0] = "to " + self.note.fields[0]
	# Refresh fields:
	# self.web.eval("setFields(%s, %d);" % (json.dumps(data), 0)) # 0 = field to place cursor to
	# self.web.eval("setFonts(%s);" % (json.dumps(self.fonts())))

def setup_to_button(self):
	to_button = self._addButton("to_button", lambda s=self: to_button_pressed(self), text="to <VERB>", size=False)
	to_shortcut = "Ctrl+o"
	to_button.setShortcut(QKeySequence(to_shortcut))
	to_button.setToolTip("Add \"to \" in front of english word (for verbs): " + to_shortcut)

Editor.setupButtons = wrap(Editor.setupButtons, setup_my_buttons)

