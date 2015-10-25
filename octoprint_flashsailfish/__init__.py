# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class FlashSailfishPlugin(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.AssetPlugin,
                          octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			url="http://jettyfirmware.yolasite.com/resources/release/firmware.xml"
		)

	#~~ TemplatePlugin mixin
	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	##~~ AssetPlugin mixin
	def get_assets(self):
		return dict(
			js=["js/flashsailfish.js"],
			css=["css/flashsailfish.css"],
			less=["less/flashsailfish.less"]
		)

	##~~ Softwareupdate hook
	def get_update_information(self):
		return dict(
			flashsailfish=dict(
				displayName="Flash Sailfish",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="markwal",
				repo="OctoPrint-FlashSailfish",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/markwal/OctoPrint-FlashSailfish/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Flash Sailfish"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = FlashSailfishPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

