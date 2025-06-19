-- init.sql
-- Este script se ejecuta una vez cuando el contenedor 'sgcpf_db' se inicia por primera vez.

-- Eliminar tablas si existen para asegurar una creación limpia (solo para desarrollo)
DROP TABLE IF EXISTS financial_movements CASCADE;
DROP TABLE IF EXISTS proposals CASCADE;
DROP TABLE IF EXISTS survey_responses CASCADE;
DROP TABLE IF EXISTS surveys CASCADE;
DROP TABLE IF EXISTS event_notifications CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS meeting_attendees CASCADE;
DROP TABLE IF EXISTS meetings CASCADE;
DROP TABLE IF EXISTS reports CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS committee_members CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS committees CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Crear la tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Mantener para consistencia, aunque la seguridad se manejara fuera
    role VARCHAR(50) NOT NULL -- Ej: 'Administrador', 'Tesorero', 'Secretario', 'PresidenteComite', 'Director', 'PadreDeFamilia'
);

-- Crear la tabla de Comités
CREATE TABLE IF NOT EXISTS committees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    period VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'activo'
);

-- Tabla de unión para miembros del Comité (muchos a muchos entre users y committees)
CREATE TABLE IF NOT EXISTS committee_members (
    committee_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (committee_id, user_id),
    FOREIGN KEY (committee_id) REFERENCES committees (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Crear la tabla de Documentos
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL, -- Ej: 'General', 'Acta', 'Proyecto', 'Reporte Financiero', 'Reporte Construccion'
    file_path VARCHAR(255) NOT NULL, -- Ruta o URL al archivo
    uploader_id INTEGER, -- Quién subió el documento
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploader_id) REFERENCES users (id) ON DELETE SET NULL
);

-- Crear la tabla de Proyectos (coincide con el modelo Proyecto.py)
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE, -- Añadido UNIQUE para el nombre del proyecto
    responsible_user_id INTEGER, -- Encargado del proyecto (un usuario)
    start_date DATE NOT NULL,
    end_date DATE,
    document_path VARCHAR(255), -- Ruta o ID del documento principal (campo en modelo: ruta_documento)
    status VARCHAR(50) NOT NULL DEFAULT 'activo', -- Ej: 'activo', 'finalizado', 'pendiente', 'aprobado', 'rechazado'
    FOREIGN KEY (responsible_user_id) REFERENCES users (id) ON DELETE SET NULL
);


-- Crear la tabla de Reportes (incluyendo reportes financieros y de avance de construcción)
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    type VARCHAR(100) NOT NULL, -- Ej: 'Financiero', 'Avance Construccion'
    description TEXT,
    report_date DATE NOT NULL,
    file_path VARCHAR(255) NOT NULL, -- Ruta o URL al archivo del reporte
    uploader_id INTEGER, -- Quién subió el reporte
    project_id INTEGER, -- Para reportes de avance de construcción, FK a projects
    FOREIGN KEY (uploader_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Crear la tabla de Reuniones
CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    meeting_date DATE NOT NULL,
    meeting_time TIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    agenda TEXT,
    minutes_document_id INTEGER, -- Referencia al documento del acta de reunión
    FOREIGN KEY (minutes_document_id) REFERENCES documents (id) ON DELETE SET NULL
);

-- Tabla de unión para Asistencia a Reuniones (muchos a muchos entre users y meetings)
CREATE TABLE IF NOT EXISTS meeting_attendees (
    meeting_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ausente', -- Ej: 'presente', 'ausente', 'justificado'
    PRIMARY KEY (meeting_id, user_id),
    FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Crear la tabla de Eventos
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    event_datetime TIMESTAMP NOT NULL,
    location VARCHAR(255) NOT NULL,
    target_audience VARCHAR(100) -- Ej: 'padres', 'estudiantes', 'docentes', 'todos'
);

-- Tabla de unión para notificaciones de Eventos (muchos a muchos entre users y events)
CREATE TABLE IF NOT EXISTS event_notifications (
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Crear la tabla de Encuestas
CREATE TABLE IF NOT EXISTS surveys (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL, -- 🆕 Título o nombre de la encuesta
    creator_id INTEGER, -- Quién creó la encuesta
    questions TEXT NOT NULL, -- Preguntas en formato JSON o similar
    deadline_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users (id) ON DELETE SET NULL
);


-- Tabla para respuestas de Encuestas (muchos a muchos entre users y surveys)
CREATE TABLE IF NOT EXISTS survey_responses (
    survey_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    response_data TEXT, -- Guarda las respuestas como texto JSON
    responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (survey_id, user_id),
    FOREIGN KEY (survey_id) REFERENCES surveys (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Crear la tabla de Propuestas/Quejas
CREATE TABLE IF NOT EXISTS proposals (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL, -- Ej: 'Propuesta', 'Queja'
    content TEXT NOT NULL,
    submission_date DATE NOT NULL DEFAULT CURRENT_DATE,
    submitter_id INTEGER, -- Quién envió la propuesta/queja (normalmente un PadreDeFamilia)
    FOREIGN KEY (submitter_id) REFERENCES users (id) ON DELETE SET NULL
);

-- Crear la tabla de Movimientos Financieros (ingresos y egresos)
CREATE TABLE IF NOT EXISTS financial_movements (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL, -- Ej: 'ingreso', 'egreso'
    amount NUMERIC(10, 2) NOT NULL,
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    concept TEXT NOT NULL,
    -- Puedes agregar una referencia a un comprobante (documento) si es necesario
    -- receipt_document_id INTEGER,
    -- FOREIGN KEY (receipt_document_id) REFERENCES documents (id) ON DELETE SET NULL,
    registered_by_user_id INTEGER, -- Quién registró el movimiento (Tesorero)
    FOREIGN KEY (registered_by_user_id) REFERENCES users (id) ON DELETE SET NULL
);


-- Insertar datos de ejemplo
-- Usuarios de ejemplo (roles: Director, Secretario, PadreDeFamilia)
INSERT INTO users (name, last_name, email, password_hash, role) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', 'hashed_password_1', 'Director'),
('María', 'García', 'maria.garcia@example.com', 'hashed_password_2', 'Secretario'),
('Carlos', 'López', 'carlos.lopez@example.com', 'hashed_password_3', 'PadreDeFamilia'),
('Ana', 'Díaz', 'ana.diaz@example.com', 'hashed_password_4', 'Tesorero');

-- Proyectos de ejemplo
INSERT INTO projects (name, responsible_user_id, start_date, end_date, document_path, status) VALUES
('Proyecto de Reforestación "Pulmón Verde"', (SELECT id FROM users WHERE email = 'juan.perez@example.com'), '2025-07-01', '2025-12-31', '/docs/reforestacion_plan.pdf', 'activo'),
('Feria de Ciencias 2025', (SELECT id FROM users WHERE email = 'maria.garcia@example.com'), '2025-09-15', '2025-11-20', '/docs/feria_ciencias_bases.pdf', 'activo'),
('Mejora de Instalaciones Deportivas', (SELECT id FROM users WHERE email = 'juan.perez@example.com'), '2026-01-10', '2026-06-30', '/docs/instalaciones_deportivas.pdf', 'pendiente'),
('Taller de Crianza Positiva', (SELECT id FROM users WHERE email = 'carlos.lopez@example.com'), '2025-08-01', '2025-08-30', '/docs/crianza_positiva_temario.pdf', 'activo');

-- Documentos de ejemplo
INSERT INTO documents (name, type, file_path, uploader_id, created_at) VALUES
('Acta de Reunión 01/07/2025', 'Acta', '/actas/acta_01072025.pdf', (SELECT id FROM users WHERE email = 'maria.garcia@example.com'), '2025-07-01 10:00:00'),
('Plan de Reforestación Detallado', 'Proyecto', '/docs/reforestacion_plan.pdf', (SELECT id FROM users WHERE email = 'juan.perez@example.com'), '2025-06-25 15:30:00'),
('Informe Financiero Julio 2025', 'Reporte Financiero', '/reportes/fin_julio2025.xlsx', (SELECT id FROM users WHERE email = 'ana.diaz@example.com'), '2025-08-05 09:00:00');

-- Comités de ejemplo
INSERT INTO committees (name, period, status) VALUES
('Comité Escolar 2024-2025', '2024-2025', 'activo'),
('Comité de Finanzas', '2025', 'activo');

-- Miembros del comité de ejemplo
INSERT INTO committee_members (committee_id, user_id) VALUES
((SELECT id FROM committees WHERE name = 'Comité Escolar 2024-2025'), (SELECT id FROM users WHERE email = 'juan.perez@example.com')),
((SELECT id FROM committees WHERE name = 'Comité Escolar 2024-2025'), (SELECT id FROM users WHERE email = 'maria.garcia@example.com')),
((SELECT id FROM committees WHERE name = 'Comité Escolar 2024-2025'), (SELECT id FROM users WHERE email = 'carlos.lopez@example.com')),
((SELECT id FROM committees WHERE name = 'Comité de Finanzas'), (SELECT id FROM users WHERE email = 'ana.diaz@example.com'));

-- Movimientos financieros de ejemplo
INSERT INTO financial_movements (type, amount, transaction_date, concept, registered_by_user_id) VALUES
('ingreso', 5000.00, '2025-07-10', 'Donación de la comunidad', (SELECT id FROM users WHERE email = 'ana.diaz@example.com')),
('egreso', 1500.00, '2025-07-15', 'Compra de materiales de oficina', (SELECT id FROM users WHERE email = 'ana.diaz@example.com')),
('ingreso', 250.00, '2025-07-20', 'Cuotas de padres - Julio', (SELECT id FROM users WHERE email = 'ana.diaz@example.com'));

-- Reuniones de ejemplo
INSERT INTO meetings (meeting_date, meeting_time, location, agenda, minutes_document_id) VALUES
('2025-07-01', '09:00:00', 'Sala de Juntas', 'Discusión de Proyectos y Finanzas', (SELECT id FROM documents WHERE name = 'Acta de Reunión 01/07/2025'));

-- Asistencia a reuniones de ejemplo
INSERT INTO meeting_attendees (meeting_id, user_id, status) VALUES
((SELECT id FROM meetings WHERE meeting_date = '2025-07-01'), (SELECT id FROM users WHERE email = 'juan.perez@example.com'), 'presente'),
((SELECT id FROM meetings WHERE meeting_date = '2025-07-01'), (SELECT id FROM users WHERE email = 'maria.garcia@example.com'), 'presente'),
((SELECT id FROM meetings WHERE meeting_date = '2025-07-01'), (SELECT id FROM users WHERE email = 'carlos.lopez@example.com'), 'ausente');

-- Eventos de ejemplo
INSERT INTO events (name, description, event_datetime, location, target_audience) VALUES
('Día Familiar de Limpieza Escolar', 'Actividad para limpiar y embellecer la escuela con la participación de las familias.', '2025-09-07 09:00:00', 'Patio Central', 'padres'),
('Noche de Talentos 2025', 'Evento para que los estudiantes muestren sus habilidades artísticas y musicales.', '2025-10-25 18:00:00', 'Auditorio Escolar', 'todos');

-- Propuestas/Quejas de ejemplo
INSERT INTO proposals (type, content, submission_date, submitter_id) VALUES
('Propuesta', 'Sugiero instalar más bebederos en el patio de primaria.', '2025-07-05', (SELECT id FROM users WHERE email = 'carlos.lopez@example.com')),
('Queja', 'Problemas con la iluminación en el pasillo principal.', '2025-07-08', (SELECT id FROM users WHERE email = 'carlos.lopez@example.com'));

-- Encuestas de ejemplo
INSERT INTO surveys (nombre, creator_id, questions, deadline_date, created_at)VALUES ('Encuesta de comunicación y proyectos',
(SELECT id FROM users WHERE email = 'juan.perez@example.com'),'[{"question": "¿Está satisfecho con la comunicación del comité?", "type": "radio", "options": ["Si", "No"]}, {"question": "¿Qué proyectos le gustaría ver en el futuro?", "type": "text"}]','2025-08-31','2025-07-20 14:00:00');

-- Respuestas a encuestas de ejemplo
INSERT INTO survey_responses (survey_id, user_id, response_data, responded_at) VALUES
((SELECT id FROM surveys WHERE creator_id = (SELECT id FROM users WHERE email = 'juan.perez@example.com')), (SELECT id FROM users WHERE email = 'carlos.lopez@example.com'), '{"¿Está satisfecho con la comunicación del comité?": "Si", "¿Qué proyectos le gustaría ver en el futuro?": "Más actividades deportivas"}', '2025-07-25 09:30:00');
