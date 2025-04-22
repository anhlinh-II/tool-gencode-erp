import sys
import os
import shutil
import streamlit as st

# Thêm đường dẫn cho các module phụ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_utils.db_browser import connect_database, get_tables, get_columns
from codeGen.generator import generate_entity, generate_controller, generate_service_impl, \
    extract_package_name_from_path, generate_service_interface, generate_repository, generate_mapper, \
    generate_custom_paging_mapper, snake_to_camel
import urllib.parse

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Code Generator Tool", layout="wide")
st.title("🧱 Code Generator Tool")


username = "micro"
password = urllib.parse.quote_plus("Micro@#2025")  # Kết quả: Micro%40%232025
host = "115.146.120.253"
port = 3306
db_name = "miro_erp"

db_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"

if db_url:
    try:
        engine = connect_database(db_url)
        if engine:
            tables = get_tables(engine)
            if not tables:
                st.warning("⚠️ Không tìm thấy bảng nào trong cơ sở dữ liệu.")
            else:
                selected_table = st.selectbox("📋 Chọn bảng", tables)

                if selected_table:
                    columns = get_columns(engine, selected_table)

                    class_name = st.text_input("📁 Nhập tên class", "BusinessUnit")
                    controller_folder = st.text_input("📁 Thư mục sinh Controller", "controller")
                    service_folder = st.text_input("📁 Thư mục sinh Service", "service")
                    impl_folder = os.path.join(service_folder, "impl")
                    repository_folder = st.text_input("📁 Thư mục sinh Repository", "repository")
                    mapper_folder = st.text_input("📁 Thư mục sinh Mapper", "mapper")
                    custom_paging_mapper_folder = st.text_input("📁 Thư mục sinh Custom Paging Mapper", "custom_paging_mapper")

                    if st.button("⚙️ Sinh code"):
                        try:
                            # 🔄 Convert column names + types
                            # processed_fields = []
                            #
                            # for col in columns:  # assuming each col is a dict with 'name' and 'type'
                            #     java_type = map_sql_type_to_java(col["type"])
                            #     camel_name = snake_to_camel(col["name"])
                            #
                            #     processed_fields.append({
                            #         "name": camel_name,
                            #         "type": java_type,
                            #         "original_name": col["name"]
                            #     })

                            custom_paging_mapper_package = extract_package_name_from_path(custom_paging_mapper_folder)

                            generate_controller(class_name, controller_folder)
                            generate_service_interface(class_name, service_folder)
                            generate_service_impl(class_name, impl_folder)
                            generate_repository(class_name, repository_folder)
                            generate_mapper(class_name, mapper_folder)
                            generate_custom_paging_mapper(class_name, custom_paging_mapper_folder)

                            st.success("✅ Đã sinh code Controller và Service thành công!")
                        except ValueError as e:
                            st.error(f"Lỗi: {e}")
        else:
            st.error("❌ Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra URL.")
    except Exception as e:
        st.error(f"❌ Lỗi kết nối hoặc xử lý DB: {e}")
