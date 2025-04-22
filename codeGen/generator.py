import os
import re
from jinja2 import Environment, FileSystemLoader

template_dir = 'codeGen/templates'  # Your templates directory path

# List all files in the 'templates' directory
files_in_templates = os.listdir(template_dir)
base_package = "com.micro.stock.business_unit"  # nhập base package tại đây

# Print the files
print("Files in templates directory:")
for file in files_in_templates:
    print(file)

env = Environment(loader=FileSystemLoader('codeGen/templates'))

def to_camel_case(value):
    return value[0].lower() + value[1:] if value else value

env.filters['camel_case'] = to_camel_case

def snake_to_camel(name):
    return ''.join(word.capitalize() for word in name.split('_'))

def map_sql_to_java(sql_type):
    mapping = {
        'varchar': 'String',
        'char': 'String',
        'text': 'String',
        'int': 'Integer',
        'integer': 'Integer',
        'bigint': 'Long',
        'smallint': 'Short',
        'float': 'Float',
        'double': 'Double',
        'decimal': 'BigDecimal',
        'datetime': 'LocalDateTime',
        'timestamp': 'LocalDateTime',
        'date': 'LocalDate',
        'time': 'LocalTime',
        'boolean': 'Boolean',
        'bit': 'Boolean'
    }
    sql_type_str = str(sql_type).lower()

    for key in mapping:
        if key in sql_type_str:
            return mapping[key]

    return "String"  # Default fallback type


def generate_entity(table_name, columns, output_dir):
    class_name = snake_to_camel(table_name)
    cols = []
    for col in columns:
        cols.append({
            'name': col['name'],
            'java_type': map_sql_to_java(col['type'])
        })

    template = env.get_template('entity.java.j2')
    content = template.render(table_name=table_name, class_name=class_name, columns=cols)

    output_path = os.path.join(output_dir)
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, f"{class_name}.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def generate_controller(class_name, output_dir):
    controller_package = extract_package_name_from_path(output_dir)
    template = env.get_template('controller.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=controller_package,
        base_package=base_package
    )

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{class_name}Controller.java")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir

def generate_service_impl(class_name, output_dir):
    service_package = extract_package_name_from_path(output_dir)
    service_interface = f"{class_name}Service"
    repository_name = f"{class_name}Repository"

    template = env.get_template('service_impl.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=service_package,
        base_package=base_package,
        service_interface=service_interface,
        repository_name=repository_name
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{class_name}ServiceImpl.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir

def generate_service_interface(class_name, output_dir):
    impl_package = extract_package_name_from_path(output_dir)

    template = env.get_template('service_interface.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=impl_package,
        base_package=base_package
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{class_name}Service.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir

def generate_repository(class_name, output_dir):
    repository_package = extract_package_name_from_path(output_dir)
    template = env.get_template('repository.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=repository_package,
        base_package=base_package

    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{class_name}Repository.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir

def generate_mapper(class_name, output_dir):
    mapper_package = extract_package_name_from_path(output_dir)

    template = env.get_template('mapper.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=mapper_package,
        base_package=base_package
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{class_name}Mapper.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir

def generate_custom_paging_mapper(class_name, output_dir):
    custom_paging_package_name = extract_package_name_from_path(output_dir)
    template = env.get_template('custom_paging_mapper.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=custom_paging_package_name,
        base_package=base_package
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{class_name}CustomPageToCustomPagingResponseMapper.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir

def generate_domain_model(class_name, fields, output_dir):
    package_name = extract_package_name_from_path(output_dir)
    template = env.get_template('domain_model.java.j2')
    content = template.render(
        model_name=class_name,
        package_name=package_name,
        fields=fields
    )

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{class_name}.java"), 'w', encoding='utf-8') as f:
        f.write(content)

    return output_dir


def extract_package_name_from_path(folder_path):
    # Normalize path để dùng được cả trên Windows lẫn Linux
    norm_path = os.path.normpath(folder_path)
    # Tìm đoạn path bắt đầu từ "com"
    match = re.search(r"(com[\\/].*)", norm_path)
    if not match:
        raise ValueError("Path không chứa thư mục 'com'")
    package_path = match.group(1)
    # Chuyển dấu / hoặc \ thành dấu .
    package_name = package_path.replace("\\", ".").replace("/", ".")
    return package_name
