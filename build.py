from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import github

output_folder = Path('build_output').absolute()
env = Environment(loader=FileSystemLoader('templates'),
                  autoescape=select_autoescape(['html', 'xml'])
                  )

gh = github.Github()

info = {
    "base_url": "https://github.com/RandNameOfOrg",
    'projects': [], 'projects_urls': {}
}


def list_of_projects() -> list:
    repos = gh.get_organization("RandNameOfOrg").get_repos()
    non_forks = []
    for repo in repos:
        if repo.fork is False:
            non_forks.append(repo.name)
    return non_forks


for project in list_of_projects():
    info['projects'].append(project)
    info['projects_urls'][project] = "/" + project

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

for dirpath, dirnames, filenames in os.walk(output_folder):
    if ".well-known" in dirpath:
        continue
    for fn in filenames:
        os.remove(dirpath + "\\" + fn)
    for dirs in dirnames:
        if dirs != ".well-known":
            os.removedirs(dirpath + "\\" + dirs)

for _, _, files in os.walk('templates'):
    for file in files:
        env.get_template(file).stream(info=info).dump(f'{output_folder}\\{file}')
