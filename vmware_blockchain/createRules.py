from jinja2 import Template, Environment, FileSystemLoader
from pprint import pprint

# Create metrics list
def get_metrics_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


# Module entrypoint
if __name__ == "__main__":
    metrics_list_filename = 'metrics_list.txt'
    rules_template_filename = 'rules.tmpl'
    preprocessor_rules_filename = 'preprocessor_rules.yaml'
    metrics_list = get_metrics_list(metrics_list_filename)

    # Get template file
    file_loader = FileSystemLoader('')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(rules_template_filename)

    # Render output from template
    result = template.render(metrics=metrics_list)

    # Prepare preprocessor rules file
    # pprint(result)
    with open(preprocessor_rules_filename, 'w') as file:
        for line in result:
            file.write(line)
