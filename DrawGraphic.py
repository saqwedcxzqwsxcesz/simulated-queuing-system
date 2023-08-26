import json
import math
import shutil

import pandas
from pyecharts import charts
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


class ServerInf:
    def __init__(self, serversRecord, config):
        self.serverNumber = config['system']['serverNumber']
        self.FrequencyOfSampling = config['FrequencyOfSampling']
        self.x=[]
        self.x.append(0)
        for i in range(len(serversRecord['currentTime'])):
            serversRecord['remainSize'][i] /= self.serverNumber
        # print(serversRecord)
        self.servers = []
        for i in range(self.serverNumber + 1):
            self.servers.append({
                "remainSize": [],
                "remainNumber": [],
                "time":[]
            })
        for i in range(self.serverNumber + 1):
            self.servers[i]['remainSize'].append(0)
            self.servers[i]['remainNumber'].append(0)
            self.servers[i]['time'].append(0)

        recordNumber=0
        for i in range(self.FrequencyOfSampling, math.ceil(max(serversRecord['currentTime'])),
                       self.FrequencyOfSampling):
            self.x.append(i/self.FrequencyOfSampling)
            for j in range(1, self.serverNumber + 1):
                self.servers[j]['time'].append(i)
                self.servers[j]['remainNumber'].append(
                    self.servers[j]['remainNumber'][len(self.servers[j]['remainNumber']) - 1])
                lastRemainSize = self.servers[j]['remainSize'][len(self.servers[j]['remainSize']) - 1]
                self.servers[j]['remainSize'].append(
                    max((lastRemainSize - self.FrequencyOfSampling / self.serverNumber), 0))
            if recordNumber<=len(serversRecord['currentTime']):
                while serversRecord['currentTime'][recordNumber]<=i:
                    sever=serversRecord['server'][recordNumber]
                    self.servers[sever]['remainNumber'][len(self.servers[sever]['remainNumber'])-1]=serversRecord['remainNumber'][recordNumber]
                    self.servers[sever]['remainSize'][len(self.servers[sever]['remainSize'])-1]=max((serversRecord['remainSize'][recordNumber]-(i-serversRecord['currentTime'][recordNumber]) / self.serverNumber),0)
                    recordNumber += 1
            totalRemainNumber=0
            totalRemainSize=0
            for j in range(1, self.serverNumber + 1):
                totalRemainNumber+=self.servers[j]['remainNumber'][len(self.servers[j]['remainNumber'])-1]
                totalRemainSize+=self.servers[j]['remainSize'][len(self.servers[j]['remainSize'])-1]
            self.servers[0]['remainNumber'].append(totalRemainNumber)
            self.servers[0]['remainSize'].append(totalRemainSize)

        # print(self.servers)
        # for i in range(len(self.servers[0]['remainNumber'])):
        #     self.x.append(i*self.FrequencyOfSampling)
        # print(self.servers)

    def get_x(self):
        return self.x
    def get_server_number(self):
        return self.serverNumber + 1

class JobInf:
    jobs = {}

    def __init__(self, record, jobsArrival, config):
        self.serverNumber = config['system']['serverNumber']
        number = len(jobsArrival['interArrivalTime'])
        self.server = [0] * number
        self.queueTime = [0] * number
        self.severTime = [0] * number
        self.responseTime = [0] * number
        self.slowdown = [0] * number
        self.arrivalTime = [0] * number
        self.departureTime = [0] * number
        for i in range(number):
            self.severTime[i] = jobsArrival['jobsSize'][i]
            self.arrivalTime[i] = jobsArrival['arrivalTime'][i]
        j = 0
        for i in range(len(record)):
            key = str(i)
            event = json.loads(record[key])
            if event['operation'] == "275":
                print(event)
                self.server[j] = event['server']
                self.queueTime[j] = event['queueTime']
                self.departureTime[j] = event['expectDepartureTime']
                j += 1
        for i in range(number):
            self.responseTime[i] = self.queueTime[i] + self.severTime[i]
            self.slowdown[i] = self.responseTime[i] * 1. / self.severTime[i]
        self.servers = []
        for i in range(self.serverNumber + 1):
            self.servers.append({
                "jobNumber": [],
                "severTime": [],
                "arrivalTime": [],
                "queueTime": [],
                "departureTime": [],
                "responseTime": [],
                "slowdown": [],
            })
        # print(self.servers)
        for i in range(number):
            self.servers[self.server[i]]["jobNumber"].append(i)
            self.servers[self.server[i]]["severTime"].append(self.severTime[i])
            self.servers[self.server[i]]["arrivalTime"].append(self.arrivalTime[i])
            self.servers[self.server[i]]["queueTime"].append(self.queueTime[i])
            self.servers[self.server[i]]["departureTime"].append(self.departureTime[i])
            self.servers[self.server[i]]["responseTime"].append(self.responseTime[i])
            self.servers[self.server[i]]["slowdown"].append(self.slowdown[i])

    def get_server_number(self):
        return self.serverNumber + 1


class DrawGraphic:
    width = "1080px"
    height = "600px"

    def inter_arrival_time_statistics(self, jobsArrive):
        y = [int(item) for item in list(jobsArrive.get_inter_arrival_time_statistics().value_counts().values)]
        x = [str(item) for item in list(jobsArrive.get_inter_arrival_time_statistics().value_counts().index.values)]

        interArrivalTimeStatistics = (charts.Bar(init_opts=opts.InitOpts(width=self.width,
                                                                         height=self.height))
                                      .add_xaxis(x)
                                      .add_yaxis("InterArrivalTime", y)
                                      .set_global_opts(title_opts=opts.TitleOpts(title="InterArrivalTimeStatistics"),
                                                       xaxis_opts=opts.AxisOpts(name='InterArrivalTime',
                                                                                axislabel_opts={"rotate": 50}),
                                                       yaxis_opts=opts.AxisOpts(name='Number'),
                                                       legend_opts=opts.LegendOpts(is_show=False))
                                      .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                                      .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                                      )
        return interArrivalTimeStatistics

    def jobs_size_statistics(self, jobsArrive):
        y = [int(item) for item in list(jobsArrive.get_jobs_size_statistics().value_counts().values)]
        x = [str(item) for item in list(jobsArrive.get_jobs_size_statistics().value_counts().index.values)]

        # print(x)
        # print(y)
        jobsSizeStatistics = (charts.Bar(init_opts=opts.InitOpts(width=self.width, height=self.height))
                              .add_xaxis(x)
                              .add_yaxis("JobsSize", y)
                              .set_global_opts(title_opts=opts.TitleOpts(title="JobsSizeStatistics"),
                                               xaxis_opts=opts.AxisOpts(name='JobsSize', axislabel_opts={"rotate": 50}),
                                               yaxis_opts=opts.AxisOpts(name='Number'),
                                               legend_opts=opts.LegendOpts(is_show=False))
                              .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                              .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                              )
        return jobsSizeStatistics

    def draw_job_arrival(self, jobsArrive, config):
        page = charts.Page()

        inter_arrival_time_statistics=self.inter_arrival_time_statistics(jobsArrive)
        jobs_size_statistics=self.jobs_size_statistics(jobsArrive)
        page.add(inter_arrival_time_statistics)
        page.add(jobs_size_statistics)

        if (config['ifScreenShot'] != 0):
            path = "./save/" + config['fileName'] + "/inter_arrival_time_statistics.png"
            make_snapshot(snapshot, inter_arrival_time_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/jobs_size_statistics.png"
            make_snapshot(snapshot, jobs_size_statistics.render(), path)

        page.render("arrival_jobs_statistics.html")

        path = "./save/" + config['fileName']
        shutil.copy('arrival_jobs_statistics.html', path)
        print("arrival_jobs_statistics saved\n")

    def queue_time_statistics(self, jobInf, Xaxis):
        queueTime = jobInf.queueTime
        queueTime = pandas.cut(queueTime,
                               bins=[x for x in range(0, math.ceil(max(queueTime)), math.ceil(max(queueTime) / Xaxis))])
        y = [int(item) for item in list(queueTime.value_counts().values)]
        x = [str(item) for item in list(queueTime.value_counts().index.values)]
        queueTimeStatistics = (charts.Bar(init_opts=opts.InitOpts(width=self.width, height=self.height))
                               .add_xaxis(x)
                               .add_yaxis("queueTime", y)
                               .set_global_opts(title_opts=opts.TitleOpts(title="QueueTimeStatistics"),
                                                xaxis_opts=opts.AxisOpts(name='QueueTime',
                                                                         axislabel_opts={"rotate": 50}),
                                                yaxis_opts=opts.AxisOpts(name='Number'),
                                                legend_opts=opts.LegendOpts(is_show=False))
                               .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                               .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                               )
        return queueTimeStatistics

    def queue_time(self, jobInf):
        y = jobInf.queueTime
        x = [i for i in range(len(y))]
        queueTime = (charts.Line(init_opts=opts.InitOpts(width=self.width, height=self.height))
                               .add_xaxis(x)
                               .add_yaxis(series_name="queueTime", y_axis=y, label_opts=opts.LabelOpts(is_show=False))
                               .set_global_opts(title_opts=opts.TitleOpts(title="QueueTime"),
                                                xaxis_opts=opts.AxisOpts(name='Job',
                                                                         axislabel_opts={"rotate": 50}),
                                                yaxis_opts=opts.AxisOpts(name='QueueTime'),
                                                legend_opts=opts.LegendOpts(is_show=False))
                               .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                               )
        return queueTime

    def slowdown_statistics(self, jobInf, Xaxis):
        slowdown = jobInf.slowdown
        slowdown = pandas.cut(slowdown,
                              bins=[x for x in range(0, math.ceil(max(slowdown)), math.ceil(max(slowdown) / Xaxis))])
        y = [int(item) for item in list(slowdown.value_counts().values)]
        x = [str(item) for item in list(slowdown.value_counts().index.values)]
        slowdownStatistics = (charts.Bar(init_opts=opts.InitOpts(width=self.width, height=self.height))
                              .add_xaxis(x)
                              .add_yaxis("slowdown", y)
                              .set_global_opts(title_opts=opts.TitleOpts(title="SlowdownStatistics"),
                                               xaxis_opts=opts.AxisOpts(name='Slowdown',
                                                                        axislabel_opts={"rotate": 50}),
                                               yaxis_opts=opts.AxisOpts(name='Number'),
                                               legend_opts=opts.LegendOpts(is_show=False))
                              .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                              .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                              )
        return slowdownStatistics

    def slowdown(self, jobInf):
        y = jobInf.slowdown
        x = [i for i in range(len(y))]
        slowdown = (charts.Line(init_opts=opts.InitOpts(width=self.width, height=self.height))
                               .add_xaxis(x)
                               .add_yaxis(series_name="Slowdown", y_axis=y, label_opts=opts.LabelOpts(is_show=False))
                               .set_global_opts(title_opts=opts.TitleOpts(title="Slowdown"),
                                                xaxis_opts=opts.AxisOpts(name='Job',
                                                                         axislabel_opts={"rotate": 50}),
                                                yaxis_opts=opts.AxisOpts(name='Slowdown'),
                                                legend_opts=opts.LegendOpts(is_show=False))
                               .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                               )
        return slowdown


    def arrival_departure_time_statistics(self, jobInf):
        arrivalTime = jobInf.arrivalTime
        departureTime = jobInf.departureTime
        x = [i for i in range(len(arrivalTime))]
        arrival_departure_time_statistics = (
            Line(init_opts=opts.InitOpts(width=self.width, height=self.height))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="arrivalTime", y_axis=arrivalTime, label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis(series_name="departureTime", y_axis=departureTime, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Arrival-Departure"),
                             xaxis_opts=opts.AxisOpts(name='Job',
                                                      axislabel_opts={"rotate": 50}),
                             yaxis_opts=opts.AxisOpts(name='Time'))
        )
        return arrival_departure_time_statistics

    def server_queue_time_statistics(self, jobInf, Xaxis):
        serverQueueTime = []
        y = []
        for i in range(1, jobInf.get_server_number()):
            serverQueueTime.append(pandas.cut(jobInf.servers[i]["queueTime"],
                                              bins=[x for x in range(0, math.ceil(max(jobInf.queueTime)), math.ceil(
                                                  max(jobInf.queueTime) / Xaxis * jobInf.get_server_number()))]))

        x = [str(item) for item in list(serverQueueTime[0].value_counts().index.values)]
        for i in range(0, jobInf.get_server_number() - 1):
            print()
            y.append([int(item) for item in list(serverQueueTime[i].value_counts().values)])
        serverQueueTimeStatistics = (charts.Bar(init_opts=opts.InitOpts(width=self.width, height=self.height))
                                     .add_xaxis(x)
                                     .set_global_opts(title_opts=opts.TitleOpts(title="ServerQueueTimeStatistics"),
                                                      xaxis_opts=opts.AxisOpts(name='QueueTime',
                                                                               axislabel_opts={"rotate": 50}),
                                                      yaxis_opts=opts.AxisOpts(name='Number'))
                                     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                                     .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                                     )
        for i in range(1, jobInf.get_server_number()):
            serverQueueTimeStatistics.add_yaxis("server" + str(i), y[i - 1])
        return serverQueueTimeStatistics

    def server_slowdown_statistics(self, jobInf, Xaxis):
        serverSlowdown = []
        y = []
        for i in range(1, jobInf.get_server_number()):
            serverSlowdown.append(pandas.cut(jobInf.servers[i]["slowdown"],
                                             bins=[x for x in range(0, math.ceil(max(jobInf.slowdown)), math.ceil(
                                                 max(jobInf.slowdown) / Xaxis * jobInf.get_server_number()))]))

        x = [str(item) for item in list(serverSlowdown[0].value_counts().index.values)]
        for i in range(0, jobInf.get_server_number() - 1):
            print()
            y.append([int(item) for item in list(serverSlowdown[i].value_counts().values)])
        serverSlowdownStatistics = (charts.Bar(init_opts=opts.InitOpts(width=self.width, height=self.height))
                                    .add_xaxis(x)
                                    .set_global_opts(title_opts=opts.TitleOpts(title="ServerSlowdownStatistics"),
                                                     xaxis_opts=opts.AxisOpts(name='Slowdown',
                                                                              axislabel_opts={"rotate": 50}),
                                                     yaxis_opts=opts.AxisOpts(name='Number'))
                                    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                                    )
        for i in range(1, jobInf.get_server_number()):
            serverSlowdownStatistics.add_yaxis("server" + str(i), y[i - 1])
        return serverSlowdownStatistics

    def server_job_statistics(self, jobInf):
        jobs = []
        for i in range(1, jobInf.get_server_number()):
            jobs.append(len(jobInf.servers[i]['slowdown']))
        x = [i for i in range(1, jobInf.get_server_number())]
        jobsInEachServerStatistics = (
            charts.Bar(init_opts=opts.InitOpts(width=self.width, height=self.height))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="Jobs", y_axis=jobs)
            .set_global_opts(title_opts=opts.TitleOpts(title="ServerWorkload"),
                             xaxis_opts=opts.AxisOpts(name='Sever'),
                             yaxis_opts=opts.AxisOpts(name='Jobs'),
                             legend_opts=opts.LegendOpts(is_show=False))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True)
                             ))
        return jobsInEachServerStatistics

    def remain_number_statistics(self,serverInf):
        x=serverInf.get_x()
        # print("x:",x)
        y=serverInf.servers
        remainNumberStatistics = (
            Line(init_opts=opts.InitOpts(width=self.width, height=self.height))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="Total", y_axis=y[0]['remainNumber'], label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="RemainJobs"),
                             xaxis_opts=opts.AxisOpts(name='SamplingPoint',
                                                      axislabel_opts={"rotate": 50}),
                             yaxis_opts=opts.AxisOpts(name='Job'))
        )
        for i in range(1, serverInf.get_server_number()):
            remainNumberStatistics.add_yaxis("server" + str(i), y[i]['remainNumber'], label_opts=opts.LabelOpts(is_show=False))
        return remainNumberStatistics

    def remain_size_statistics(self,serverInf):
        x=serverInf.get_x()
        # print("x:",x)
        y=serverInf.servers
        remainSizeStatistics = (
            Line(init_opts=opts.InitOpts(width=self.width, height=self.height))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="Total", y_axis=y[0]['remainSize'], label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="RemainTime"),
                             xaxis_opts=opts.AxisOpts(name='SamplingPoint',
                                                      axislabel_opts={"rotate": 50}),
                             yaxis_opts=opts.AxisOpts(name='Time'))
        )
        for i in range(1, serverInf.get_server_number()):
            remainSizeStatistics.add_yaxis("server" + str(i), y[i]['remainSize'], label_opts=opts.LabelOpts(is_show=False))
        return remainSizeStatistics

    def draw_simulate(self, config):
        path = "./save/" + config['fileName'] + "/record.json"
        with open(path, 'r') as x:
            record = json.load(x)
        # print(record)
        path = "./save/" + config['fileName'] + "/jobsArrival.json"
        with open(path, 'r') as x:
            jobsArrival = json.load(x)
        # print(jobsArrival)
        jobInf = JobInf(record, jobsArrival, config)
        page = charts.Page()
        queue_time=self.queue_time(jobInf=jobInf)
        queue_time_statistics=self.queue_time_statistics(jobInf=jobInf, Xaxis=config['SimulateXaxis'])
        slowdown=self.slowdown(jobInf=jobInf)
        slowdown_statistics=self.slowdown_statistics(jobInf=jobInf, Xaxis=config['SimulateXaxis'])
        arrival_departure_time_statistics=self.arrival_departure_time_statistics(jobInf=jobInf)
        server_queue_time_statistics=self.server_queue_time_statistics(jobInf=jobInf, Xaxis=config['SimulateXaxis'])
        server_slowdown_statistics=self.server_slowdown_statistics(jobInf=jobInf, Xaxis=config['SimulateXaxis'])
        server_job_statistics=self.server_job_statistics(jobInf=jobInf)
        page.add(queue_time)
        page.add(queue_time_statistics)
        page.add(server_queue_time_statistics)
        page.add(slowdown)
        page.add(slowdown_statistics)
        page.add(server_slowdown_statistics)
        page.add(arrival_departure_time_statistics)
        page.add(server_job_statistics)

        path = "./save/" + config['fileName'] + "/seversRecord.json"
        with open(path, 'r') as x:
            seversRecord = json.load(x)

        serverInf = ServerInf(serversRecord=seversRecord, config=config)
        remain_number_statistics=self.remain_number_statistics(serverInf=serverInf)
        remain_size_statistics=self.remain_size_statistics(serverInf=serverInf)
        page.add(remain_number_statistics)
        page.add(remain_size_statistics)

        if (config['ifScreenShot'] != 0):
            path = "./save/" + config['fileName'] + "/queue_time.png"
            make_snapshot(snapshot, queue_time.render(), path)

            path = "./save/" + config['fileName'] + "/queue_time_statistics.png"
            make_snapshot(snapshot, queue_time_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/server_queue_time_statistics.png"
            make_snapshot(snapshot, server_queue_time_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/slowdown.png"
            make_snapshot(snapshot, slowdown.render(), path)

            path = "./save/" + config['fileName'] + "/slowdown_statistics.png"
            make_snapshot(snapshot, slowdown_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/server_slowdown_statistics.png"
            make_snapshot(snapshot, server_slowdown_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/arrival_departure_time_statistics.png"
            make_snapshot(snapshot, arrival_departure_time_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/server_job_statistics.png"
            make_snapshot(snapshot, server_job_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/remain_number_statistics.png"
            make_snapshot(snapshot, remain_number_statistics.render(), path)

            path = "./save/" + config['fileName'] + "/remain_size_statistics.png"
            make_snapshot(snapshot, remain_size_statistics.render(), path)

        page.render("simulate_statistics.html")
        path = "./save/" + config['fileName']
        shutil.copy('simulate_statistics.html', path)
        print("simulate_statistics saved\n")
