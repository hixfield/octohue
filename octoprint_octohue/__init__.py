# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class OctoHuePlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):
	def on_after_startup(self):
		self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

	def get_settings_defaults(self):
		return dict(url="https://snookercoaches.com")

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def get_assets(self):
		return dict(
			js=["js/octohue.js"],
			css=["css/octohue.css"],
			less=["less/octohue.less"]
		)

__plugin_name__ = "OctoHue"
__plugin_implementation__ = OctoHuePlugin()
