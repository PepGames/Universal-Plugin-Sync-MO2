from PyQt5.QtGui import QIcon

import mobase

class GamePluginsRequirement(mobase.IPluginRequirement):

    def __init__(self):
        super().__init__()

    def check(self, organizer: mobase.IOrganizer):
        managedGame = organizer.managedGame()
        if (managedGame and not managedGame.feature(mobase.GamePlugins)):
            return mobase.IPluginRequirement.Problem(
                "This plugin can only be enabled for games with plugins.")

        return None

class PluginSync(mobase.IPluginTool):

    _organizer: mobase.IOrganizer
    _modList: mobase.IModList
    _pluginList: mobase.IPluginList

    def __init__(self):
        super().__init__()

    def init(self, organizer: mobase.IOrganizer):
        self._organizer = organizer
        self._modList = organizer.modList()
        self._pluginList = organizer.pluginList()
        return True

    def name(self):
        return "Sync Plugins (Universal)"

    def author(self):
        return "coldrifting & SuperPep"

    def description(self):
        return "Syncs plugin load order with mod order"

    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.FINAL)

    def isActive(self):
        return (self._organizer.managedGame().feature(mobase.GamePlugins))

    def settings(self):
        return []

    def display(self):
        # Get all plugins as a list
        allPlugins = self._pluginList.pluginNames()

        # Sort the list by plugin origin
        allPlugins = sorted(
            allPlugins,
            key=lambda
            plugin: self._modList.priority(self._pluginList.origin(plugin))
        )


        # Set load order
        self._pluginList.setLoadOrder(allPlugins)

        # Update the plugin list to use the new load order
        self._organizer.managedGame().feature(
            mobase.GamePlugins).writePluginLists(self._pluginList)

        # Refresh the UI
        self._organizer.refresh()

        return True

    def displayName(self):
        return "Sync Plugins (Universal)"

    def tooltip(self):
        return "Enables all Mods one at a time to match load order"

    def icon(self):
        return QIcon()

    def requirements(self):
        return [GamePluginsRequirement()]


def createPlugin() -> mobase.IPluginTool:
    return PluginSync()
