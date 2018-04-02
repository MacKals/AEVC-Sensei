import states as s
import teensy_talker as teensy


class AEVC(object):
    """
    A simple state machine that mimics the functionality of a device from a
    high level.
    """

    def __init__(self):
        self.state = s.Sleep()  # Start with sleep state

    def update_state(self, event):
        new_state = self.state.on_event(event)

        if new_state:
            self.state.on_exit()

            self.state = new_state
            self.state.on_entry()
            print("Transitioned to " + str(self.state) + ": " + str(event))  # announce state change made
        else:
            print("Stayed in " + str(self.state))

    def direct_event(self, event):
        teensy.send_command(event)

    def teensy_event(self, event):
        if event in s.returnMessages:
            s.returnMessages.remove(event)
            print("successfully removed " + str(event) + " from " + str(s.returnMessages))
        else:
            print("Passing on message from Teensy: " + str(event))

        if not s.returnMessages:
            self.update_state(event)

    def timer_event(self):
        self.state.tick()

    def user_event(self, event):

        if event is 'q':
            self.state = s.Sleep()
            print("Sleeping")
            self.state.on_entry()
            return

        self.update_state(event)

    def set_joystick_array(self, ja):
        s.joystickArray = ja

    # def controllerEvent(self, event):
    # The next state will be the result of the on_event function.
