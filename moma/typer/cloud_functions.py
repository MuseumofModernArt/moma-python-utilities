import asyncio
import base64
import json
import os
import pprint
import psutil
import requests
import sys
import typer

from signal import SIGINT, SIGTERM
from typing_extensions import Annotated

_pp = pprint.PrettyPrinter(indent=2, stream=sys.stdout)

app = typer.Typer()

@app.command()
def run_local(name,
              port: Annotated[int, typer.Option("--port", "-p")]=8043,
              project: Annotated[str, typer.Option("--project", "-j")]='moma-apps-local',
              subscription: Annotated[str, typer.Option("--subscription", "-S")]='my-sub',
              topic: Annotated[str, typer.Option("--topic", "-t")]='my-topic',
              s_port: Annotated[int, typer.Option("--subscriber-port", "-s")]=8080
              ):
    asyncio.run(_run_local(name, port, project, subscription, topic, s_port))

async def _run_local(name, port, project, subscription, topic, s_port):
    config = cloud_function_config(name)
    function_name = config['functionName']
    environment = (f'FUNCTION_NAME={function_name}\n'
                   f'PROJECT={project}\n'
                   f'PORT={port}\n'
                   f'TOPIC={topic}\n'
                   f'SUBSCRIPTION={subscription}\n'
                   f'S_PORT={s_port}\n')

    dir = os.path.join(os.getcwd(), config['directory'])
    tmp_path = os.path.join(dir, 'tmp')

    os.makedirs(tmp_path, exist_ok=True)
    env_file = os.path.join(tmp_path, '.env')
    with open(env_file, 'w+') as f:
        f.write(environment)

    print(f'running -- honcho -d cloud-functions/ -f HProcfile -e {env_file} start')

    proc = await asyncio.create_subprocess_shell(
        f'honcho -d cloud-functions/ -f HProcfile -e {env_file} start'
    )
    await proc.communicate()

@app.command()
def list():
    for cfunc in cloud_functions_config():
        print(cfunc['functionName'] + ' ' + cfunc['alias'])

@app.command()
def config(name):
    config = cloud_function_config(name)
    _pp.pprint(config)

@app.command()
def start_pubsub(name,
                 port: Annotated[int, typer.Option("--port", "-p")]=8043,
                 project: Annotated[str, typer.Option("--project", "-j")]='moma-apps-local',
                 subscription: Annotated[str, typer.Option("--subscription", "-S")]='my-sub',
                 topic: Annotated[str, typer.Option("--topic", "-t")]='my-topic',
                 s_port: Annotated[int, typer.Option("--subscriber-port", "-s")]=8080,
                 init: Annotated[bool, typer.Option("--init", "-i")]=False
                 ):
    asyncio.run(_start_pubsub(name, port, project, subscription, topic, s_port, init))

async def _start_pubsub(name, port, project, subscription, topic, s_port, init):
    config = cloud_function_config(name)
    dir = os.path.join(os.getcwd(), config['directory'])

    tmp_path = os.path.join(dir, 'tmp')
    port_file = os.path.join(tmp_path, 'port')
    os.makedirs(tmp_path, exist_ok=True)
    with open(port_file, 'w+') as f:
        f.write(str(port))

    def shutdown():
        _shutdown_pubsub(port, port_file)

    loop = asyncio.get_event_loop()
    for signal in [SIGINT, SIGTERM]:
       loop.add_signal_handler(signal, shutdown)

    try:
        await _run_tasks(port, project, subscription, topic, s_port, init)
    except KeyboardInterrupt:
        pass
    finally:
        shutdown()

async def _run_tasks(port, project, subscription, topic, s_port, init):
    tasks = [asyncio.create_task(_run_pubsub(project, port))]
    if init:
        tasks.append(asyncio.create_task(_init_pubsub(subscription, topic, port, project, s_port)))
    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)


async def _run_pubsub(project, port):
    proc = await asyncio.create_subprocess_shell(
        f"gcloud beta emulators pubsub start --project={project} --host-port='localhost:{port}'"
    )
    await proc.communicate()

async def _init_pubsub(subscription, topic, port, project, s_port):
    await asyncio.sleep(2)
    await _create_topic(port, project, topic)
    await _create_subscription(port, project, topic, subscription, s_port)

def _shutdown_pubsub(port, port_file):
    print('Shutting down')

    if os.path.exists(port_file):
        os.remove(port_file)

    (pid, _) = get_pid_for_port(port)
    if not pid is None:
        psutil.Process(pid).kill()

    print('Shutdown complete')


@app.command()
def create_topic(topic, port: Annotated[int, typer.Option("--port", "-p")]=8043, project: Annotated[str, typer.Option("--project", "-j")]='moma-apps-local'):
    asyncio.run(_create_topic(port, project, topic))

async def _create_topic(port, project, topic):
    put_topic(port, project, topic)

def put_topic(port, project, topic):
    url = f'http://localhost:{port}/v1/projects/{project}/topics/{topic}'
    return requests.put(url)

@app.command()
def create_subscription(subscription,
                        topic, port: Annotated[int, typer.Option("--port", "-p")]=8043,
                        project: Annotated[str, typer.Option("--project", "-j")]='moma-apps-local',
                        s_port: Annotated[int, typer.Option("--subscriber-port", "-s")]=8080
                        ):
    asyncio.run(_create_subscription(port, project, topic, subscription, s_port))

async def _create_subscription(port, project, topic, subscription, s_port):
    put_subscription(port, project, topic, subscription, s_port)

def put_subscription(port, project, topic, subscription, s_port):
    url = f'http://localhost:{port}/v1/projects/{project}/subscriptions/{subscription}'
    headers = { 'Content-Type': 'application/json' }
    fq_topic = f'projects/{project}/topics/{topic}'
    payload = {
        'topic': fq_topic,
        'pushConfig': {
            'pushEndpoint': f'http://localhost:{s_port}/{fq_topic}'
        }
    }
    return requests.put(url, headers=headers, data=json.dumps(payload))

@app.command()
def build(name):
    asyncio.run(_build(name))

async def _build(name):
    config = cloud_function_config(name)
    dir = config['directory']
    function_name = config['functionName']
    builder = 'gcr.io/buildpacks/builder:v1'
    function_type = 'GOOGLE_FUNCTION_SIGNATURE_TYPE=event'
    entry_point = config['entryPoint']
    target = f'GOOGLE_FUNCTION_TARGET={entry_point}'

    proc = await asyncio.create_subprocess_shell(
        f'pack build -p {dir} --builder {builder} --env {function_type} --env {target} {function_name}'
    )
    await proc.communicate()

@app.command()
def run_client(name, port: Annotated[int, typer.Option("--port", "-p")]=8080, build: Annotated[bool, typer.Option("--build", "-b")]=False):
    asyncio.run(_run_client(name, port, build))

async def _run_client(name, port, build):
    config = cloud_function_config(name)
    mount = 'type=bind,source=${HOME}/.config/gcloud,target=/app/.config/gcloud'
    function_name = config['functionName']
    credentials = 'GOOGLE_APPLICATION_CREDENTIALS="/app/.config/gcloud/application_default_credentials.json"'

    if build:
        await _build(name)

    print(f'Running {function_name}')

    proc = await asyncio.create_subprocess_shell(
        f'docker run -e VERBOSE=TRUE -e {credentials} -ePORT={port} --mount {mount} --rm -p {port}:{port} {function_name}'
    )
    await proc.communicate()

@app.command()
def publish(
    topic, payload,
    port: Annotated[int, typer.Option("--port", "-p")]=8043,
    project: Annotated[str, typer.Option("--project", "-j")]='moma-apps-local',
    ):
    url = f'http://localhost:{port}/v1/projects/{project}/topics/{topic}:publish'
    headers = { 'Content-Type': 'application/json' }
    data = ""
    with open(payload) as f:
        data = base64.b64encode(json.dumps(json.load(f)).encode()).decode()

    payload = {
        "messages": [{
            "data": data
        }]
    }
    requests.post(url, headers=headers, data=json.dumps(payload))

@app.command()
def create(
    name,
    project: Annotated[str, typer.Option("--project", "-j")]='moma-apps-staging',
    region: Annotated[str, typer.Option("--region", "-r")]='us-east4',
    topic: Annotated[str, typer.Option("--topic", "-t")]='',
    retry=False,
):
    asyncio.run(_create(name, project, region, topic, retry))

async def _create(name, project, region, topic, retry):
    func_name = f'{topic}-{name}'

    options = [
        f'--gen2',
        f'--project {project}',
        f'--region {region}',
        f'--trigger-topic={topic}',
        f'--runtime=python312',
        f'--entry-point=main',
        f'--source=cloud-functions/{topic}/{name}',]

    if retry:
        options.append('--retry')

    proc = await asyncio.create_subprocess_shell(
        f'gcloud functions deploy {func_name} {' '.join(options)}'
    )
    await proc.communicate()

_cloud_functions_config = None
def cloud_functions_config():
    global _cloud_functions_config
    if not _cloud_functions_config is None:
        return _cloud_functions_config

    with open('.vscode/launch.json') as f:
        launch_configurations = json.load(f)
        _cloud_functions_config = []

        i = 1
        for cfunc in launch_configurations['configurations']:
            if cfunc['type'] == 'cloudcode.cloudfunctions':
                cfunc['alias'] = f'f{i}'
                _cloud_functions_config.append(cfunc)
                i += 1

        return _cloud_functions_config

def cloud_function_config(name):
    for config in cloud_functions_config():
        if config['functionName'] == name or config['alias'] == name:
            return config
    return None

def get_pid_for_port(port):
    connections = psutil.net_connections()
    for con in connections:
        if (
            con.raddr != tuple() and con.raddr.port == port
           ) or (
            con.laddr != tuple() and con.laddr.port == port
           ):
            _pp.pprint(con)

    for con in connections:
        if con.raddr != tuple():
            if con.raddr.port == port and con.status == 'LISTEN':
                return con.pid, con.status
        if con.laddr != tuple():
            if con.laddr.port == port and con.status == 'LISTEN':
                return con.pid, con.status
    return None, None