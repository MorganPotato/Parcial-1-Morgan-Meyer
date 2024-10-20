from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#
Base = declarative_base()


#inicio del programa
class Articulo(Base):
    __tablename__ = 'articulos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, nullable=False)
    desc = Column(String)
    pre = Column(Float, nullable=False)


# Conexion a la base de datos SQLite
engine = create_engine('sqlite:///recetas.db')
Base.metadata.create_all(engine)

# Crear una sesion
Session = sessionmaker(bind=engine)
session = Session()


# Funcion para agregar articulos
def agregar_articulo(nom, desc, pre):
    nuevo_articulo = Articulo(nom=nom, desc=desc, pre=pre)
    session.add(nuevo_articulo)
    session.commit()
    print("Articulo agregado exitosamente.")


# Funcion para buscar articulos
def buscar_articulo(nom):
    resultados = session.query(Articulo).filter(Articulo.nom.like(f'%{nom}%')).all()
    if resultados:
        for articulo in resultados:
            print(f"ID: {articulo.id}, Nom: {articulo.nom}, Desc: {articulo.desc}, Pre: {articulo.pre}")
    else:
        print("No se encontraron articulos.")


# Funcion para editar articulos
def editar_articulo(id_articulo, nom=None, desc=None, pre=None):
    articulo = session.query(Articulo).filter_by(id=id_articulo).first()
    if articulo:
        if nom:
            articulo.nom = nom
        if desc:
            articulo.desc = desc
        if pre:
            articulo.pre = pre
        session.commit()
        print("Articulo actualizado exitosamente.")
    else:
        print("Articulo no encontrado.")


# Funcion para eliminar articulos
def eliminar_articulo(id_articulo):
    articulo = session.query(Articulo).filter_by(id=id_articulo).first()
    if articulo:
        session.delete(articulo)
        session.commit()
        print("Articulo eliminado exitosamente.")
    else:
        print("Articulo no encontrado.")


# Menu de la aplicacion
def menu():
    while True:
        print("\n--- Menu del Sistema de Registro de Presupuesto en Cocina ---")
        print("1. Registrar un nuevo articulo")
        print("2. Buscar un articulo")
        print("3. Editar un articulo")
        print("4. Eliminar un articulo")
        print("5. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == '1':
            nom = input("Nom del articulo: ")
            desc = input("Desc del articulo: ")
            pre = float(input("Pre del articulo: "))
            agregar_articulo(nom, desc, pre)

        elif opcion == '2':
            nom = input("Ingrese el nom del articulo a buscar: ")
            buscar_articulo(nom)

        elif opcion == '3':
            id_articulo = int(input("Ingrese el ID del articulo a editar: "))
            print("Deje el campo vacio si no desea cambiarlo.")
            nom = input("Nuevo nom (opcional): ") or None
            desc = input("Nueva desc (opcional): ") or None
            pre = input("Nuevo pre (opcional): ")
            pre = float(pre) if pre else None
            editar_articulo(id_articulo, nom, desc, pre)

        elif opcion == '4':
            id_articulo = int(input("Ingrese el ID del articulo a eliminar: "))
            eliminar_articulo(id_articulo)

        elif opcion == '5':
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida. Intentelo de nuevo.")


if __name__ == "__main__":
    menu()
