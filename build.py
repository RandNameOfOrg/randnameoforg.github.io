import os
import shutil
from pathlib import Path

import github
from jinja2 import Environment, FileSystemLoader, select_autoescape

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

def main():
    for project in list_of_projects():
        info['projects'].append(project)
        info['projects_urls'][project] = "/" + project

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for dirpath, dirnames, filenames in os.walk(output_folder):
        dirpath = Path(dirpath)
        if ".well-known" in str(dirpath):
            continue
        try:
            for fn in filenames:
                os.remove(dirpath / fn)
            for dirs in dirnames:
                if dirs != ".well-known":
                    shutil.rmtree(dirpath / dirs)
        except FileNotFoundError:
            continue

    for _, _, files in os.walk('templates'):
        for file in files:
            env.get_template(file).stream(info=info).dump(str(output_folder / file))

    # copy static files
    if not os.path.exists(output_folder / "static"):
        os.mkdir(output_folder / "static")

    for dirpath, dirnames, filenames in os.walk(Path('static').absolute()):
        dirpath = Path(dirpath)
        for fn in filenames:
            shutil.copyfile(dirpath / fn, str(output_folder / "static" / fn))


if __name__ == "__main__":
    # try:
        main()
    # except KeyboardInterrupt:
    #     exit(0)
    # except Exception as e:
    #     print(e)
    #     exit(-1)
    