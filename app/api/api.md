###Proyecto
```bash
╭─m4r10@opensuse ~/Documents/ComiteEscolar ‹main●› 
╰─$ curl "http://localhost:8000/proyectos/"                                 
[{"id":1,"nombre":"Proyecto de Reforestación \"Pulmón Verde\"","id_usuario_responsable":1,"fecha_inicio":"2025-07-01","fecha_fin":"2025-12-31","ruta_documento":"/docs/reforestacion_plan.pdf","estado":"activo"},{"id":2,"nombre":"Feria de Ciencias 2025","id_usuario_responsable":2,"fecha_inicio":"2025-09-15","fecha_fin":"2025-11-20","ruta_documento":"/docs/feria_ciencias_bases.pdf","estado":"activo"},{"id":3,"nombre":"Mejora de Instalaciones Deportivas","id_usuario_responsable":1,"fecha_inicio":"2026-01-10","fecha_fin":"2026-06-30","ruta_documento":"/docs/instalaciones_deportivas.pdf","estado":"pendiente"},{"id":4,"nombre":"Taller de Crianza Positiva","id_usuario_responsable":3,"fecha_inicio":"2025-08-01","fecha_fin":"2025-08-30","ruta_documento":"/docs/crianza_positiva_temario.pdf","estado":"activo"}]╭─m4r10@opensuse ~/Documents/ComiteEscolar ‹main●› 
╰─$ curl "http://localhost:8000/proyectos/1"         
{"id":1,"nombre":"Proyecto de Reforestación \"Pulmón Verde\"","id_usuario_responsable":1,"fecha_inicio":"2025-07-01","fecha_fin":"2025-12-31","ruta_documento":"/docs/reforestacion_plan.pdf","estado":"activo"}╭─m4r10@opensuse ~/Documents/ComiteEscolar ‹main●› 
╰─$ curl -X POST "http://localhost:8000/proyectos/" \
     -H "Content-Type: application/json" \
     -d '{
           "nombre": "Proyecto de Renovación Biblioteca",
           "id_usuario_responsable": 1,
           "fecha_inicio": "2025-10-01",
           "fecha_fin": "2026-03-31",
           "ruta_documento": "/docs/renovacion_biblioteca.pdf"
         }'
{"id":5,"nombre":"Proyecto de Renovación Biblioteca","id_usuario_responsable":1,"fecha_inicio":"2025-10-01","fecha_fin":"2026-03-31","ruta_documento":"/docs/renovacion_biblioteca.pdf","estado":"activo"}╭─m4r10@opensuse ~/Documents/ComiteEscolar ‹main●› 
╰─$ curl -X PUT "http://localhost:8000/proyectos/2" \                         
     -H "Content-Type: application/json" \
     -d '{
           "nombre": "Proyecto de Renovación Biblioteca - Completado",
           "estado": "finalizado",
           "fecha_fin": "2026-02-15"
         }'
{"id":2,"nombre":"Proyecto de Renovación Biblioteca - Completado","id_usuario_responsable":2,"fecha_inicio":"2025-09-15","fecha_fin":"2026-02-15","ruta_documento":"/docs/feria_ciencias_bases.pdf","estado":"finalizado"}╭─m4r10@opensuse ~/Documents/ComiteEscolar ‹main●› 
╰─$ curl -X DELETE "http://localhost:8000/proyectos/3"
```