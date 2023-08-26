import json
from queue import Queue
from Struct.Job import Job
from Struct.Event import Event


class FCFS:

    def __init__(self, serverNumber):
        self.queue = Queue()
        self.serverNumber = serverNumber

    def is_empty(self):
        return self.queue.empty()

    def operate_queue(self, parentEvent, currentTime):
        singleEvent = parentEvent
        finishEvent = Queue()

        # print(json.dumps(singleEvent.__dict__))
        if singleEvent.operation[0] != '2':
            print("Wrong in queue.")

        if singleEvent.operation[1] == '2':
            if singleEvent.operation[2] == '3':
                self.queue.put(Job().event_to_job(singleEvent))
                finishEvent.put(Event().event_to_event(operation="325", event=singleEvent))
                return finishEvent

        if singleEvent.operation[1] == '3':
            if singleEvent.operation[2] == '0':
                job = self.queue.get()
                job=job.job_leave_queue(currentTime)
                finishEvent.put(Event().job_to_event(operation="333", job=job))
            return finishEvent
