import click
from .utils.readers import ReaderBinary, ReaderProtobuf
from .utils.connection import Connection
from .utils.protocol import Hello, Config
import requests
import json


def upload_thought(address, data_path, version):
    ip, port = address.split(":")
    try:
        if version == '2':
            reader = ReaderProtobuf(data_path)
        else:
            reader = ReaderBinary(data_path)
        hello = Hello(reader.user)
        json_user_info = hello.to_json()
        session = requests.session()
        session.verify = False
        for snapshot in reader:
            r = session.post(f"http://{address}/config", json=json_user_info)
            config_list = json.loads(r.content)

            snap_json = snapshot.to_json(config_list)

            r = session.post(f"http://{address}/snapshot", json=snapshot.to_json())
            import pdb; pdb.set_trace()

            print(2)

            # with Connection.connect(host=ip, port=int(port)) as con:
            #     con.send(hello.serialize())
            #     conf = Config.deserialize(con.receive())
            #     snap = snapshot.serialize(conf.fields)
            #     con.send(snap)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    pass
