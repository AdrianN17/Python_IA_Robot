from finite_state_machine import StateMachine, transition

class fsm_decision(StateMachine):
    initial_state = "no_abastecido"

    def __init__(self):
        self.state = self.initial_state
        super().__init__()

    @transition(source = ["abastecido"], target="irA")
    def irA(self):
        pass

    @transition(source=["abastecido"], target="irB")
    def irB(self):
        pass

    @transition(source=["abastecido"], target="irC")
    def irC(self):
        pass

    @transition(source=["irA","irB","irC"], target="no_abastecido")
    def irNoAbastecido(self):
        pass

    @transition(source=["no_abastecido"], target="abastecido")
    def irAbastecido(self):
        pass

    @transition(source=["irA", "irB", "irC", "no_abastecido", "abastecido"], target="no_abastecido")
    def reseteo_fsm(self):
        pass

