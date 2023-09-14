import re
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
    _pluginGame: mobase.IPluginGame

    def __init__(self):
        super().__init__()

    def init(self, organizer: mobase.IOrganizer):
        self._organizer = organizer
        self._modList = organizer.modList()
        self._pluginList = organizer.pluginList()
        return True
    
   # def init(self, pluginGame: mobase.IPluginGame):
   #     self._pluginGame = pluginGame
  #      self._gameName = pluginGame.gameName()
   #     return True
    
    def name(self):
        return "Sync Plugins (Universal)"

    def author(self):
        return "coldrifting, and SuperPep"

    def description(self):
        return "Syncs plugin load order with mod order"

    def version(self):
        return mobase.VersionInfo(2, 0, 0, mobase.ReleaseType.FINAL)

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
        
        # Split into two lists, master files and regular plugins
        plugins = []
        masters = []
        for plugin in allPlugins:
            if (self._pluginList.isMaster(plugin)):
                masters.append(plugin)
            else:
                plugins.append(plugin)
        
        
        # Sort DLC correctly (Unmanaged Files)
        if (self._gameName == "Skyrim"):
         masters[0] = "Skyrim.esm"
         masters[1] = "Update.esm"
         masters[2] = "Dawnguard.esm"
         masters[3] = "HearthFires.esm"
         masters[4] = "Dragonborn.esm"
        elif (self._gameName == "Morrowind"):
         masters[0] = "Morrowind.esm"
         masters[1] = "Tribunal.esm"
         masters[2] = "Bloodmoon.esm"
        else: []
         

        # Merge masters into the plugin list at the begining
        allPlugins = masters + plugins

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
        return []

    def requirements(self):
        return [GamePluginsRequirement()]


def createPlugin() -> mobase.IPluginTool:
    return PluginSync()
