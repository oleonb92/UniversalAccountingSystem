import sys
import os
from sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy import create_engine, MetaData

# Agrega la ruta raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.models import Base

# Conecta a la base de datos existente
engine = create_engine("sqlite:///data/universal_finances.db")
Base.metadata.create_all(engine)

# Refleja todas las tablas
metadata = MetaData()
metadata.reflect(bind=engine)

# Genera el gráfico (usando versión simplificada de la función)
graph = create_uml_graph(Base.registry.mappers)

# Exporta a PDF
graph.write_pdf("universal_accounting_erd.pdf")
print("✅ ERD generado exitosamente: universal_accounting_erd.pdf")