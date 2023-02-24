import json
import os
import shutil

from service.service.deployers.abstract import AbstractDeployer


class GoogleDeployer(AbstractDeployer):
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    SERVICE = os.path.join(ROOT, "service")

    def __init__(self, config, *args, **kwargs):
        with open(os.path.join(GoogleDeployer.SERVICE, "status.json"), 'r') as file:
            status = json.load(file)
        self._deployed = status["deployed"]
        print(self._deployed)

    def setup(self, app_name, *args, **kwargs):
        # makedir
        # os.mkdir(GoogleDeployer.SERVICE)
        # copy stuff
        print("Setting up")
        shutil.copyfile(os.path.join(GoogleDeployer.ROOT, "requirements.txt"),
                        os.path.join(GoogleDeployer.SERVICE, "requirements.txt"))

        # shutil.copyfile(os.path.join(GoogleDeployer.SERVICE, "service", "app.py"),
        #                 os.path.join(GoogleDeployer.DEPLOY, app_name))

        with open(os.path.join(GoogleDeployer.SERVICE, "Dockerfile"), 'w') as file:
            file.write(
                f"FROM python:3.9\nWORKDIR /app\nCOPY requirements.txt ./requirements.txt\nRUN pip3 install -r requirements.txt\nEXPOSE 8080\nCOPY . ./\nCMD streamlit run --server.port 8080 --server.enableCORS false {app_name}")

        with open(os.path.join(GoogleDeployer.SERVICE, "app.yaml"), 'w') as file:
            file.write("runtime: custom\nenv: flex")

    def deploy(self, *args, **kwargs):
        print("Deploying")
        os.chdir(GoogleDeployer.SERVICE)
        os.system("gcloud app deploy")
        # shutil.rmtree(GoogleDeployer.DEPLOY)
        with open(os.path.join(GoogleDeployer.SERVICE, "status.json"), 'w') as file:
            json.dump({"deployed": "true"}, file)
