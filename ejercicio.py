# ==========================================
# 1. DATOS INICIALES DEL SISTEMA
# ==========================================

def inicializar_datos():
    # Diccionario descriptivo de productos
    productos = {
        'M001': ['Alimento Premium', 'comida', 'DogPlus', 10.0, True, False],
        'M002': ['Arena Aglomerante', 'higiene', 'CatClean', 8.0, False, False],
        'M003': ['Snack Dental', 'snack', 'BiteJoy', 1.0, True, True],
        'M004': ['Shampoo Suave', 'higiene', 'PetCare', 0.5, False, True],
        'M005': ['Correa Nylon', 'accesorio', 'WalkPro', 0.3, True, False],
        'M006': ['Cama Mediana', 'accesorio', 'CozyPet', 2.0, False, False]
    }
    
    # Diccionario operativo de stock [precio, unidades]
    stock = {
        'M001': [32990, 12],
        'M002': [9990, 0],
        'M003': [5490, 25],
        'M004': [7990, 5],
        'M005': [11990, 7],
        'M006': [24990, 3]
    }
    return productos, stock


# ==========================================
# FUNCIONES GENERALES Y MENÚ
# ==========================================

def leer_opcion():
    opcion = -1
    es_valida = False
    while not es_valida:
        try:
            entrada = input("Ingrese opción: ")
            opcion = int(entrada)
            if 1 <= opcion <= 6:
                es_valida = True
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")
    return opcion


def buscar_codigo(codigo, productos):
    # La validación del código no debe distinguir mayúsculas y minúsculas
    for c in productos:
        if c.upper() == codigo.upper():
            return True
    return False


# ==========================================
# OPCIÓN 1: UNIDADES POR CATEGORÍA
# ==========================================

def unidades_categoria(categoria, productos, stock):
    total_unidades = 0
    categoria_buscar = categoria.strip().lower()
    
    for cod, datos in productos.items():
        cat_producto = datos[1].lower()
        if cat_producto == categoria_buscar:
            if cod in stock:
                total_unidades += stock[cod][1]
                
    print(f"El total de unidades disponibles es: {total_unidades}")


# ==========================================
# OPCIÓN 2: BÚSQUEDA POR RANGO DE PRECIO
# ==========================================

def busqueda_precio(p_min, p_max, productos, stock):
    resultados = []
    
    for cod, datos_stock in stock.items():
        precio = datos_stock[0]
        unidades = datos_stock[1]
        
        if p_min <= precio <= p_max and unidades > 0:
            if cod in productos:
                nombre = productos[cod][0]
                resultados.append(f"{nombre}--{cod}")
                
    if len(resultados) > 0:
        # Se ordenan alfabéticamente por nombre
        resultados.sort()
        print(f"Los productos encontrados son: {resultados}")
    else:
        print("No hay productos en ese rango de precios.")


# ==========================================
# OPCIÓN 3: ACTUALIZAR PRECIO
# ==========================================

def actualizar_precio(codigo, nuevo_precio, productos, stock):
    if buscar_codigo(codigo, productos):
        # Encontrar la clave exacta con su capitalización original
        clave_exacta = codigo
        for c in stock:
            if c.upper() == codigo.upper():
                clave_exacta = c
        
        stock[clave_exacta][0] = nuevo_precio
        return True
    return False


# ==========================================
# OPCIÓN 4: FUNCIONES DE VALIDACIÓN INDEPENDIENTES
# ==========================================

def validar_codigo_nuevo(codigo, productos):
    if not codigo or codigo.isspace():
        return False
    # No debe existir previamente en el diccionario
    if buscar_codigo(codigo, productos):
        return False
    return True

def validar_nombre(nombre):
    return bool(nombre and not nombre.isspace())

def validar_categoria(categoria):
    return bool(categoria and not categoria.isspace())

def validar_marca(marca):
    return bool(marca and not marca.isspace())

def validar_peso(peso_txt):
    try:
        peso = float(peso_txt)
        return peso > 0
    except ValueError:
        return False

def validar_es_importado(opcion_txt):
    return opcion_txt.strip().lower() in ['s', 'n']

def validar_es_para_cachorro(opcion_txt):
    return opcion_txt.strip().lower() in ['s', 'n']

def validar_precio_valor(precio_txt):
    try:
        precio = int(precio_txt)
        return precio > 0
    except ValueError:
        return False

def validar_unidades_valor(unidades_txt):
    try:
        unidades = int(unidades_txt)
        return unidades >= 0
    except ValueError:
        return False

def agregar_producto(codigo, nombre, categoria, marca, peso_kg, es_importado, es_para_cachorro, precio, unidades, productos, stock):
    if buscar_codigo(codigo, productos):
        return False
    
    # Conversiones finales de los datos sanitizados
    bool_importado = True if es_importado.strip().lower() == 's' else False
    bool_cachorro = True if es_para_cachorro.strip().lower() == 's' else False
    
    # Agregar a estructuras
    productos[codigo] = [nombre, categoria, marca, float(peso_kg), bool_importado, bool_cachorro]
    stock[codigo] = [int(precio), int(unidades)]
    return True


# ==========================================
# OPCIÓN 5: ELIMINAR PRODUCTO
# ==========================================

def eliminar_producto(codigo, productos, stock):
    if buscar_codigo(codigo, productos):
        clave_exacta = codigo
        for c in productos:
            if c.upper() == codigo.upper():
                clave_exacta = c
                
        del productos[clave_exacta]
        del stock[clave_exacta]
        return True
    return False


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    # Inicialización de diccionarios locales (no globales)
    dicc_productos, dicc_stock = inicializar_datos()
    
    ejecutando_menu = True
    while ejecutando_menu:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Unidades por categoría")
        print("2. Búsqueda de productos por rango de precio")
        print("3. Actualizar precio de producto")
        print("4. Agregar producto")
        print("5. Eliminar producto")
        print("6. Salir")
        print("=====================================")
        
        opc = leer_opcion()
        
        if opc == 1:
            cat = input("Ingrese categoría a consultar: ")
            unidades_categoria(cat, dicc_productos, dicc_stock)
            
        elif opc == 2:
            solicitando_rangos = True
            p_min = 0
            p_max = 0
            while solicitando_rangos:
                try:
                    p_min_txt = input("Ingrese precio mínimo: ")
                    p_min = int(p_min_txt)
                    p_max_txt = input("Ingrese precio máximo: ")
                    p_max = int(p_max_txt)
                    
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        solicitando_rangos = False
                    else:
                        print("Debe ingresar valores enteros coherentes (min <= max y mayores a 0)")
                except ValueError:
                    print("Debe ingresar valores enteros")
            
            busqueda_precio(p_min, p_max, dicc_productos, dicc_stock)
            
        elif opc == 3:
            procesando_actualizacion = True
            while procesando_actualizacion:
                cod_act = input("Ingrese código del producto: ")
                nuevo_p_txt = input("Ingrese nuevo precio: ")
                
                # Validación de nuevo precio entero y positivo
                try:
                    nuevo_p = int(nuevo_p_txt)
                    if nuevo_p > 0:
                        resultado = actualizar_precio(cod_act, nuevo_p, dicc_productos, dicc_stock)
                        if resultado:
                            print("Precio actualizado")
                        else:
                            print("El código no existe")
                    else:
                        print("El precio debe ser un entero positivo")
                except ValueError:
                    print("El precio debe ser un número entero")
                
                # Ciclo controlado de repetición sin Break
                respuesta_valida = False
                while not respuesta_valida:
                    resp = input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()
                    if resp == 's':
                        respuesta_valida = True
                    elif resp == 'n':
                        respuesta_valida = True
                        procesando_actualizacion = False
                        
        elif opc == 4:
            c_cod = input("Ingrese código del producto: ")
            c_nom = input("Ingrese nombre: ")
            c_cat = input("Ingrese categoría: ")
            c_mar = input("Ingrese marca: ")
            c_pes = input("Ingrese peso (kg): ")
            c_imp = input("¿Es importado? (s/n): ")
            c_cac = input("¿Es para cachorro? (s/n): ")
            c_pre = input("Ingrese precio: ")
            c_uni = input("Ingrese unidades: ")
            
            # Ejecutar todas las validaciones independientes
            v1 = validar_codigo_nuevo(c_cod, dicc_productos)
            v2 = validar_nombre(c_nom)
            v3 = validar_categoria(c_cat)
            v4 = validar_marca(c_mar)
            v5 = validar_peso(c_pes)
            v6 = validar_es_importado(c_imp)
            v7 = validar_es_para_cachorro(c_cac)
            v8 = validar_precio_valor(c_pre)
            v9 = validar_unidades_valor(c_uni)
            
            if v1 and v2 and v3 and v4 and v5 and v6 and v7 and v8 and v9:
                exito = agregar_producto(c_cod, c_nom, c_cat, c_mar, c_pes, c_imp, c_cac, c_pre, c_uni, dicc_productos, dicc_stock)
                if exito:
                    print("Producto agregado")
                else:
                    print("El código ya existe")
            else:
                # El enunciado indica mostrar error correspondiente si alguno falla
                if not v1: print("Error: Código vacío o ya existente.")
                elif not v2: print("Error: Nombre inválido.")
                elif not v3: print("Error: Categoría inválida.")
                elif not v4: print("Error: Marca inválida.")
                elif not v5: print("Error: Peso debe ser mayor a 0.")
                elif not v6: print("Error: Debe ingresar 's' o 'n' para importado.")
                elif not v7: print("Error: Debe ingresar 's' o 'n' para cachorro.")
                elif not v8: print("Error: Precio debe ser un entero mayor a 0.")
                elif not v9: print("Error: Unidades debe ser mayor o igual a 0.")
                
        elif opc == 5:
            cod_eliminar = input("Ingrese código del producto que desea eliminar: ")
            if eliminar_producto(cod_eliminar, dicc_productos, dicc_stock):
                print("Producto eliminado")
            else:
                print("El código no existe")
                
        elif opc == 6:
            print("Programa finalizado.")
            ejecutando_menu = False

# Punto de entrada estándar de ejecución
if __name__ == "__main__":
    main()