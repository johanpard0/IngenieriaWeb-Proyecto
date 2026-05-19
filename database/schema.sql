-- =========================================================
-- BASE DE DATOS CATALINA - CHATBOT INSTITUCIONAL
-- PostgreSQL
-- =========================================================

-- =========================
-- 1. PROGRAMAS ACADÉMICOS
-- =========================

CREATE TABLE programas_academicos (
    id_programa SERIAL PRIMARY KEY,
    nombre_programa VARCHAR(120) NOT NULL,
    facultad VARCHAR(120),
    jornada VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 2. ESTUDIANTES
-- =========================

CREATE TABLE estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    id_programa INT REFERENCES programas_academicos(id_programa) ON DELETE SET NULL,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE,
    correo VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT,
    telefono VARCHAR(20),
    codigo_estudiantil VARCHAR(30),
    semestre INT,
    provider VARCHAR(30) DEFAULT 'local',
    provider_id TEXT,
    foto_perfil TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP
);

-- =========================
-- 3. SESIONES
-- =========================

CREATE TABLE sesiones (
    id_sesion SERIAL PRIMARY KEY,
    id_estudiante INT NOT NULL REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP,
    estado VARCHAR(30) DEFAULT 'activa',
    ip_usuario VARCHAR(50),
    navegador TEXT,
    metodo_login VARCHAR(30) DEFAULT 'local'
);

-- =========================
-- 4. CHATS
-- =========================

CREATE TABLE chats (
    id_chat SERIAL PRIMARY KEY,
    id_estudiante INT NOT NULL REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    titulo VARCHAR(150) DEFAULT 'Nuevo chat',
    estado VARCHAR(30) DEFAULT 'abierto',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad_mensajes INT DEFAULT 0,
    resumen_chat TEXT
);

-- =========================
-- 5. MENSAJES
-- =========================

CREATE TABLE mensajes (
    id_mensaje SERIAL PRIMARY KEY,
    id_chat INT NOT NULL REFERENCES chats(id_chat) ON DELETE CASCADE,
    emisor VARCHAR(30) NOT NULL,
    contenido TEXT NOT NULL,
    tipo_mensaje VARCHAR(30) DEFAULT 'texto',
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    leido BOOLEAN DEFAULT FALSE,
    metadata JSONB
);

-- =========================
-- 6. DOCUMENTOS INSTITUCIONALES
-- =========================

CREATE TABLE documentos_institucionales (
    id_documento SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(80),
    tipo_archivo VARCHAR(20),
    ruta_archivo TEXT NOT NULL,
    tamano_mb DECIMAL(10,2),
    version VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subido_por VARCHAR(100),
    palabras_clave TEXT
);

-- =========================
-- 7. CONTENIDO DE DOCUMENTOS
-- =========================

CREATE TABLE contenido_documento (
    id_contenido SERIAL PRIMARY KEY,
    id_documento INT NOT NULL REFERENCES documentos_institucionales(id_documento) ON DELETE CASCADE,
    titulo_seccion VARCHAR(150),
    pagina INT,
    contenido_texto TEXT NOT NULL,
    palabras_clave TEXT,
    fecha_indexacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 8. DOCUMENTOS SUBIDOS POR ESTUDIANTES
-- =========================

CREATE TABLE documentos_usuario (
    id_documento_usuario SERIAL PRIMARY KEY,
    id_estudiante INT NOT NULL REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    nombre_original VARCHAR(150) NOT NULL,
    nombre_guardado VARCHAR(150) NOT NULL,
    tipo_archivo VARCHAR(30),
    ruta_archivo TEXT NOT NULL,
    tamano_mb DECIMAL(10,2),
    estado VARCHAR(30) DEFAULT 'subido',
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT
);

-- =========================
-- 9. DOCENTES
-- =========================

CREATE TABLE docentes (
    id_docente SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(120) UNIQUE,
    facultad VARCHAR(120),
    area_conocimiento VARCHAR(120),
    oficina VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 10. ASIGNATURAS
-- =========================

CREATE TABLE asignaturas (
    id_asignatura SERIAL PRIMARY KEY,
    id_programa INT REFERENCES programas_academicos(id_programa) ON DELETE SET NULL,
    nombre VARCHAR(120) NOT NULL,
    codigo VARCHAR(30) UNIQUE,
    creditos INT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 11. RELACIÓN DOCENTE - ASIGNATURA
-- =========================

CREATE TABLE docente_asignatura (
    id_docente_asignatura SERIAL PRIMARY KEY,
    id_docente INT NOT NULL REFERENCES docentes(id_docente) ON DELETE CASCADE,
    id_asignatura INT NOT NULL REFERENCES asignaturas(id_asignatura) ON DELETE CASCADE,
    periodo_academico VARCHAR(20),
    grupo VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE
);

-- =========================
-- 12. SALONES
-- =========================

CREATE TABLE salones (
    id_salon SERIAL PRIMARY KEY,
    codigo_salon VARCHAR(30) UNIQUE NOT NULL,
    bloque VARCHAR(30),
    piso INT,
    capacidad INT,
    tipo_salon VARCHAR(50),
    descripcion_ubicacion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- =========================
-- 13. HORARIOS DE CLASE
-- =========================

CREATE TABLE horarios_clase (
    id_horario SERIAL PRIMARY KEY,
    id_asignatura INT REFERENCES asignaturas(id_asignatura) ON DELETE CASCADE,
    id_docente INT REFERENCES docentes(id_docente) ON DELETE SET NULL,
    id_salon INT REFERENCES salones(id_salon) ON DELETE SET NULL,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    periodo_academico VARCHAR(20),
    grupo VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE
);

-- =========================
-- 14. CONSULTAS DEL CHAT
-- =========================

CREATE TABLE consultas_chat (
    id_consulta SERIAL PRIMARY KEY,
    id_chat INT REFERENCES chats(id_chat) ON DELETE CASCADE,
    id_estudiante INT REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    id_mensaje INT REFERENCES mensajes(id_mensaje) ON DELETE SET NULL,
    tipo_consulta VARCHAR(50),
    pregunta_original TEXT NOT NULL,
    respuesta_generada TEXT,
    nivel_confianza DECIMAL(5,2),
    resuelta BOOLEAN DEFAULT FALSE,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 15. FORMULARIOS O SOLICITUDES
-- =========================

CREATE TABLE formularios_solicitud (
    id_solicitud SERIAL PRIMARY KEY,
    id_estudiante INT REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    tipo_solicitud VARCHAR(80),
    asunto VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(30) DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_respuesta TIMESTAMP,
    respuesta TEXT
);

-- =========================
-- 16. RETROALIMENTACIÓN DEL CHAT
-- =========================

CREATE TABLE retroalimentacion_chat (
    id_retroalimentacion SERIAL PRIMARY KEY,
    id_mensaje INT REFERENCES mensajes(id_mensaje) ON DELETE CASCADE,
    id_estudiante INT REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    calificacion INT CHECK (calificacion BETWEEN 1 AND 5),
    comentario TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 17. AUDITORÍA DEL SISTEMA
-- =========================

CREATE TABLE auditoria_sistema (
    id_auditoria SERIAL PRIMARY KEY,
    id_estudiante INT REFERENCES estudiantes(id_estudiante) ON DELETE SET NULL,
    accion VARCHAR(100) NOT NULL,
    descripcion TEXT,
    modulo VARCHAR(80),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_usuario VARCHAR(50),
    metadata JSONB
);

-- =========================================================
-- TABLAS PARA CONEXIÓN CON IA
-- =========================================================

-- =========================
-- 18. PROVEEDORES DE IA
-- =========================

CREATE TABLE proveedores_ia (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 19. MODELOS DE IA
-- =========================

CREATE TABLE modelos_ia (
    id_modelo SERIAL PRIMARY KEY,
    id_proveedor INT NOT NULL REFERENCES proveedores_ia(id_proveedor) ON DELETE CASCADE,
    nombre_modelo VARCHAR(100) NOT NULL,
    tipo_modelo VARCHAR(50),
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 20. CONFIGURACIÓN DEL CHATBOT
-- =========================

CREATE TABLE configuracion_chatbot (
    id_configuracion SERIAL PRIMARY KEY,
    nombre_chatbot VARCHAR(80) DEFAULT 'Catalina',
    id_modelo_respuesta INT REFERENCES modelos_ia(id_modelo) ON DELETE SET NULL,
    id_modelo_embedding INT REFERENCES modelos_ia(id_modelo) ON DELETE SET NULL,
    instruccion_sistema TEXT NOT NULL,
    temperatura DECIMAL(3,2) DEFAULT 0.70,
    max_tokens INT DEFAULT 800,
    activo BOOLEAN DEFAULT TRUE,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 21. INDEXACIÓN DE DOCUMENTOS
-- =========================

CREATE TABLE indexacion_documentos (
    id_indexacion SERIAL PRIMARY KEY,
    id_documento INT NOT NULL REFERENCES documentos_institucionales(id_documento) ON DELETE CASCADE,
    id_modelo_embedding INT REFERENCES modelos_ia(id_modelo) ON DELETE SET NULL,
    estado VARCHAR(30) DEFAULT 'pendiente',
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    cantidad_secciones INT DEFAULT 0,
    vector_store_id TEXT,
    external_file_id TEXT,
    mensaje_error TEXT
);

-- =========================
-- 22. SOLICITUDES A LA IA
-- =========================

CREATE TABLE solicitudes_ia (
    id_solicitud_ia SERIAL PRIMARY KEY,
    id_chat INT REFERENCES chats(id_chat) ON DELETE CASCADE,
    id_mensaje_usuario INT REFERENCES mensajes(id_mensaje) ON DELETE SET NULL,
    id_mensaje_respuesta INT REFERENCES mensajes(id_mensaje) ON DELETE SET NULL,
    id_modelo INT REFERENCES modelos_ia(id_modelo) ON DELETE SET NULL,
    prompt_enviado TEXT,
    respuesta_recibida TEXT,
    tokens_entrada INT DEFAULT 0,
    tokens_salida INT DEFAULT 0,
    costo_estimado DECIMAL(10,6) DEFAULT 0,
    estado VARCHAR(30) DEFAULT 'exitosa',
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tiempo_respuesta_ms INT
);

-- =========================
-- 23. FUENTES USADAS EN LA RESPUESTA
-- =========================

CREATE TABLE fuentes_respuesta (
    id_fuente_respuesta SERIAL PRIMARY KEY,
    id_solicitud_ia INT NOT NULL REFERENCES solicitudes_ia(id_solicitud_ia) ON DELETE CASCADE,
    id_documento INT REFERENCES documentos_institucionales(id_documento) ON DELETE SET NULL,
    id_contenido INT REFERENCES contenido_documento(id_contenido) ON DELETE SET NULL,
    titulo_fuente VARCHAR(150),
    pagina INT,
    fragmento_utilizado TEXT,
    puntaje_similitud DECIMAL(6,4),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- ÍNDICES RECOMENDADOS
-- =========================================================

CREATE INDEX idx_estudiantes_correo ON estudiantes(correo);
CREATE INDEX idx_chats_estudiante ON chats(id_estudiante);
CREATE INDEX idx_mensajes_chat ON mensajes(id_chat);
CREATE INDEX idx_documentos_categoria ON documentos_institucionales(categoria);
CREATE INDEX idx_contenido_documento ON contenido_documento(id_documento);
CREATE INDEX idx_consultas_chat ON consultas_chat(id_chat);
CREATE INDEX idx_solicitudes_ia_chat ON solicitudes_ia(id_chat);
CREATE INDEX idx_fuentes_respuesta_solicitud ON fuentes_respuesta(id_solicitud_ia);