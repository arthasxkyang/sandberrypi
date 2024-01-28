import os

from flask import Flask


def create_app(test_config=None):
    """创建并配置 Flask 应用程序的实例。"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # 应由实例配置覆盖的默认密钥，以保持数据安全
        SECRET_KEY="dev",
        # 将数据库存储在实例文件夹中
        DATABASE=os.path.join(app.instance_path, "sandmakerpi.sqlite"),
    )

    if test_config is None:
        # 不测试时加载实例配置（如果存在）
        app.config.from_pyfile("config.py", silent=True)
    else:
        # 如果传递了测试配置，则加载它
        app.config.update(test_config)

        # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # 注册数据库命令
    from . import db

    db.init_app(app)


    # 注册蓝图
    from . import auth
    from . import main

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # 使 url_for('index') == url_for('blog.index')
    # 在另一个应用程序中，您可以在此处使用 app.route 定义单独的主索引，
    # 同时为 blog 蓝图提供 url_prefix
    app.add_url_rule("/", endpoint="index")

    return app
