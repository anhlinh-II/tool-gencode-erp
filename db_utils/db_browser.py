from sqlalchemy import create_engine, inspect

def connect_database(db_url: str):
    engine = create_engine(db_url)

    try:
        with engine.connect() as conn:
            print("✅ Kết nối MySQL thành công!")
            return engine
    except Exception as e:
        print("❌ Lỗi kết nối:", e)
        return None

def get_tables(engine):
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        print("Lỗi lấy bảng:", e)
        return []

def get_columns(engine, table_name):
    try:
        inspector = inspect(engine)
        return inspector.get_columns(table_name)
    except Exception as e:
        print("Lỗi lấy cột:", e)
        return []