import states as s


class AEVC(object):
    """
    A simple state machine that mimics the functionality of a device from a
    high level.
    """

    def __init__(self):
        self.state = s.Initialize() # Start with initialization state


    def teensy_event(self, event):
        if event in s.returnMessages:
            s.returnMessages.remove(event)
            print("successfully removed " + str(event) + " from " + str(s.returnMessages))
        else:
            print("error in machine.py, tried to remove " + str(event) + " from " + str(s.returnMessages))

        if not s.returnMessages:

            last_state = self.state
            self.state = self.state.on_event(event)

            last_state.on_exit()
            self.state.on_entry()

            print("Transitioned to " + str(self.state) + ": " + str(event))  # announce state change made

    def user_event(self, event):
        last_state = self.state
        self.state = self.state.on_event(event)

        last_state.on_exit()
        self.state.on_entry()

        print("Transitioned to " + str(self.state) + ": " + str(event))  # announce state change made

    # def controllerEvent(self, event):
    # The next state will be the result of the on_event function.
