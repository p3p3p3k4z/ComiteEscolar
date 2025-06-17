-- init.sql
-- Este script se ejecuta una vez cuando el contenedor 'sgcpf_db' se inicia por primera vez.

-- Crear la tabla de Usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    -- Aunque las librerías de seguridad fueron removidas del requirements.txt,
    -- mantener un campo para el hash de la contraseña es crucial para la gestión de usuarios
    password_hash VARCHAR(255) NOT NULL,
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

-- Crear la tabla de Proyectos
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    responsible_user_id INTEGER, -- Encargado del proyecto (un usuario)
    start_date DATE NOT NULL,
    end_date DATE,
    main_document_id INTEGER, -- Referencia al documento principal del proyecto
    status VARCHAR(50) NOT NULL DEFAULT 'activo', -- Ej: 'activo', 'finalizado', 'pendiente'
    FOREIGN KEY (responsible_user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (main_document_id) REFERENCES documents (id) ON DELETE SET NULL
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
    creator_id INTEGER, -- Quién creó la encuesta
    questions TEXT NOT NULL, -- Para simplificar, guarda las preguntas como texto JSON o un formato similar. Considera una tabla 'survey_questions' y 'survey_options' para un diseño más normalizado.
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

