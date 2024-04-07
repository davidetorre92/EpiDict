class TransitionRule:
    def __init__(self):
        self.name = None
        self.attribute = None
        self.initial_state = None
        self.triggering_state = None
        self.final_state = None
        self.prob = None
        self.mode = None
        
    def _validate_dynamics(self, attributes):
        available_attributes = ['compartment']
        available_modes = ['rate', 'neighbor']

        if self.attribute is None:
            raise RuntimeError("Attribute not initialized")
        if self.attribute not in available_attributes:
            raise RuntimeError(f"Attribute should be equal to one of these: {', '.join(map(str, available_attributes))}")

        if self.initial_state is None:
            raise RuntimeError("Initial state not initialized")
        if self.attribute == 'compartment':
            compartments_name = attributes['compartment']
            if self.initial_state not in compartments_name:
                raise RuntimeError(f"Initial state should be equal to one of these: {', '.join(map(str, compartments_name))}")

        if self.final_state is None:
            raise RuntimeError("Final state not initialized")
        if self.attribute == 'compartment':
            compartments_name = attributes['compartment']
            if self.final_state not in compartments_name:
                raise RuntimeError(f"Final state should be equal to one of these: {', '.join(map(str, compartments_name))}")
        
        if self.prob is None:
            raise RuntimeError("Probability not initialized")
        if self.prob <= 0 or self.prob >= 1:
            raise RuntimeError(f"Illegal probability value: p = {self.prob} while p in (0,1)")
        if self.mode is None:
            raise RuntimeError("Mode not initialized")
        if self.mode not in available_modes:
            raise RuntimeError(f"Mode should be equal to one of these: {', '.join(map(str, compartments_name))}")
        if self.mode == 'neighbor':
            if self.attribute == 'compartment':
                compartments_name = attributes['compartment']
                if self.triggering_state not in compartments_name:
                    raise RuntimeError(f"Triggering state should be equal to one of these: {', '.join(map(str, compartments_name))}")

        return True

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Attribute: {self.attribute}\n"
                f"Initial State: {self.initial_state}\n"
                f"Triggering State: {self.triggering_state}\n"
                f"Final State: {self.final_state}\n"
                f"Probability: {self.prob}\n"
                f"Mode: {self.mode}\n"
                f"Check Status: {self.check_status}")


class Compartment:
    def __init__(self, attributes):
        self.attributes = attributes
        self.transition_rules = []
        
    def add_dynamic_from_transition_rule(self, tr):
        tr._validate_dynamics(self.attributes)
        self.transition_rules.append(tr)

    def add_dynamic_from_dictionary(self, **kwargs):
        new_transition_rule = TransitionRule()
        new_transition_rule.name = kwargs['name']
        new_transition_rule.attribute = kwargs['attribute']
        new_transition_rule.initial_state = kwargs['initial_state']
        new_transition_rule.triggering_state = kwargs['triggering_state']
        new_transition_rule.final_state = kwargs['final_state']
        new_transition_rule.prob = kwargs['prob']
        new_transition_rule.mode = kwargs['mode']
        new_transition_rule._validate_dynamics(self.attributes)
        self.transition_rules.append(new_transition_rule)
        
    def __str__(self):
        string = "SUMMARY"
        for transition in self.transition_rules:
            string += f"\n- {transition.name}:\n"
            string += f"({transition.initial_state}) -> ({transition.final_state})"
            if transition.mode == 'neighbor':
                string += f" caused by ({transition.triggering_state})"
            string += f" p = {transition.prob}"
        return string
