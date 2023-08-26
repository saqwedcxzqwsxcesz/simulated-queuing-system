from queue import Queue


class EventRecord:
    def __init__(self, operation, server, jobNumber, arrivalTime, size, remainSize, queueTime, expectDepartureTime):
        self.expectDepartureTime = expectDepartureTime
        self.queueTime = queueTime
        self.remainSize = remainSize
        self.arrivalTime = arrivalTime
        self.size = size
        self.operation = operation
        self.jobNumber = jobNumber
        self.server = server


class Record:
    def __init__(self):
        self.eventQueue = Queue()

    def event_put(self, eventRecord):
        self.eventQueue.put(eventRecord)

    def event_get(self):
        return self.eventQueue.get()

    def event_empty(self):
        return self.eventQueue.empty()
