# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.server.util.flask import restricted_access
from octoprint.server import admin_permission
from octoprint.plugin import BlueprintPlugin

import requests
import xmltodict

class FlashSailfishPlugin(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.AssetPlugin,
                          octoprint.plugin.TemplatePlugin,
						  octoprint.plugin.BlueprintPlugin):

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			url="http://jettyfirmware.yolasite.com/resources/release/firmware.xml"
		)

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
				repo="octoflashsailfish",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/markwal/octoflashsailfish/archive/{target_version}.zip"
			)
		)

	##~~ Blueprint mixin
	@BlueprintPlugin.route("/firmware_file", methods=["POST"])
	@restricted_access
	@admin_permission.require(403)
	def firmware_file(self):
		pass

	@BlueprintPlugin.route("/refresh_firmware_info", method=["POST"])
	@restricted_access
	@admin_permission.require(403)
	def refresh_firmware_info(self):
		pass

	##~~ internal
	def _fetch_firmware_info(self):
		try:
			self.xml = requests.get(self._settings.url)
		except:
			return make_response("Unable to retrieve firmware information from {0}".format(self._settings.url), 400)
		try:
			self.firmware_info = xmltodict.parse(self.xml)
		except:
			return make_response("Retrieved firmware information from {0}, but was unable to understand the response.".format(self._settings.url), 400)


__plugin_name__ = "Flash Sailfish"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = FlashSailfishPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

