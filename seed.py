"""Carga inicial de datos para cumplir con los mínimos exigidos por la Universidad de Madeira."""
from datetime import date
from sqlalchemy.orm import Session
from app.constants import EstadoRecurso, RolUsuario, TipoColeccion
from app.models.recurso import Recurso
from app.models.usuario import Usuario


def poblar_base_de_datos(db: Session):
    if db.query(Usuario).count() > 0:
        return

    usuarios = []
    # 50 Estudiantes
    for i in range(1, 51):
        usuarios.append(
            Usuario(
                identificacion=f"100000{i:02d}",
                codigo=f"2026{i:04d}",
                nombres=f"Estudiante {i}",
                apellidos="Madeira",
                correo_institucional=f"estudiante{i}@umadeira.edu.co",
                plan="Ingeniería de Software",
                semestre=(i % 10) + 1,
                rol=RolUsuario.ESTUDIANTE,
            )
        )
    # 10 Profesores
    for i in range(1, 11):
        usuarios.append(
            Usuario(
                identificacion=f"200000{i:02d}",
                codigo=None,
                nombres=f"Profesor {i}",
                apellidos="Académico",
                correo_institucional=f"profesor{i}@umadeira.edu.co",
                plan="Facultad de Ingeniería",
                semestre=None,
                rol=RolUsuario.PROFESOR,
            )
        )
    # 3 Bibliotecarios
    for i in range(1, 4):
        usuarios.append(
            Usuario(
                identificacion=f"3000000{i}",
                codigo=None,
                nombres=f"Bibliotecario {i}",
                apellidos="SGB",
                correo_institucional=f"bibliotecario{i}@umadeira.edu.co",
                plan="Biblioteca Central",
                semestre=None,
                rol=RolUsuario.BIBLIOTECARIO,
            )
        )
    db.add_all(usuarios)

    recursos = []
    # 20 Libros Colección General (mín. 5 ejemplares c/u)
    for i in range(1, 21):
        recursos.append(
            Recurso(
                codigo_recurso=f"GEN-{i:03d}",
                coleccion=TipoColeccion.GENERAL,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Arquitectura de Software Vol. {i}",
                isbn_issn=f"978-958-00-{i:04d}-1",
                resumen_descripcion="Obra general sobre diseño y arquitectura de sistemas.",
                autores="Robert C. Martin, Martin Fowler",
                editorial="Madeira Press",
                fecha_publicacion=date(2022, 5, 10),
                volumen="1",
                numero_edicion="2da",
                idioma="Español",
                numero_paginas=350,
                ancho=15.0,
                alto=23.0,
                profundidad=2.5,
                unidad_dimension="cm",
                tipo_encuadernacion="Tapa blanda" if i % 2 == 0 else "Tapa dura",
                cantidad_ejemplares=5,
            )
        )

    # 20 Libros Colección Reserva (mín. 10 ejemplares c/u)
    for i in range(1, 21):
        recursos.append(
            Recurso(
                codigo_recurso=f"RES-{i:03d}",
                coleccion=TipoColeccion.RESERVA,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Cálculo y Estructuras Académicas {i}",
                isbn_issn=f"978-958-11-{i:04d}-2",
                resumen_descripcion="Texto guía de alta demanda académica.",
                autores="James Stewart",
                editorial="McGraw-Hill",
                fecha_publicacion=date(2021, 3, 15),
                idioma="Español",
                numero_paginas=620,
                ancho=18.0,
                alto=25.0,
                profundidad=3.2,
                unidad_dimension="cm",
                tipo_encuadernacion="Tapa dura",
                cantidad_ejemplares=10,
            )
        )

    # 20 Diccionarios Colección Referencia (dimensiones en pulgadas, mín. 3 ejemplares)
    for i in range(1, 21):
        recursos.append(
            Recurso(
                codigo_recurso=f"REF-{i:03d}",
                coleccion=TipoColeccion.REFERENCIA,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Diccionario Enciclopédico Especializado {i}",
                isbn_issn=f"978-958-22-{i:04d}-3",
                resumen_descripcion="Diccionario de referencia y consulta rápida.",
                autores="Real Academia / Editorial Madeira",
                editorial="Editorial Madeira",
                fecha_publicacion=date(2020, 8, 1),
                idioma="Español/Inglés",
                numero_paginas=980,
                ancho=6.5,
                alto=9.5,
                profundidad=2.0,
                unidad_dimension="pulgadas",
                cantidad_ejemplares=3,
            )
        )

    # 15 Revistas Hemeroteca (ISSN, mín. 2 ejemplares)
    for i in range(1, 16):
        recursos.append(
            Recurso(
                codigo_recurso=f"HEM-{i:03d}",
                coleccion=TipoColeccion.HEMEROTECA,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Revista Científica de Ingeniería #{i}",
                isbn_issn=f"2027-{i:04d}",
                volumen=f"Vol. {i}",
                numero_edicion=f"Ed. {i*2}",
                fecha_publicacion=date(2024, 1, 20),
                editorial="IEEE Madeira",
                idioma="Inglés",
                periodicidad="Mensual",
                numero_paginas=85,
                cantidad_ejemplares=2,
            )
        )

    # 15 Mapas Mapoteca (jpg, pdf, shape, dwg, sin cantidad de ejemplares)
    formatos = ["jpg", "pdf", "shape", "dwg"]
    for i in range(1, 16):
        recursos.append(
            Recurso(
                codigo_recurso=f"MAP-{i:03d}",
                coleccion=TipoColeccion.MAPOTECA,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Mapa Cartográfico Región Madeira {i}",
                resumen_descripcion="Préstamo en modo lectura por USB.",
                formato_mapa=formatos[i % 4],
                cantidad_ejemplares=0,
            )
        )

    # 5 Laptops (mín. 3 ejemplares c/u) y 2 Tabletas (mín. 10 ejemplares c/u) en Tecnoteca
    for i in range(1, 6):
        recursos.append(
            Recurso(
                codigo_recurso=f"LAP-{i:03d}",
                coleccion=TipoColeccion.TECNOTECA_LAPTOP,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Laptop Académica Dell Latitude #{i}",
                numero_equipo=f"EQ-LAP-{i:02d}",
                marca="Dell",
                modelo=f"Latitude 54{i}0",
                cargador="USB-C 65W Original",
                funda="Funda neopreno 14 pulgadas",
                cantidad_ejemplares=3,
            )
        )
    for i in range(1, 3):
        recursos.append(
            Recurso(
                codigo_recurso=f"TAB-{i:03d}",
                coleccion=TipoColeccion.TECNOTECA_TABLETA,
                estado=EstadoRecurso.DISPONIBLE,
                titulo=f"Tableta de Lectura iPad Air #{i}",
                marca="Apple",
                modelo=f"iPad Air Gen {i+4}",
                cargador="USB-C 20W",
                funda="Smart Folio protectora",
                cantidad_ejemplares=10,
            )
        )

    db.add_all(recursos)
    db.commit()
