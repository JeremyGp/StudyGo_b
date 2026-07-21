from sqlalchemy.orm import Session

from app.models.enums import EstadoTarea
from app.models.subtarea import Subtarea
from app.models.tarea import Tarea
from app.repository import subtarea as subtarea_repository
from app.repository import tarea as tarea_repository


PLANTILLAS_SUBTAREAS = {
    "informe": [
        ("Investigar el tema", "Buscar fuentes y recopilar informacion relevante."),
        ("Organizar la estructura", "Definir secciones, ideas principales y orden del contenido."),
        ("Redactar el contenido", "Escribir el desarrollo principal de la tarea."),
        ("Revisar y corregir", "Corregir ortografia, coherencia y formato antes de entregar."),
    ],
    "examen": [
        ("Revisar los temas", "Identificar los contenidos que entran en la evaluacion."),
        ("Estudiar apuntes", "Repasar clases, lecturas y material de apoyo."),
        ("Resolver ejercicios", "Practicar con ejercicios, preguntas o ejemplos similares."),
        ("Repasar puntos debiles", "Reforzar los temas que aun generan dificultad."),
    ],
    "exposicion": [
        ("Investigar el tema", "Recopilar informacion clara y confiable."),
        ("Preparar diapositivas", "Crear el material visual para la presentacion."),
        ("Organizar el discurso", "Definir que dira cada integrante o cada seccion."),
        ("Practicar la presentacion", "Ensayar tiempos, explicacion y posibles preguntas."),
    ],
    "proyecto": [
        ("Definir requisitos", "Identificar que debe incluir la entrega."),
        ("Desarrollar la solucion", "Construir la parte principal del trabajo."),
        ("Probar el resultado", "Verificar que todo funcione correctamente."),
        ("Documentar y revisar", "Preparar evidencia, explicacion y correcciones finales."),
    ],
    "general": [
        ("Analizar la tarea", "Leer la consigna y definir que se debe entregar."),
        ("Desarrollar la actividad", "Trabajar en el contenido principal de la tarea."),
        ("Revisar el avance", "Comprobar si falta informacion o correcciones."),
        ("Preparar la entrega", "Ordenar el resultado final y dejarlo listo para entregar."),
    ],
}

PALABRAS_CLAVE = {
    "informe": ["informe", "ensayo", "documento", "reporte", "resumen"],
    "examen": ["examen", "parcial", "quiz", "evaluacion", "prueba"],
    "exposicion": ["exposicion", "presentacion", "diapositiva", "sustentacion"],
    "proyecto": ["proyecto", "sistema", "app", "aplicacion", "desarrollo"],
}


def generar_subtareas(
    db: Session,
    id_tarea: int,
    regenerar: bool = False
) -> list[Subtarea]:
    """Genera subtareas automaticas para una tarea usando reglas simples."""

    tarea = tarea_repository.obtener_por_id(db, id_tarea)

    if tarea is None:
        raise ValueError("Tarea no encontrada.")

    subtareas_existentes = subtarea_repository.listar_por_tarea(db, id_tarea)

    if subtareas_existentes and not regenerar:
        return subtareas_existentes

    if subtareas_existentes and regenerar:
        eliminar_subtareas_existentes(db, subtareas_existentes)

    plantilla = seleccionar_plantilla(tarea)
    cantidad = calcular_cantidad_subtareas(tarea.horas_estimadas)
    subtareas_generadas = []

    for orden, (titulo, descripcion) in enumerate(plantilla[:cantidad], start=1):
        subtarea = Subtarea(
            titulo=titulo,
            descripcion=descripcion,
            estado=EstadoTarea.PENDIENTE,
            orden=orden,
            id_tarea=id_tarea
        )

        subtareas_generadas.append(
            subtarea_repository.crear(db, subtarea)
        )

    return subtareas_generadas


def regenerar_subtareas(
    db: Session,
    id_tarea: int
) -> list[Subtarea]:
    """Elimina las subtareas actuales y crea una nueva propuesta."""

    return generar_subtareas(
        db,
        id_tarea,
        regenerar=True
    )


def seleccionar_plantilla(tarea: Tarea) -> list[tuple[str, str]]:
    """Selecciona una plantilla segun el titulo y la descripcion."""

    texto = f"{tarea.titulo or ''} {tarea.descripcion or ''}".lower()

    for tipo, palabras in PALABRAS_CLAVE.items():
        if any(palabra in texto for palabra in palabras):
            return PLANTILLAS_SUBTAREAS[tipo]

    return PLANTILLAS_SUBTAREAS["general"]


def calcular_cantidad_subtareas(horas_estimadas: int | None) -> int:
    """Determina cuantas subtareas crear segun el esfuerzo estimado."""

    if horas_estimadas is None or horas_estimadas <= 2:
        return 2

    if horas_estimadas <= 4:
        return 3

    if horas_estimadas <= 8:
        return 4

    return 5


def eliminar_subtareas_existentes(
    db: Session,
    subtareas: list[Subtarea]
) -> None:
    """Elimina subtareas previas para permitir regeneracion."""

    for subtarea in subtareas:
        subtarea_repository.eliminar(db, subtarea)
