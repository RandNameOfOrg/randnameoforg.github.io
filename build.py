from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
import os
import github

output_folder = '/output/'

env = Environment(loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

gh = github.Github()

info = {
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
    info['projects'].append(project); 
    info['projects_urls'][project] = "/" + project

if not os.path.exists(output_folder):
    print('Creating output folder...')
    os.mkdir(output_folder)
else:
    for file in os.listdir('build_output'):
        os.remove(f'{output_folder}{file}')

for _, _, files in os.walk('templates'):
    for file in files: 
        env.get_template(file).stream(info=info).dump(f'{output_folder}{file}')