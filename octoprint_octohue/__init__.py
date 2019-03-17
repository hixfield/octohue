# coding=utf-8
from __future__ import absolute_import
from os import path
from qhue import Bridge, QhueException, create_new_username
import yaml

import octoprint.plugin

CRED_FILE_PATH = "qhue_username.txt"


class OctoHuePlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
					   octoprint.plugin.EventHandlerPlugin):

	hueUsername = ""

	def on_after_startup(self):
		self._logger.info("Hue bridge  : %s" % self._settings.get(["hueBridge"]))
		self._logger.info("Hue lamp id : %s" % self._settings.get(["hueLampId"]))
		self.checkHueUserName()

	def get_settings_defaults(self):
		return dict(hueBridge="192.168.99.200", hueLampId="13")

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def on_event(self, event, payload):
		self._logger.info("Event: %s" % event)
		if event == "PrintStarted":
		    self.lampOn(True)
		if event == "PrintDone":
		    self.lampOn(False)
		if event == "PrintFailed":
		    self.lampOn(False)
		if event == "PrintCancelled":
		    self.lampOn(False)			

	def checkHueUserName(self):
		self._logger.info("Checking hue username...")
		if not path.exists(CRED_FILE_PATH):
			while True:
				try:
					self.hueUsername = create_new_username(self._settings.get(["hueBridge"]))
					break
				except QhueException as err:
					self._logger.err("Create username failed: {}".format(err))
			with open(CRED_FILE_PATH, "w") as cred_file:
				cred_file.write(self.hueUsername)
		else:
			with open(CRED_FILE_PATH, "r") as cred_file:
				self.hueUsername = cred_file.read()
		self._logger.info("Hue username : %s" % self.hueUsername)
		
	def lampOn(self, state):
		ip = self._settings.get(["hueBridge"])
		lampId = self._settings.get(["hueLampId"])
		lights = Bridge(ip, self.hueUsername).lights
		#self._logger.info(yaml.safe_dump(lights()))
 		lights(lampId,'state', on=state)

__plugin_name__ = "OctoHue"
__plugin_implementation__ = OctoHuePlugin()
