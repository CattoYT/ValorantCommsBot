import OverlayUtils
import qtOverlay
from Chat import ChatModule

if __name__ == "__main__":
    AgentTracker = OverlayUtils.ValorantAgentTracker()
    Overlay = qtOverlay.QTOverlay()
    ChatReader = ChatModule()

    while True:
        AgentTracker.updateAgentPositions()

        for agent in AgentTracker.validAgentsL:
            Overlay.updateAgent(agent, "R", 150, agent)



