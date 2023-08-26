import json
from queue import Queue

import servers.SeverQueue
from Struct.Event import Event
from Struct.Job import Job


class Server:
    serverNumber = 0

    finishNumber = 0
    finishSize = 0
    remainSize = 0
    remainNumber = 0

    currentTime = 0
    lastCheckTime = 0

    serverRecord= {
        "remainSize":[],
        "remainNumber": [],
        'currentTime':[],
        'server':[]
    }

    def __init__(self, policy, serverNumber):
        if policy == "FCFS":
            self.queue = servers.SeverQueue.FCFS(serverNumber=serverNumber)
            self.serverNumber = serverNumber
            self.job = Job()
            self.finishEvent = Queue()


    def job_leave(self, isFinish):

        self.finishNumber += isFinish
        self.remainNumber -= isFinish
        self.finishSize += self.currentTime - self.job.arrivalTime
        self.remainSize -= self.currentTime - self.job.arrivalTime
        self.job.arrivalTime = self.currentTime
        self.job.refresh()
        self.serverRecord['remainSize'].append(self.remainSize)
        self.serverRecord['remainNumber'].append(self.remainNumber)
        self.serverRecord['currentTime'].append(self.currentTime)
        self.serverRecord['server'].append(self.serverNumber)

    def job_arrive(self, job):
        if self.remainNumber !=0:
            self.finishSize += self.currentTime - self.job.arrivalTime
            self.remainSize -= self.currentTime - self.job.arrivalTime
            self.job.arrivalTime=self.currentTime
        self.remainSize += job.size
        self.remainNumber += 1

        self.serverRecord['remainSize'].append(self.remainSize)
        self.serverRecord['remainNumber'].append(self.remainNumber)
        self.serverRecord['currentTime'].append(self.currentTime)
        self.serverRecord['server'].append(self.serverNumber)

    def operation_recursion(self, parentEvent):
        while parentEvent.empty() is False:
            singleEvent = parentEvent.get()
            self.finishEvent.put(singleEvent)
            # print(json.dumps(singleEvent.__dict__))
            if singleEvent.operation[0] == '1':
                if singleEvent.operation[1] == '2':
                    if singleEvent.operation[2] == '3':
                        # print("self.remainNumber",self.remainNumber)
                        job = Job().event_to_job(singleEvent)
                        self.job_arrive(job)
                        if self.remainNumber == 1:
                            job = job.job_enter_processor(self.currentTime)
                            self.job = job
                            self.finishEvent.put(
                                Event().job_to_event(operation="215", job=self.job))
                            return
                        else:
                            event = Event().event_to_event(operation="223", event=singleEvent)
                            self.finishEvent.put(event)
                            subEvent = self.queue.operate_queue(
                                parentEvent=event,
                                currentTime=self.currentTime)
                            self.operation_recursion(subEvent)

                if singleEvent.operation[1] == '7':
                    if singleEvent.operation[2] == '0':
                        job = Job().job_to_job(self.job)
                        job = job.job_leave_processor(self.currentTime)
                        event = Event().job_to_event(operation="275", job=job)
                        self.finishEvent.put(event)
                        self.job_leave(1)
                        if self.queue.is_empty():
                            self.finishEvent.put(Event().job_to_event(operation="277", job=job))
                        else:
                            event = Event().only_operation(operation="230")
                            self.finishEvent.put(event)
                            subEvent = self.queue.operate_queue(parentEvent=event,
                                                                currentTime=self.currentTime)
                            self.operation_recursion(subEvent)

            if singleEvent.operation[0] == '3':
                if singleEvent.operation[1] == '2':
                    if singleEvent.operation[2] == '5':
                        self.finishEvent.put(Event().event_to_event(operation="225", event=singleEvent))
                        return
                if singleEvent.operation[1] == '3':
                    if singleEvent.operation[2] == '3':
                        job = Job().event_to_job(singleEvent)
                        job = job.job_enter_processor(self.currentTime)
                        self.job = job
                        self.finishEvent.put(Event().job_to_event(operation="235", job=job))

    def operate_server(self, parentEvent, currentTime):
        self.lastCheckTime = currentTime
        # print(currentTime)
        self.currentTime = currentTime
        self.finishEvent = Queue()
        event = Queue()
        event.put(parentEvent)
        self.operation_recursion(event)
        return self.finishEvent

    def get_remain_size(self):
        if self.remainSize == 0:
            return 0
        else:
            return self.remainSize - self.lastCheckTime

    def get_remain_number(self):
        return self.remainNumber
