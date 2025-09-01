# cli.py
import requests
import click
import json

# APIのベースURL (自分の環境に合わせて変更)
BASE_URL = 'http://127.0.0.1:8000'

# --- API呼び出し関数 ---
def list_mountains():
    """山の一覧を取得して表示する"""
    try:
        response = requests.get(f'{BASE_URL}/api/mountains/')
        response.raise_for_status()
        
        mountains = response.json()
        click.echo('--- 山の一覧 ---')
        for mountain in mountains:
            click.echo(f"- ID: {mountain['id']}, 名前: {mountain['name']}, 都道府県: {mountain['prefecture']}, 標高: {mountain['elevation']}m")

    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

def create_mountain(name, prefecture, elevation, auth):
    """新しい山を作成する (要認証)"""
    try:
        response = requests.post(
            f'{BASE_URL}/api/mountains/',
            json={'name': name, 'prefecture': prefecture, 'elevation': elevation},
            auth=auth
        )
        response.raise_for_status()
        
        new_mountain = response.json()
        click.echo(f'成功: 新しい山を作成しました。 ID: {new_mountain["id"]}')

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [401, 403]:
            click.echo('エラー: 認証に失敗しました。ユーザー名またはパスワードが間違っています。', err=True)
        else:
            click.echo(f'エラー: 山の作成に失敗しました。 {e.response.status_code}', err=True)
            click.echo(e.response.json(), err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

def list_records():
    """登山記録の一覧を取得して表示する"""
    try:
        response = requests.get(f'{BASE_URL}/api/records/')
        response.raise_for_status()
        
        records = response.json()
        click.echo('--- 登山記録の一覧 ---')
        for record in records:
            click.echo(f"- ID: {record['id']}, UserID: {record['user']}, MountainID: {record['mountain']}, Comment: {record['comment'][:20]}...")

    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

def create_record(mountain_id, climb_date, comment, auth):
    """新しい登山記録を作成する (要認証)"""
    try:
        response = requests.post(
            f'{BASE_URL}/api/records/',
            json={'mountain': mountain_id, 'climb_date': climb_date, 'comment': comment},
            auth=auth
        )
        response.raise_for_status()
        
        new_record = response.json()
        click.echo(f'成功: 新しい登山記録を作成しました。 ID: {new_record["id"]}')

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [401, 403]:
            click.echo('エラー: 認証に失敗しました。ユーザー名またはパスワードが間違っています。', err=True)
        else:
            click.echo(f'エラー: 記録の作成に失敗しました。 {e.response.status_code}', err=True)
            click.echo(e.response.json(), err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)


def list_users(auth):
    """ユーザーの一覧を取得して表示する (要認証)"""
    try:
        response = requests.get(f'{BASE_URL}/api/users/', auth=auth)
        response.raise_for_status()
        
        users = response.json()
        click.echo('--- ユーザーの一覧 ---')
        for user in users:
            click.echo(f"- ID: {user['id']}, ユーザー名: {user['username']}, Email: {user['email']}")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [401, 403]:
            click.echo('エラー: 認証に失敗したか、一覧表示の権限がありません。', err=True)
        elif e.response.status_code == 404:
            click.echo('エラー: /api/users/ エンドポイントが見つかりません。Django側の設定を確認してください。', err=True)
        else:
            click.echo(f'エラー: ユーザー一覧の取得に失敗しました。 {e.response.status_code}', err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

def create_user(username, email, password):
    """新しいユーザーを作成する"""
    try:
        response = requests.post(
            f'{BASE_URL}/api/register/',
            json={'username': username, 'email': email, 'password': password},
        )
        response.raise_for_status()
        
        new_user = response.json()
        click.echo(f"成功: 新しいユーザー '{new_user['username']}' を作成しました。")

    except requests.exceptions.HTTPError as e:
        click.echo(f'エラー: ユーザーの作成に失敗しました。 ({e.response.status_code})', err=True)
        try:
            errors = e.response.json()
            for field, messages in errors.items():
                click.echo(f"- {field}: {', '.join(messages)}", err=True)
        except json.JSONDecodeError:
            click.echo("サーバーから不明なエラーが返されました。", err=True)
            
    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

# --- clickを使ったコマンド定義 ---

@click.group()
def cli():
    """登山記録アプリのAPIクライアント"""
    pass

@cli.command(name='Mt_list', help='山の一覧を表示します。')
def mountain_list_command():
    list_mountains()

@cli.command(name='Mt_create', help='新しい山を登録します。')
@click.option('--name', required=True, help='作成する山の名前')
@click.option('--prefecture', required=True, help='作成する山の都道府県')
@click.option('--elevation', required=True, type=int, help='作成する山の標高')
def mountain_create_command(name, prefecture, elevation):
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    create_mountain(name, prefecture, elevation, (username, password))

@cli.command(name='rec_list', help='登山記録の一覧を表示します。')
def record_list_command():
    list_records()

@cli.command(name='rec_create', help='新しい登山記録を登録します。')
@click.option('--mountain-id', required=True, type=int, help='記録対象の山のID')
@click.option('--date', 'climb_date', required=True, help='登った日付 (YYYY-MM-DD)')
@click.option('--comment', default="", help='感想やコメント')
def record_create_command(mountain_id, climb_date, comment):
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    create_record(mountain_id, climb_date, comment, (username, password))

@cli.command(name='user_list', help='ユーザーの一覧を表示します。(要管理者権限)')
def user_list_command():
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    list_users((username, password))

@cli.command(name='user_create', help='新しいユーザーを登録します。')
@click.option('--username', required=True, help='登録するユーザー名')
@click.option('--email', required=True, help='登録するメールアドレス')
def user_create_command(username, email):
    password = click.prompt('パスワード', hide_input=True, confirmation_prompt=True)
    create_user(username, email, password)

if __name__ == '__main__':
    cli()
