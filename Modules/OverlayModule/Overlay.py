import threading
import time

import OverlayUtils
import qtOverlay
from Chat import ChatModule

def runChatThread(ChatReader):

    time.sleep(5)


if __name__ == "__main__":
    AgentTracker = OverlayUtils.ValorantAgentTracker()
    Overlay = qtOverlay.QTOverlay()
    ChatReader = ChatModule(agentTracker=AgentTracker)

    Overlay.startSetup()

    while True:
        AgentTracker.updateAgentPositions()
        ChatReader.updateChat()
        #threading.Thread(target=runChatThread, args=(ChatReader,), daemon=True).start()

        time.sleep(5)



