class Event:
    # jobNumber = 0
    # server = 0
    # size = 0
    # operation = 0
    # expectDepartureTime = 0
    # arrivalTime = 0
    # remainSize = 0
    # queueTime = 0

    def __init__(self):
        self.jobNumber = 0
        self.server = 0
        self.size = 0
        self.operation = ""
        self.expectDepartureTime = 0
        self.arrivalTime = 0
        self.remainSize = 0
        self.queueTime = 0

    def job_to_event(self, operation, job):
        self.jobNumber = job.jobNumber
        self.server = job.server
        self.size = job.size
        self.operation = operation
        self.expectDepartureTime = job.expectDepartureTime
        self.arrivalTime = job.arrivalTime
        self.remainSize = job.remainSize
        self.queueTime = job.queueTime
        return self

    # destination=1,2,3
    # 1 queue, 2 processor, 3 leave
    # def job_transfer(self, operation, job, currentTime, destination):
    #     # job: enter queue
    #     if destination == 1:
    #         self.jobNumber = job.jobNumber
    #         self.server = job.server
    #         self.size = job.size
    #         self.operation = operation
    #         self.expectDepartureTime = 0
    #         self.arrivalTime = currentTime
    #         self.remainSize = job.remainSize
    #         self.queueTime = job.queueTime + (currentTime - job.arrivalTime)
    #
    #     # job: enter processor
    #     if destination == 2:
    #         self.jobNumber = job.jobNumber
    #         self.server = job.server
    #         self.size = job.size
    #         self.operation = operation
    #         self.expectDepartureTime = currentTime + job.remainSize
    #         self.arrivalTime = currentTime
    #         self.remainSize = job.remainSize
    #         self.queueTime = job.queueTime + (currentTime - job.arrivalTime)
    #
    #     #  job leave processor
    #     if destination == 3:
    #         self.jobNumber = job.jobNumber
    #         self.server = job.server
    #         self.size = job.size
    #         self.operation = operation
    #         self.expectDepartureTime = 0
    #         self.arrivalTime = currentTime
    #         self.remainSize = job.remainSize - (currentTime - job.arrivalTime)
    #         self.queueTime = job.queueTime
    #
    #     return self
    #
    #     # # job: leave processor, enter queue
    #     # if destination == 2:
    #     #     self.jobNumber = job.jobNumber
    #     #     self.server = job.server
    #     #     self.size = job.size
    #     #     self.operation = operation
    #     #     self.expectDepartureTime = 0
    #     #     self.arrivalTime = currentTime
    #     #     self.remainSize = job.remainSize - (currentTime - job.arrivalTime)
    #     #     self.queueTime = job.queueTime
    #
    #     # # job: leave queue, enter processor
    #     # if destination == 1:
    #     #     self.jobNumber = job.jobNumber
    #     #     self.server = job.server
    #     #     self.size = job.size
    #     #     self.operation = operation
    #     #     self.expectDepartureTime = currentTime + job.remainSize
    #     #     self.arrivalTime = currentTime
    #     #     self.remainSize = job.remainSize
    #     #     self.queueTime = job.queueTime + (currentTime - job.arrivalTime)

    # event transfer
    def event_to_event(self, operation, event):
        self.jobNumber = event.jobNumber
        self.server = event.server
        self.size = event.size
        self.operation = operation
        self.expectDepartureTime = event.expectDepartureTime
        self.arrivalTime = event.arrivalTime
        self.remainSize = event.remainSize
        self.queueTime = event.queueTime
        return self

    # just operation
    def only_operation(self, operation):
        self.jobNumber = 0
        self.server = 0
        self.size = 0
        self.operation = operation
        self.expectDepartureTime = 0
        self.arrivalTime = 0
        self.remainSize = 0
        self.queueTime = 0
        return self

    def __lt__(self, other):
        if self.expectDepartureTime < other.expectDepartureTime:
            return True
        else:
            return False
