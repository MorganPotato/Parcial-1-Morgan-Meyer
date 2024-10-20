import redis

# Conexion a Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Funcion para generar IDs unicos
def generar_id():
    return r.incr('articulo_id')

# Funcion para agregar articulos
def agregar_articulo(nom, desc, pre):
    id_articulo = generar_id()
    r.hset(f"articulo:{id_articulo}", "nom", nom)
    r.hset(f"articulo:{id_articulo}", "desc", desc)
    r.hset(f"articulo:{id_articulo}", "pre", pre)
    print(f"Articulo {id_articulo} agregado exitosamente.")

# Funcion para buscar articulos
def buscar_articulo(nom):
    keys = r.keys("articulo:*")
    encontrados = False
    for key in keys:
        articulo = r.hgetall(key)
        if nom.lower() in articulo["nom"].lower():
            id_articulo = key.split(":")[1]
            print(f"ID: {id_articulo}, Nom: {articulo['nom']}, Desc: {articulo['desc']}, Pre: {articulo['pre']}")
            encontrados = True
    if not encontrados:
        print("No se encontraron articulos.")

# Funcion para editar articulos
def editar_articulo(id_articulo, nom=None, desc=None, pre=None):
    key = f"articulo:{id_articulo}"
    if r.exists(key):
        if nom:
            r.hset(key, "nom", nom)
        if desc:
            r.hset(key, "desc", desc)
        if pre:
            r.hset(key, "pre", pre)
        articulo_actualizado = r.hgetall(key)
        print(f"Articulo {id_articulo} actualizado exitosamente:")
        print(f"ID: {id_articulo}, Nom: {articulo_actualizado['nom']}, Desc: {articulo_actualizado['desc']}, Pre: {articulo_actualizado['pre']}")
    else:
        print("Articulo no encontrado.")

# Funcion para eliminar articulos
def eliminar_articulo(id_articulo):
    key = f"articulo:{id_articulo}"
    if r.exists(key):
        r.delete(key)
        print(f"Articulo {id_articulo} eliminado exitosamente.")
    else:
        print("Articulo no encontrado.")

# Funcion para validar que el precio sea un numero valido
def solicitar_precio():
    while True:
        try:
            pre = float(input("Pre del articulo: "))
            return pre
        except ValueError:
            print("Error: El precio debe ser un numero. Intente de nuevo.")

# Menu de la aplicacion
def menu():
    while True:
        print("\n--- Menu del Sistema de Registro de Presupuesto en Cocina ---")
        print("Nom = nombre del articulo")
        print("Desc = descripcion del articulo")
        print("Pre = precio del articulo")
        print("\n1. Registrar un nuevo articulo")
        print("2. Buscar un articulo")
        print("3. Editar un articulo")
        print("4. Eliminar un articulo")
        print("5. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == '1':
            nom = input("Nom del articulo: ")
            desc = input("Desc del articulo: ")
            pre = solicitar_precio()
            agregar_articulo(nom, desc, pre)

        elif opcion == '2':
            nom = input("Ingrese el nom del articulo a buscar: ")
            buscar_articulo(nom)

        elif opcion == '3':
            id_articulo = input("Ingrese el ID del articulo a editar: ")
            print("Deje el campo vacio si no desea cambiarlo.")
            nom = input("Nuevo nom (opcional): ") or None
            desc = input("Nueva desc (opcional): ") or None
            pre = input("Nuevo pre (opcional, debe ser un numero): ")
            pre = float(pre) if pre else None
            editar_articulo(id_articulo, nom, desc, pre)

        elif opcion == '4':
            id_articulo = input("Ingrese el ID del articulo a eliminar: ")
            eliminar_articulo(id_articulo)

        elif opcion == '5':
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida. Intentelo de nuevo.")

if __name__ == "__main__":
    menu()
