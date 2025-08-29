import requests
import click  
import json

# result.json() example
# [
#     ...
#     {
#         'ID': 1,
#         '名前': '大山',
#         '都道府県': '神奈川県',
#         '標高': '1252m',
#     },
#     ...
# ]

def list_mountains():
    """山の一覧を取得して表示する"""
    try:
        response = requests.get(f'{BASE_URL}/mountains/')
        response.raise_for_status()  # エラーがあれば例外を発生させる
        
        mountains = response.json()
        click.echo('--- 山の一覧 ---') # printをclick.echoに変更
        for mountain in mountains:
            click.echo(f"- ID: {mountain['id']}, 名前: {mountain['name']}, 都道府県: {mountain['prefecture']}, 標高: {mountain['elevation']}m")

    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

def create_mountain(name, prefecture, elevation, auth):
    """新しい山を作成する (要認証)"""
    try:
        # Basic認証を使ってリクエストを送信
        response = requests.post(
            f'{BASE_URL}/mountains/',
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
            click.echo(e.response.json(), err=True) # APIからのエラー詳細を表示
    except requests.exceptions.RequestException as e:
        click.echo(f'エラー: APIへの接続に失敗しました。 {e}', err=True)

# --- clickを使ったコマンド定義 ---

@click.group()
def cli():
    """登山記録アプリのAPIクライアント"""
    pass

@cli.group()
def mountains():
    """山に関する操作"""
    pass

@mountains.command(name='list', help='山の一覧を表示。')
def list_command():
    list_mountains()

@mountains.command(name='create', help='新しい山を登録')
@click.option('--name', required=True, help='作成する山の名前')
@click.option('--prefecture', required=True, help='作成する山の都道府県')
@click.option('--elevation', required=True, type=int, help='作成する山の標高')
def create_command(name, prefecture, elevation):
    username = click.prompt('ユーザー名')
    password = click.prompt('パスワード', hide_input=True)
    create_mountain(name, prefecture, elevation, (username, password))


if __name__ == '__main__':
    cli()
