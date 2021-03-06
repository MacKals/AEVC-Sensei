class AEVCState(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self):
        print('Init new state:' + str(self))

    def on_entry(self):
        pass

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def on_exit(self):
        pass

    def tick(self):
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__
