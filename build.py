from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
import os

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

info = {
    'projects': ['test1', 'test2', 'test3'],
    'projects_urls': {
        'test1': 'test1',
        'test2': 'test2',
        'test3': 'test3'
    }
}

for file in os.listdir('build_output'):
    os.remove(f'build_output\\{file}')

for _, _, files in os.walk('templates'):
    for file in files: 
        rendered = env.get_template(file).stream(info=info).dump(f'build_output\\{file}')