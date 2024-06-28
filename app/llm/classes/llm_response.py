class LlmResponse:
    def __init__(
            self, 
            text, 
            chooseable_actions=[],
            actions=[]
        ) -> None:
        self.text = text
        self.chooseable_actions=chooseable_actions
        self.actions = actions
