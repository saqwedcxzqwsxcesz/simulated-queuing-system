import json
from asyncio import sleep
from queue import Queue
import heapq
import random

from Struct.Event import Event
from Struct.Job import Job
from Struct.Record import Record
from servers.Sever import Server


# import random


class CentralSystem:

    def __init__(self, config):
        self.config = config
        self.policy = config['system']['taskAssignment']['policy']
        self.SITAPolicy = config['system']['taskAssignment']['SITAPolicy']
        self.k = config['system']['serverNumber']
        self.serverNumber = config['system']['serverNumber']
        self.jubNumber = config['system']['jobNumber']

        path="./save/" +config['fileName']+"/jobsArrival.json"
        with open(path, 'r') as x:
            jobArrival = json.load(x)
        print("jobArrival:",jobArrival)
        self.jobSize = jobArrival['jobsSize']
        self.arrivalTime = jobArrival['arrivalTime']
        print("jobSize:",self.jobSize)
        print("arrivalTime:",self.arrivalTime)

        # self.jobSize = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        # self.arrivalTime = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

        # self.jobSize = [4, 4, 4, 4, 4, 4, 2, 2, 2, 2]
        # self.arrivalTime = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

        # self.jobSize = [3, 0.5, 0.5, 0.5, 0.5, 4, 2, 2, 2, 2]
        # self.arrivalTime = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]



        self.centralQueue = Queue()
        self.eventHeap = []
        self.servers = {}


        self.record = Record()

        self.RRNumber = 0

        self.k = config['system']['serverNumber']
        for i in range(self.jubNumber):
            self.jobSize[i] = self.jobSize[i] * self.k

        for i in range(self.serverNumber + 1):
            self.servers[i] = Server(policy=config['system']['schedulingPolicy']['policy'], serverNumber=i)

        for i in range(self.jubNumber):
            job = Job()
            job = job.set_job(jobNumber=i, arrivalTime=self.arrivalTime[i], size=self.jobSize[i],
                              remainSize=self.jobSize[i],
                              queueTime=0, server=0)
            self.centralQueue.put(job)

        while self.centralQueue.empty() is False:
            heapq.heappush(self.eventHeap, Event().job_to_event(operation="123", job=self.centralQueue.get()))

        while len(self.eventHeap) != 0:
            event = heapq.heappop(self.eventHeap)
            currentTime = event.expectDepartureTime
            if event.operation == "123":
                server = 0
                if self.policy == "Random":
                    server = random.randint(1, self.serverNumber)
                    # print("server", server)

                if self.policy == "RR":
                    server = self.RRNumber % self.serverNumber + 1
                    self.RRNumber += 1
                    # print("server", server)

                if self.policy == "JSQ":
                    JSQList = []
                    for i in range(1, self.serverNumber + 1):
                        JSQList.append(self.servers[i].get_remain_number())
                    server = JSQList.index(min(JSQList)) + 1

                if self.policy == "LWL":
                    JSQList = []
                    for i in range(1, self.serverNumber + 1):
                        JSQList.append(self.servers[i].get_remain_size())
                    server = JSQList.index(min(JSQList)) + 1

                if self.policy == "SITA":
                    for i in range(self.serverNumber - 1):
                        if (self.SITAPolicy[i]*self.k < event.size) & (event.size < self.SITAPolicy[i + 1]*self.k):
                            server = i+1
                            break
                    if (server == 0):
                        server = self.serverNumber

                job = Job().event_to_job(event)
                job = job.job_leave_queue(currentTime)
                job.server = server
                feedback = self.servers[server].operate_server(
                    parentEvent=Event().job_to_event(operation="123", job=job),
                    currentTime=currentTime)
                while feedback.empty() is False:
                    singleRecord = feedback.get()
                    # print(json.dumps(singleRecord.__dict__))
                    self.record.event_put(singleRecord)
                    if singleRecord.operation == "215":
                        heapq.heappush(self.eventHeap, Event().event_to_event(operation="170", event=singleRecord))

            if event.operation == "170":
                feedback = self.servers[event.server].operate_server(
                    parentEvent=Event().only_operation(operation="170"),
                    currentTime=currentTime)
                while feedback.empty() is False:
                    singleRecord = feedback.get()
                    # print(json.dumps(singleRecord.__dict__))
                    self.record.event_put(singleRecord)
                    if singleRecord.operation == "235":
                        heapq.heappush(self.eventHeap, Event().event_to_event(operation="170", event=singleRecord))
        print("simulate finished")
        self.save_record()
        self.save_severs_record()

    def save_record(self):
        recordWrite = {}
        i = 0
        # print()
        while self.record.event_empty() is False:
            singleRecord = self.record.event_get()
            # print(json.dumps(singleRecord.__dict__))
            recordWrite[i] = json.dumps(singleRecord.__dict__)
            i += 1

        path = "./save/" + self.config['fileName'] + "/record.json"
        with open(path, "w") as f:
            json.dump(recordWrite, f)
        print("record saved\n")

        return self.record

    def save_severs_record(self):
        seversRecord=self.servers[1].serverRecord
        path = "./save/" + self.config['fileName'] + "/seversRecord.json"
        with open(path, "w") as f:
            json.dump(seversRecord, f)
        print("seversRecord saved\n")
        return

