import json
import math

import pandas as pd
from scipy import stats
import pandas as pandas
import numpy as np


class JobsArrivalRecord:
    def __init__(self, interArrivalTime, interArrivalTimeStatistics, arrivalTime, jobsSize, jobsSizeStatistics):
        self.jobsSizeStatistics = jobsSizeStatistics
        self.jobsSize = jobsSize
        self.arrivalTime = arrivalTime
        self.interArrivalTimeStatistics = interArrivalTimeStatistics
        self.interArrivalTime = interArrivalTime


class JobsArrive:

    def __init__(self, x):
        self.config = x
        self.jobsSizeStatistics = None
        self.interArrivalTimeStatistics = None
        self.interArrivalTime = None
        self.arrivalTime = None
        self.section = None
        self.jobsSize = None
        self.Xaxis = x['comingJobsXaxis']
        self.jobNumber = x['system']['jobNumber']
        self.comingJobs = x['system']['comingJobs']
        self.meanInterArrivalTime = x['system']['meanInterArrivalTime']
        self.interArrivalTimeStandardDeviation = x['system']['interArrivalTimeStandardDeviation']
        self.meanJobsSize = x['system']['meanJobsSize']
        self.jobsSizeStandardDeviation = x['system']['jobsSizeStandardDeviation']
        self.set_jobs_arrive()
        self.jobArrivalRecord = {}

    def set_jobs_arrive(self):

        # Distribution of inter_arrival times of the jobs.
        if self.comingJobs[0] == 'M':
            self.interArrivalTime = stats.expon.rvs(scale=self.meanInterArrivalTime, size=self.jobNumber)
            self.interArrivalTimeStatistics = pandas.cut(self.interArrivalTime,
                                                         bins=[x for x in
                                                               range(0, math.ceil(max(self.interArrivalTime)),
                                                                     math.ceil(
                                                                         max(self.interArrivalTime) / self.Xaxis))])

        if self.comingJobs[0] == 'G':
            self.interArrivalTime = np.random.normal(loc=self.meanInterArrivalTime,
                                                     scale=self.interArrivalTimeStandardDeviation,
                                                     size=self.jobNumber)
            interval=max(max(self.interArrivalTime),self.meanInterArrivalTime * 2)
            self.interArrivalTimeStatistics = pandas.cut(self.interArrivalTime,
                                                         bins=[x for x in
                                                               range(0, math.ceil(interval),
                                                                     math.ceil(
                                                                         interval/ self.Xaxis))])

        if self.comingJobs[0] == 'D':
            self.interArrivalTime = [self.meanInterArrivalTime for _ in range(self.jobNumber)]
            self.interArrivalTimeStatistics = pandas.cut(self.interArrivalTime,
                                                         bins=[x for x in
                                                               range(0, math.ceil(self.meanInterArrivalTime * 2),
                                                                     math.ceil(
                                                                         self.meanInterArrivalTime * 2 / self.Xaxis))])

        self.arrivalTime = self.interArrivalTime
        for i in range(1, self.jobNumber):
            self.arrivalTime[i] = self.arrivalTime[i - 1] + self.interArrivalTime[i]

        # Distribution of job sizes.
        if self.comingJobs[2] == 'M':
            self.jobsSize = stats.expon.rvs(scale=self.meanJobsSize, size=self.jobNumber)
            self.jobsSizeStatistics = pandas.cut(self.jobsSize,
                                                 bins=[x for x in
                                                       range(0, math.ceil(max(self.jobsSize)),
                                                             math.ceil(
                                                                 max(self.jobsSize) / self.Xaxis))])

        if self.comingJobs[2] == 'G':
            self.jobsSize = np.random.normal(loc=self.meanJobsSize,
                                             scale=self.jobsSizeStandardDeviation,
                                             size=self.jobNumber)
            interval = max(max(self.jobsSize), self.meanJobsSize * 2)
            self.jobsSizeStatistics = pandas.cut(self.jobsSize,
                                                 bins=[x for x in
                                                       range(0, math.ceil(interval),
                                                             math.ceil(
                                                                 interval / self.Xaxis))])

        if self.comingJobs[2] == 'D':
            self.jobsSize = [self.meanJobsSize for _ in range(self.jobNumber)]
            self.jobsSizeStatistics = pandas.cut(self.jobsSize,
                                                 bins=[x for x in
                                                       range(0, math.ceil(self.meanJobsSize * 2),
                                                             math.ceil(
                                                                 self.meanJobsSize * 2 / self.Xaxis))])

        JobsArrival = {
            "interArrivalTime": self.interArrivalTime.tolist(),
            "arrivalTime": self.arrivalTime.tolist(),
            "jobsSize": self.jobsSize.tolist(),
        }
        print(JobsArrival)

        path = "./save/" + self.config['fileName'] + "/jobsArrival.json"
        with open(path, "w") as f:
            json.dump(JobsArrival, f)
        print("JobsArrival saved")
        print()

    def get_inter_arrival_time(self):
        return self.interArrivalTime

    def get_arrival_time(self):
        return self.arrivalTime

    def get_inter_arrival_time_statistics(self):
        return self.interArrivalTimeStatistics

    def get_jobs_size(self):
        return self.jobsSize

    def get_jobs_size_statistics(self):
        return self.jobsSizeStatistics

    def get_job_number(self):
        return self.jobNumber
