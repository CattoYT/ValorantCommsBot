import threading
import time

import OverlayUtils
import qtOverlay
from Chat import ChatModule


def runChatThread(ChatReader):

    time.sleep(5)


if __name__ == "__main__":
    AgentTracker = OverlayUtils.ValorantAgentTracker()
    Overlay = qtOverlay.QTOverlay(agentTracker=AgentTracker)
    ChatReader = ChatModule(agentTracker=AgentTracker)

    Overlay.startSetup()

    while True:
        AgentTracker.updateAgentPositions()
        ChatReader.updateChat()
        #threading.Thread(target=runChatThread, args=(ChatReader,), daemon=True).start()


        # for this, i literally have no idea what to do, so im literally just going to yeet the label
        # heavy beta, only uncomment when in use
        # for agent in AgentTracker.validAgentsR:
        #     if agent.currentPosition is not None:
        #
        #         labels = [qtOverlay.label1, qtOverlay.label2, qtOverlay.label3, qtOverlay.label4, qtOverlay.label5] # cursed but lolz
        #         for i in labels:
        #             if i.offset == agent.currentPosition:
        #                 qtOverlay.worker(str(agent.health))
        #                 break

        time.sleep(5)

# currently, the code does successfully overlay the damage numbers.
# The only component that is left to work on in the overlay module is the offsetting of labels on agent death
# My current ideas thrown are:
# 1. create the health label object, but initiate the qtlabel afterwards
# 2. assign the label an agent name and compare the positions of validAgentsR to the labels. If they are out of oder, match them and if they aren't correct, set their x coord to the
# base position, and their Y position to wayyy up and then return them once the agent is back.
# At least one of these soltions should work??
# pls im desperate rn



