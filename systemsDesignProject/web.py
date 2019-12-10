import sys
from pathlib import Path
from website import Website

_INDEX_HTML = '''<html>
                    <head></head>
                    <body>
                        <ul>
    {users}
                        </ul>
                    </body>
                </html>
                '''
_USER_LINE_HTML = '''                        <li><a href="/users/{user_id}">user {user_id}</a></li>'''

_SINGLE_THOUGHT_HTML = '''            <tr>
                <td>{time}</td>
                <td>{thought}</td>
            </tr>
'''

_INDEX_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {user_thoughts}
        </table>
    </body>
</html>

'''


def run_webserver(address, data_dir):
    website = Website()

    @website.route('/')
    def index():
        users_html = []
        p = Path(data_dir)
        for user_dir in p.iterdir():
            users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
        return 200, _INDEX_HTML.format(users='\n'.join(users_html))

    @website.route('/users/([0-9]+)')
    def user(user_id):
        users_html = []
        p = Path(fr"{data_dir}/{user_id}")
        for file in p.iterdir():
            if ".txt" in file.name:  # file.name is the name of the file. "file" itself returns the full path
                with open(f"{file}", "r") as f:
                    thought_time = file.name.split(".")[0]
                    users_html.append(_SINGLE_THOUGHT_HTML.format(time=thought_time, thought=f.read()))
        return 200, _INDEX_USER_HTML.format(user_thoughts='\n'.join(users_html), user_id=user_id)

    website.run(address)


def main(argv):
    # Check arguments:
    if len(argv) < 2 or type(argv[1]) is not str or type(argv[2]) is not str:
        print("arguments error. exiting")
        return 1
    ip, port = argv[1].split(":")
    try:
        run_webserver((ip, int(port)), argv[2])
    except Exception as e:
        print("run server returned with an error.", e)
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
