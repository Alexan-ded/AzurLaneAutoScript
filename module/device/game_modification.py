import subprocess

from module.handler.login import LoginHandler
from module.logger import logger


class GameModification:
    def __init__(self, config, device):
        self.config = config
        self.device = device

    def change_game_state(self, state):
        subprocess.Popen(
            [
                "adb",
                "shell",
                f"cp /storage/emulated/0/Documents/{state}/Perseus.ini /storage/emulated/0/Android/data/com.YoStarEN.AzurLane/files/",
            ]
        )
        logger.hr("App restart")
        self.device.app_stop()
        self.device.app_start()
        LoginHandler(config=self.config, device=self.device).handle_app_login()

    def ensure_game_state(self, expected_state):
        VANILLA_FALSE_COUNT = "43"
        HACK_FALSE_COUNT = "12"
        process = subprocess.Popen(
            [
                "adb",
                "shell",
                "grep -o false /storage/emulated/0/Android/data/com.YoStarEN.AzurLane/files/Perseus.ini | wc -l",
            ],
            stdout=subprocess.PIPE,
        )
        output, _ = process.communicate()
        false_count = output.decode().strip()
        if expected_state == "vanilla" and false_count == HACK_FALSE_COUNT:
            logger.critical("YOU ARE FUCKED")
            handle_notify(
                self.config.Error_OnePushConfig,
                title=f"Alas <{self.config_name}> crashed",
                content=f"<{self.config_name}> Trying to run Exercise with hacks",
            )
            exit(1)
        if expected_state == "hack" and false_count == VANILLA_FALSE_COUNT:
            logger.critical("HACK IS NOT ACTIVE")
            handle_notify(
                self.config.Error_OnePushConfig,
                title=f"Alas <{self.config_name}> crashed",
                content=f"<{self.config_name}> Hack is not active after Exercise",
            )
            exit(1)
        if false_count not in [VANILLA_FALSE_COUNT, HACK_FALSE_COUNT]:
            logger.critical(f"UNKNOWN VALUE FOR false_count: {false_count}")
            handle_notify(
                self.config.Error_OnePushConfig,
                title=f"Alas <{self.config_name}> crashed",
                content=f"<{self.config_name}> Unknown value for false_count in Perseus.ini",
            )
            exit(1)
        logger.info("Safety check passed!")
