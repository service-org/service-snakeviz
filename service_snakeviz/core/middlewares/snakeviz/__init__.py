#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import os
import tempfile
import typing as t

from pstats import Stats
from jinja2 import Environment
from werkzeug.routing import Map
from werkzeug.routing import Rule
from jinja2 import FileSystemLoader
from werkzeug.wsgi import get_path_info
from service_snakeviz.core.stats import table_rows
from service_snakeviz.core.stats import json_stats
from service_core.core.service.entrypoint import Entrypoint
from werkzeug.middleware.shared_data import SharedDataMiddleware
from service_webserver.core.middlewares.base import BaseMiddleware

if t.TYPE_CHECKING:
    # 由于其定义在存根文件所以需要在TYPE_CHECKING下
    from werkzeug.wsgi import WSGIApplication
    from werkzeug.wsgi import WSGIEnvironment
    from werkzeug.wrappers.response import StartResponse


class SnakeVizMiddleware(BaseMiddleware):
    """ 性能可视化中间件类 """

    def __init__(self, *, wsgi_app: WSGIApplication, producer: Entrypoint, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param wsgi_app: 应用程序
        @param producer: 服务提供者
        @param kwargs: 命名参数
        """
        curr_file_dir = os.path.dirname(__file__)
        static_path = os.path.join(curr_file_dir, 'static')
        self.static_url = '/snakeviz/static'
        self.pstats_url = '/snakeviz/pstats'
        self.pstats_map = Map([Rule(f'{self.pstats_url}/<file_name>')])
        kwargs.setdefault('exports', {}).update({self.static_url: static_path})
        BaseMiddleware.__init__(self, wsgi_app=wsgi_app, producer=producer)
        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, **kwargs)
        templates_path = os.path.join(curr_file_dir, 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(templates_path), autoescape=True)

    def render_template(self, template_name, **context) -> t.Text:
        """ 渲染jinja模版内容

        @param template_name: 文件名
        @param context: 上下文字典
        @return: t.Text
        """
        return self.jinja_env.get_template(template_name).render(context)

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> t.Iterable[bytes]:
        """ 请求处理器

        @param environ: 环境对象
        @param start_response: 响应对象
        @return: t.Iterable[bytes]
        """
        reqpath = get_path_info(environ)
        adapter = self.pstats_map.bind_to_environ(environ)
        if adapter.test(reqpath, method='GET'):
            start_response('200 Ok', [('Content-Type', 'text/html')])
            endpoint, path_values = adapter.match()
            file_name = path_values['file_name']
            file_path = os.path.join(tempfile.gettempdir(), file_name)
            stats = Stats(file_path)
            table_rows_data = table_rows(stats)
            json_stats_data = json_stats(stats)
            context = {'profile_name': file_name, 'table_rows': table_rows_data, 'callees': json_stats_data}
            return [self.render_template('index.html', **context).encode()]
        return self.wsgi_app(environ, start_response)  # type: ignore
