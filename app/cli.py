# cli.py
import requests
import click
import json

# APIのベースURL (自分の環境に合わせて変更)
BASE_URL = 'http://127.0.0.1:8000'

# --- API呼び出し関数 ---

def handle_api_error(e):
    """APIエラーを共通で処理するヘルパー関数"""
    if isinstance(e, requests.exceptions.HTTPError):
        status_code = e.response.status_code
        if status_code in [401, 403]:
            click.echo('エラー: 認証に失敗したか、この操作を行う権限がありません。', err=True)
        elif status_code == 404:
            click.echo('エラー: 指定されたリソースが見つかりませんでした (404)。IDを確認してください。', err=True)
        else:
            click.echo(f'エラー: APIから予期せぬ応答がありました。 ({status_code})', err=True)
            try:
                # APIからの詳細なエラーメッセージを表示
                errors = e.response.json()
                for field, messages in errors.items():
                    click.echo(f"- {field}: {', '.join(messages)}", err=True)
            except json.JSONDecodeError:
                click.echo("サーバーから不明なエラーが返されました。", err=True)
    elif isinstance(e, requests.exceptions.RequestException):
        click.echo(f'エラー: APIへの接続に失敗しました。サーバーが起動しているか確認してください。 {e}', err=True)
    else:
        click.echo(f'予期せぬエラーが発生しました: {e}', err=True)

# --- Mountain Functions ---
def list_mountains():
    try:
        response = requests.get(f'{BASE_URL}/api/mountains/')
        response.raise_for_status()
        mountains = response.json()
        click.echo('--- 山の一覧 ---')
        for m in mountains:
            click.echo(f"- ID: {m['id']}, 名前: {m['name']}, 都道府県: {m['prefecture']}, 標高: {m['elevation']}m")
    except Exception as e:
        handle_api_error(e)

def get_mountain_detail(mountain_id):
    try:
        response = requests.get(f'{BASE_URL}/api/mountains/{mountain_id}/')
        response.raise_for_status()
        mountain = response.json()
        click.echo('--- 山の詳細 ---')
        click.echo(json.dumps(mountain, indent=2, ensure_ascii=False))
    except Exception as e:
        handle_api_error(e)

def create_mountain(name, prefecture, elevation, auth):
    try:
        response = requests.post(f'{BASE_URL}/api/mountains/', json={'name': name, 'prefecture': prefecture, 'elevation': elevation}, auth=auth)
        response.raise_for_status()
        new_mountain = response.json()
        click.echo(f'成功: 新しい山を作成しました。 ID: {new_mountain["id"]}')
    except Exception as e:
        handle_api_error(e)

def update_mountain(mountain_id, data, auth):
    try:
        response = requests.patch(f'{BASE_URL}/api/mountains/{mountain_id}/', json=data, auth=auth)
        response.raise_for_status()
        updated = response.json()
        click.echo(f'成功: ID {mountain_id} の山を更新しました。')
        click.echo(json.dumps(updated, indent=2, ensure_ascii=False))
    except Exception as e:
        handle_api_error(e)

def delete_mountain(mountain_id, auth):
    try:
        response = requests.delete(f'{BASE_URL}/api/mountains/{mountain_id}/', auth=auth)
        response.raise_for_status()
        click.echo(f'成功: ID {mountain_id} の山を削除しました。')
    except Exception as e:
        handle_api_error(e)

# --- Record Functions ---
def list_records():
    try:
        response = requests.get(f'{BASE_URL}/api/records/')
        response.raise_for_status()
        records = response.json()
        click.echo('--- 登山記録の一覧 ---')
        for r in records:
            click.echo(f"- ID: {r['id']}, UserID: {r['user']}, MountainID: {r['mountain']}, Comment: {r['comment'][:20]}...")
    except Exception as e:
        handle_api_error(e)

def get_record_detail(record_id):
    try:
        response = requests.get(f'{BASE_URL}/api/records/{record_id}/')
        response.raise_for_status()
        record = response.json()
        click.echo('--- 登山記録の詳細 ---')
        click.echo(json.dumps(record, indent=2, ensure_ascii=False))
    except Exception as e:
        handle_api_error(e)

def create_record(mountain_id, climb_date, comment, auth):
    try:
        response = requests.post(f'{BASE_URL}/api/records/', json={'mountain': mountain_id, 'climb_date': climb_date, 'comment': comment}, auth=auth)
        response.raise_for_status()
        new_record = response.json()
        click.echo(f'成功: 新しい登山記録を作成しました。 ID: {new_record["id"]}')
    except Exception as e:
        handle_api_error(e)

def update_record(record_id, data, auth):
    try:
        response = requests.patch(f'{BASE_URL}/api/records/{record_id}/', json=data, auth=auth)
        response.raise_for_status()
        updated = response.json()
        click.echo(f'成功: ID {record_id} の記録を更新しました。')
        click.echo(json.dumps(updated, indent=2, ensure_ascii=False))
    except Exception as e:
        handle_api_error(e)

def delete_record(record_id, auth):
    try:
        response = requests.delete(f'{BASE_URL}/api/records/{record_id}/', auth=auth)
        response.raise_for_status()
        click.echo(f'成功: ID {record_id} の記録を削除しました。')
    except Exception as e:
        handle_api_error(e)

# --- User Functions ---
def list_users(auth):
    try:
        response = requests.get(f'{BASE_URL}/api/users/', auth=auth)
        response.raise_for_status()
        users = response.json()
        click.echo('--- ユーザーの一覧 ---')
        for u in users:
            click.echo(f"- ID: {u['id']}, ユーザー名: {u['username']}, Email: {u['email']}")
    except Exception as e:
        handle_api_error(e)

def create_user(username, email, password):
    try:
        response = requests.post(f'{BASE_URL}/api/register/', json={'username': username, 'email': email, 'password': password})
        response.raise_for_status()
        new_user = response.json()
        click.echo(f"成功: 新しいユーザー '{new_user['username']}' を作成しました。")
    except Exception as e:
        handle_api_error(e)

# --- CLI Commands ---
@click.group()
def cli():
    pass

# Mountain Commands
@cli.command(help='山の一覧を表示します。')
def Mt_list():
    list_mountains()

@cli.command(help='指定したIDの山の詳細を表示します。')
@click.option('--id', 'mountain_id', required=True, type=int)
def Mt_detail(mountain_id):
    get_mountain_detail(mountain_id)

@cli.command(help='新しい山を登録します。')
@click.option('--name', required=True)
@click.option('--prefecture', required=True)
@click.option('--elevation', required=True, type=int)
def Mt_create(name, prefecture, elevation):
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    create_mountain(name, prefecture, elevation, (username, password))

@cli.command(help='指定したIDの山の情報を更新します。')
@click.option('--id', 'mountain_id', required=True, type=int)
@click.option('--name')
@click.option('--prefecture')
@click.option('--elevation', type=int)
def Mt_update(mountain_id, name, prefecture, elevation):
    data = {k: v for k, v in {'name': name, 'prefecture': prefecture, 'elevation': elevation}.items() if v is not None}
    if not data:
        click.echo('エラー: 更新するデータが指定されていません。', err=True)
        return
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    update_mountain(mountain_id, data, (username, password))

@cli.command(help='指定したIDの山を削除します。')
@click.option('--id', 'mountain_id', required=True, type=int)
def Mt_delete(mountain_id):
    click.confirm(f'本当にID {mountain_id} の山を削除しますか？', abort=True)
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    delete_mountain(mountain_id, (username, password))

# Record Commands
@cli.command(help='登山記録の一覧を表示します。')
def rec_list():
    list_records()

@cli.command(help='指定したIDの登山記録の詳細を表示します。')
@click.option('--id', 'record_id', required=True, type=int)
def rec_detail(record_id):
    get_record_detail(record_id)

@cli.command(help='新しい登山記録を登録します。')
@click.option('--mountain-id', required=True, type=int)
@click.option('--date', 'climb_date', required=True, help='YYYY-MM-DD')
@click.option('--comment', default="")
def rec_create(mountain_id, climb_date, comment):
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    create_record(mountain_id, climb_date, comment, (username, password))

@cli.command(help='指定したIDの登山記録を更新します。')
@click.option('--id', 'record_id', required=True, type=int)
@click.option('--date', 'climb_date', help='YYYY-MM-DD')
@click.option('--comment')
def rec_update(record_id, climb_date, comment):
    data = {k: v for k, v in {'climb_date': climb_date, 'comment': comment}.items() if v is not None}
    if not data:
        click.echo('エラー: 更新するデータが指定されていません。', err=True)
        return
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    update_record(record_id, data, (username, password))

@cli.command(help='指定したIDの登山記録を削除します。')
@click.option('--id', 'record_id', required=True, type=int)
def rec_delete(record_id):
    click.confirm(f'本当にID {record_id} の記録を削除しますか？', abort=True)
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    delete_record(record_id, (username, password))

# User Commands
@cli.command(name='user_list', help='ユーザーの一覧を表示します。(要管理者権限)')
def user_list_command():
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    list_users((username, password))

@cli.command(name='user_create', help='新しいユーザーを登録します。')
@click.option('--username', required=True)
@click.option('--email', required=True)
def user_create_command(username, email):
    password = click.prompt('パスワード', hide_input=True, confirmation_prompt=True)
    create_user(username, email, password)


if __name__ == '__main__':
    cli()

