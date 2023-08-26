class Job:
    jobNumber = 0
    server = 0
    queueTime = 0
    size = 0
    arrivalTime = 0
    remainSize = 0
    expectDepartureTime = 0

    # def __init__(self):
    #     self.jobNumber = 0
    #     self.server = 0
    #     self.queueTime = 0
    #     self.size = 0
    #     self.arrivalTime = 0
    #     self.remainSize = 0

    def set_job(self, jobNumber, arrivalTime, size, remainSize, queueTime, server):
        self.remainSize = remainSize
        self.size = size
        self.arrivalTime = arrivalTime
        self.jobNumber = jobNumber
        self.queueTime = queueTime
        self.server = server
        self.expectDepartureTime = arrivalTime
        return self

    # evnet to job
    def event_to_job(self, event):
        self.remainSize = event.remainSize
        self.size = event.size
        self.arrivalTime = event.arrivalTime
        self.jobNumber = event.jobNumber
        self.queueTime = event.queueTime
        self.server = event.server
        self.expectDepartureTime = event.expectDepartureTime
        return self

    def job_leave_queue(self, currentTime):
        self.jobNumber = self.jobNumber
        self.server = self.server
        self.size = self.size
        self.queueTime = self.queueTime + (currentTime - self.arrivalTime)
        self.arrivalTime = currentTime
        self.remainSize = self.remainSize
        self.expectDepartureTime = self.expectDepartureTime

        return self

    def job_leave_processor(self, currentTime):
        self.jobNumber = self.jobNumber
        self.server = self.server
        self.size = self.size
        self.expectDepartureTime = self.expectDepartureTime
        self.remainSize = self.remainSize - (currentTime - self.arrivalTime)
        self.arrivalTime = currentTime
        self.queueTime = self.queueTime
        return self

    def job_enter_processor(self, currentTime):
        self.jobNumber = self.jobNumber
        self.server = self.server
        self.size = self.size
        self.expectDepartureTime = currentTime + self.remainSize
        self.arrivalTime = currentTime
        self.remainSize = self.remainSize
        self.queueTime = self.queueTime
        return self

    def job_to_job(self, job):
        self.jobNumber = job.jobNumber
        self.server = job.server
        self.size = job.size
        self.expectDepartureTime = job.expectDepartureTime
        self.arrivalTime = job.arrivalTime
        self.remainSize = job.remainSize
        self.queueTime =job.queueTime
        return self

    def refresh(self):
        self.remainSize = 0
        self.size = 0
        self.arrivalTime = 0
        self.jobNumber = 0
        self.queueTime = 0
        self.expectDepartureTime = 0
        self.server = 0
