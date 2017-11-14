from __future__ import absolute_import
from __future__ import with_statement

import time
import logging
import threading
from celery.events import EventReceiver
from celery.events.state import State



# logger = logging.getLogger(__name__)


class Events(threading.Thread):

    def __init__(self, state):
        threading.Thread.__init__(self)
        self.state = state

    def run(self):
        from app import celery
        celery.control.enable_events()
        while True:
            with celery.connection() as conn:
                recv = EventReceiver(conn,
                                     handlers={"*": self.on_event},
                                     app=celery)
                recv.capture(limit=None, timeout=None, wakeup=True)


    def on_event(self, event):
       self.state.event(event)



