import os
import shutil

from CentralSystem import CentralSystem
from JobsArrive import JobsArrive
from DrawGraphic import DrawGraphic
import json


def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


with open('config.json', 'r') as x:
    config = json.load(x)

path = "./save/" + config['fileName']
folder = os.path.exists(path)
if not folder:
    os.makedirs(path)
delete_files_in_folder(path)

path = "./save/" + config['fileName'] + "/config.json"
with open(path, "w") as f:
    json.dump(config, f)
print("config saved")
print()

drawGraphic = DrawGraphic()
if config['useOtherComingJobs'] == "":
    jobsArrive = JobsArrive(config)
    drawGraphic.draw_job_arrival(jobsArrive, config)
else:
    pathFrom = "./save/" + config['useOtherComingJobs'] + "/arrival_jobs_statistics.html"
    pathTo = "./save/" + config['fileName']
    shutil.copy(pathFrom, pathTo)
    pathFrom = "./save/" + config['useOtherComingJobs'] + "/jobsArrival.json"
    pathTo = "./save/" + config['fileName']
    shutil.copy(pathFrom, pathTo)

# for i in range(1,config['system']['serverNumber']):
#     path="./save/" + config['fileName']+"/server"+str(i)+"Record.json"
#     file = open(path, 'w')
#     file.close()

centralSystem = CentralSystem(config)

drawGraphic.draw_simulate(config)
