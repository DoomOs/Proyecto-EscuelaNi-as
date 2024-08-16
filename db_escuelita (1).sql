-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-08-2024 a las 17:27:01
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_escuelita`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad_actividad`
--

CREATE TABLE `actividad_actividad` (
  `id` bigint(20) NOT NULL,
  `actividad` varchar(100) NOT NULL,
  `punteo` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `curso_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad_calificacionactividad`
--

CREATE TABLE `actividad_calificacionactividad` (
  `id` bigint(20) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `punteo` int(11) NOT NULL,
  `actividad_id` bigint(20) NOT NULL,
  `asignacion_ciclo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion_ciclo_asignacionciclo`
--

CREATE TABLE `asignacion_ciclo_asignacionciclo` (
  `id` bigint(20) NOT NULL,
  `year` int(11) NOT NULL,
  `alumna_id` bigint(20) NOT NULL,
  `grado_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `asignacion_ciclo_asignacionciclo`
--

INSERT INTO `asignacion_ciclo_asignacionciclo` (`id`, `year`, `alumna_id`, `grado_id`, `user_id`) VALUES
(1, 2024, 1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia_asistencia`
--

CREATE TABLE `asistencia_asistencia` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `presente` tinyint(1) NOT NULL,
  `asignacion_ciclo_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add carrusel', 6, 'add_carrusel'),
(22, 'Can change carrusel', 6, 'change_carrusel'),
(23, 'Can delete carrusel', 6, 'delete_carrusel'),
(24, 'Can view carrusel', 6, 'view_carrusel'),
(25, 'Can add user', 7, 'add_user'),
(26, 'Can change user', 7, 'change_user'),
(27, 'Can delete user', 7, 'delete_user'),
(28, 'Can view user', 7, 'view_user'),
(29, 'Can add rol', 8, 'add_rol'),
(30, 'Can change rol', 8, 'change_rol'),
(31, 'Can delete rol', 8, 'delete_rol'),
(32, 'Can view rol', 8, 'view_rol'),
(33, 'Can add persona', 9, 'add_persona'),
(34, 'Can change persona', 9, 'change_persona'),
(35, 'Can delete persona', 9, 'delete_persona'),
(36, 'Can view persona', 9, 'view_persona'),
(37, 'Can add alumna', 10, 'add_alumna'),
(38, 'Can change alumna', 10, 'change_alumna'),
(39, 'Can delete alumna', 10, 'delete_alumna'),
(40, 'Can view alumna', 10, 'view_alumna'),
(41, 'Can add contacto', 11, 'add_contacto'),
(42, 'Can change contacto', 11, 'change_contacto'),
(43, 'Can delete contacto', 11, 'delete_contacto'),
(44, 'Can view contacto', 11, 'view_contacto'),
(45, 'Can add asignacion ciclo', 12, 'add_asignacionciclo'),
(46, 'Can change asignacion ciclo', 12, 'change_asignacionciclo'),
(47, 'Can delete asignacion ciclo', 12, 'delete_asignacionciclo'),
(48, 'Can view asignacion ciclo', 12, 'view_asignacionciclo'),
(49, 'Can add actividad', 13, 'add_actividad'),
(50, 'Can change actividad', 13, 'change_actividad'),
(51, 'Can delete actividad', 13, 'delete_actividad'),
(52, 'Can view actividad', 13, 'view_actividad'),
(53, 'Can add calificacion actividad', 14, 'add_calificacionactividad'),
(54, 'Can change calificacion actividad', 14, 'change_calificacionactividad'),
(55, 'Can delete calificacion actividad', 14, 'delete_calificacionactividad'),
(56, 'Can view calificacion actividad', 14, 'view_calificacionactividad'),
(57, 'Can add asistencia', 15, 'add_asistencia'),
(58, 'Can change asistencia', 15, 'change_asistencia'),
(59, 'Can delete asistencia', 15, 'delete_asistencia'),
(60, 'Can view asistencia', 15, 'view_asistencia'),
(61, 'Can add grado', 16, 'add_grado'),
(62, 'Can change grado', 16, 'change_grado'),
(63, 'Can delete grado', 16, 'delete_grado'),
(64, 'Can view grado', 16, 'view_grado'),
(65, 'Can add curso', 17, 'add_curso'),
(66, 'Can change curso', 17, 'change_curso'),
(67, 'Can delete curso', 17, 'delete_curso'),
(68, 'Can view curso', 17, 'view_curso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `curso_curso`
--

CREATE TABLE `curso_curso` (
  `id` bigint(20) NOT NULL,
  `nombre_curso` varchar(100) NOT NULL,
  `grado_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `curso_curso`
--

INSERT INTO `curso_curso` (`id`, `nombre_curso`, `grado_id`) VALUES
(2, 'Matematicas', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `curso_grado`
--

CREATE TABLE `curso_grado` (
  `id` bigint(20) NOT NULL,
  `nombre_grado` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `curso_grado`
--

INSERT INTO `curso_grado` (`id`, `nombre_grado`) VALUES
(1, '1ro.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(13, 'Actividad', 'actividad'),
(14, 'Actividad', 'calificacionactividad'),
(1, 'admin', 'logentry'),
(12, 'Asignacion_Ciclo', 'asignacionciclo'),
(15, 'Asistencia', 'asistencia'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(17, 'Curso', 'curso'),
(16, 'Curso', 'grado'),
(10, 'Persona', 'alumna'),
(11, 'Persona', 'contacto'),
(9, 'Persona', 'persona'),
(5, 'sessions', 'session'),
(8, 'user', 'rol'),
(7, 'user', 'user'),
(6, 'Web', 'carrusel');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'Curso', '0001_initial', '2024-08-15 18:45:11.259220'),
(2, 'contenttypes', '0001_initial', '2024-08-15 18:45:11.307325'),
(3, 'contenttypes', '0002_remove_content_type_name', '2024-08-15 18:45:11.395302'),
(4, 'auth', '0001_initial', '2024-08-15 18:45:11.673778'),
(5, 'auth', '0002_alter_permission_name_max_length', '2024-08-15 18:45:11.731626'),
(6, 'auth', '0003_alter_user_email_max_length', '2024-08-15 18:45:11.738604'),
(7, 'auth', '0004_alter_user_username_opts', '2024-08-15 18:45:11.746583'),
(8, 'auth', '0005_alter_user_last_login_null', '2024-08-15 18:45:11.755559'),
(9, 'auth', '0006_require_contenttypes_0002', '2024-08-15 18:45:11.758551'),
(10, 'auth', '0007_alter_validators_add_error_messages', '2024-08-15 18:45:11.766531'),
(11, 'auth', '0008_alter_user_username_max_length', '2024-08-15 18:45:11.773511'),
(12, 'auth', '0009_alter_user_last_name_max_length', '2024-08-15 18:45:11.782487'),
(13, 'auth', '0010_alter_group_name_max_length', '2024-08-15 18:45:11.797447'),
(14, 'auth', '0011_update_proxy_permissions', '2024-08-15 18:45:11.806423'),
(15, 'auth', '0012_alter_user_first_name_max_length', '2024-08-15 18:45:11.815399'),
(16, 'user', '0001_initial', '2024-08-15 18:45:12.375678'),
(17, 'Persona', '0001_initial', '2024-08-15 18:45:12.890302'),
(18, 'Asignacion_Ciclo', '0001_initial', '2024-08-15 18:45:13.138170'),
(19, 'Actividad', '0001_initial', '2024-08-15 18:45:13.657585'),
(20, 'Persona', '0002_remove_alumna_grado', '2024-08-15 18:45:17.659100'),
(21, 'Asignacion_Ciclo', '0002_alter_asignacionciclo_unique_together', '2024-08-15 18:45:17.696034'),
(22, 'Asistencia', '0001_initial', '2024-08-15 18:45:17.805770'),
(23, 'Web', '0001_initial', '2024-08-15 18:45:17.824709'),
(24, 'Web', '0002_initial', '2024-08-15 18:45:17.912475'),
(25, 'admin', '0001_initial', '2024-08-15 18:45:18.087008'),
(26, 'admin', '0002_logentry_remove_auto_add', '2024-08-15 18:45:18.099973'),
(27, 'admin', '0003_logentry_add_action_flag_choices', '2024-08-15 18:45:18.115931'),
(28, 'sessions', '0001_initial', '2024-08-15 18:45:18.149840'),
(29, 'user', '0002_rol_alter_user_options_remove_user_compras_and_more', '2024-08-15 18:45:18.737834'),
(30, 'user', '0003_remove_user_estado', '2024-08-15 18:45:18.765752');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3ibf6odgdlmnsqzhqdj3k8vbf1dfp9ax', '.eJxVjjsOwyAQRO9CHSHW_EzK9D4DWlgcnMRGMnYV5e6xJYqknTfzNG_mcd-y32ta_UTsyoBdfrOA8ZmWE9ADl3vhsSzbOgV-VnijlQ-F0uvWun-CjDUfa6NBSkChlSNhERLKOEKvoXO9NgrsGE2EZK0EcMIEGQ11IQhySEaRPaRzmkN7CZ8v09Q7gw:1sefV0:lv6omWbWXEb-ChHh5irY1W1dQ-0Y9r0VewxxT3_YqqE', '2024-08-29 18:47:02.975609');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona_alumna`
--

CREATE TABLE `persona_alumna` (
  `id` bigint(20) NOT NULL,
  `codigo` varchar(30) NOT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `persona_alumna`
--

INSERT INTO `persona_alumna` (`id`, `codigo`, `persona_id`) VALUES
(1, '19002', 2),
(3, '12', 4),
(4, '19002', 5),
(6, '190021', 6),
(7, '19002', 9),
(8, '19002', 12),
(10, '19002', 14),
(11, '19002', 16),
(13, '19002', 19),
(16, '19002', 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona_contacto`
--

CREATE TABLE `persona_contacto` (
  `id` bigint(20) NOT NULL,
  `parentesco` varchar(50) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `alumna_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `persona_contacto`
--

INSERT INTO `persona_contacto` (`id`, `parentesco`, `telefono`, `email`, `alumna_id`, `user_id`, `persona_id`) VALUES
(1, 'Papá', '59289591', 'asdasd', 1, NULL, 3),
(2, 'Papá', '12345678', 'mail@gmail.com', NULL, NULL, 7),
(3, 'Papá', '12345678', 'mail@gmail.com', NULL, NULL, 8),
(4, 'Papá', '12345678', 'mail@gmail.com', 7, NULL, 10),
(5, 'Mamá', '12345678', 'mail@gmail.com', NULL, NULL, 11),
(6, 'Mamá', '12345678', 'mail@gmail.com', 8, NULL, 13),
(7, 'Hermana', '12345678', 'mail@gmail.com', 10, NULL, 15),
(8, 'Mamá', '12345678', 'mail@gmail.com', 11, NULL, 17),
(9, 'Mamá', '12345678', 'mail@gmail.com', 11, NULL, 18),
(10, 'Papá', '12345678', 'mail@gmail.com', 16, NULL, 21);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona_persona`
--

CREATE TABLE `persona_persona` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `genero` varchar(1) NOT NULL,
  `direccion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `persona_persona`
--

INSERT INTO `persona_persona` (`id`, `nombre`, `apellido`, `fecha_nacimiento`, `genero`, `direccion`) VALUES
(1, 'Josefina', 'fina', '2008-11-02', 'F', 'su casa'),
(2, 'Josefinaqwr', 'fina', '2024-07-28', 'M', 'su casa'),
(3, 'Bryan', 'Sosa', '2024-08-15', 'M', '1ra calle- 3-54, zona 4'),
(4, 'Josefinaa', 'fina', '2024-08-15', 'M', 'su casa'),
(5, 'Josefinaa1', 'fina', '2024-08-15', 'M', 'su casa'),
(6, 'Pedroas', 'Juarez', '2024-08-15', 'M', 'su casa'),
(7, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(8, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(9, 'Maria', 'as', '2024-08-15', 'F', 'su casa'),
(10, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(11, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(12, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(13, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(14, 'Pedro', 'Juarez', '2024-08-15', 'F', 'su casa'),
(15, 'Pedro', 'Juarez', '2024-08-15', 'F', 'su casa'),
(16, 'Maria', 'as', '2024-01-23', 'M', 'su casa'),
(17, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(18, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa'),
(19, 'Maria', 'as', '2024-08-15', 'M', 'su casa'),
(20, 'Maria', 'as', '2024-08-15', 'M', 'su casa'),
(21, 'Pedrita', 'Juarez', '2024-08-15', 'M', 'su casa'),
(22, 'Pedro', 'Juarez', '2024-08-15', 'M', 'su casa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_rol`
--

CREATE TABLE `user_rol` (
  `id` bigint(20) NOT NULL,
  `rol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_user`
--

CREATE TABLE `user_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id_ciclo` int(11) DEFAULT NULL,
  `telefono` varchar(10) NOT NULL,
  `id_rol_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `user_user`
--

INSERT INTO `user_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `id_ciclo`, `telefono`, `id_rol_id`) VALUES
(1, 'pbkdf2_sha256$720000$edlgiH60ETQeHNvzQjfqyq$of9EdPtvPe8jN3cHNVUexuyq9640UtJWZjxgU+VgODM=', '2024-08-15 18:47:02.971620', 1, 'admin', 'Admin', 'Feliz', 'admin@email.com', 1, 1, '2024-08-15 18:46:04.546947', NULL, '', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_user_groups`
--

CREATE TABLE `user_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_user_user_permissions`
--

CREATE TABLE `user_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `web_carrusel`
--

CREATE TABLE `web_carrusel` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `descripcion` varchar(250) DEFAULT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `fecha` datetime(6) DEFAULT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad_actividad`
--
ALTER TABLE `actividad_actividad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Actividad_actividad_curso_id_44625e6c_fk_Curso_curso_id` (`curso_id`);

--
-- Indices de la tabla `actividad_calificacionactividad`
--
ALTER TABLE `actividad_calificacionactividad`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Actividad_calificacionac_actividad_id_asignacion__f853a63d_uniq` (`actividad_id`,`asignacion_ciclo_id`),
  ADD KEY `Actividad_calificaci_asignacion_ciclo_id_7db7a8e6_fk_Asignacio` (`asignacion_ciclo_id`);

--
-- Indices de la tabla `asignacion_ciclo_asignacionciclo`
--
ALTER TABLE `asignacion_ciclo_asignacionciclo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Asignacion_Ciclo_asignacionciclo_alumna_id_year_c7458c49_uniq` (`alumna_id`,`year`),
  ADD KEY `Asignacion_Ciclo_asi_grado_id_03c5f10e_fk_Curso_gra` (`grado_id`),
  ADD KEY `Asignacion_Ciclo_asi_user_id_72541700_fk_user_user` (`user_id`);

--
-- Indices de la tabla `asistencia_asistencia`
--
ALTER TABLE `asistencia_asistencia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Asistencia_asistenci_asignacion_ciclo_id_4a80d097_fk_Asignacio` (`asignacion_ciclo_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `curso_curso`
--
ALTER TABLE `curso_curso`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Curso_curso_grado_id_26936d59_fk_Curso_grado_id` (`grado_id`);

--
-- Indices de la tabla `curso_grado`
--
ALTER TABLE `curso_grado`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_user_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `persona_alumna`
--
ALTER TABLE `persona_alumna`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `persona_id` (`persona_id`);

--
-- Indices de la tabla `persona_contacto`
--
ALTER TABLE `persona_contacto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Persona_contacto_alumna_id_b1a80955_fk_Persona_alumna_id` (`alumna_id`),
  ADD KEY `Persona_contacto_user_id_87859761_fk_user_user_id` (`user_id`),
  ADD KEY `Persona_contacto_persona_id_56aac47a_fk_Persona_persona_id` (`persona_id`);

--
-- Indices de la tabla `persona_persona`
--
ALTER TABLE `persona_persona`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `user_rol`
--
ALTER TABLE `user_rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `user_user`
--
ALTER TABLE `user_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `user_user_id_rol_id_041d0473_fk_user_rol_id` (`id_rol_id`);

--
-- Indices de la tabla `user_user_groups`
--
ALTER TABLE `user_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_user_groups_user_id_group_id_bb60391f_uniq` (`user_id`,`group_id`),
  ADD KEY `user_user_groups_group_id_c57f13c0_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `user_user_user_permissions`
--
ALTER TABLE `user_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_user_user_permissions_user_id_permission_id_64f4d5b8_uniq` (`user_id`,`permission_id`),
  ADD KEY `user_user_user_permi_permission_id_ce49d4de_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `web_carrusel`
--
ALTER TABLE `web_carrusel`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Web_carrusel_usuario_id_4914e437_fk_user_user_id` (`usuario_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividad_actividad`
--
ALTER TABLE `actividad_actividad`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `actividad_calificacionactividad`
--
ALTER TABLE `actividad_calificacionactividad`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asignacion_ciclo_asignacionciclo`
--
ALTER TABLE `asignacion_ciclo_asignacionciclo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `asistencia_asistencia`
--
ALTER TABLE `asistencia_asistencia`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT de la tabla `curso_curso`
--
ALTER TABLE `curso_curso`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `curso_grado`
--
ALTER TABLE `curso_grado`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `persona_alumna`
--
ALTER TABLE `persona_alumna`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `persona_contacto`
--
ALTER TABLE `persona_contacto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `persona_persona`
--
ALTER TABLE `persona_persona`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `user_rol`
--
ALTER TABLE `user_rol`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user_user`
--
ALTER TABLE `user_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `user_user_groups`
--
ALTER TABLE `user_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user_user_user_permissions`
--
ALTER TABLE `user_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `web_carrusel`
--
ALTER TABLE `web_carrusel`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividad_actividad`
--
ALTER TABLE `actividad_actividad`
  ADD CONSTRAINT `Actividad_actividad_curso_id_44625e6c_fk_Curso_curso_id` FOREIGN KEY (`curso_id`) REFERENCES `curso_curso` (`id`);

--
-- Filtros para la tabla `actividad_calificacionactividad`
--
ALTER TABLE `actividad_calificacionactividad`
  ADD CONSTRAINT `Actividad_calificaci_actividad_id_8c0cd829_fk_Actividad` FOREIGN KEY (`actividad_id`) REFERENCES `actividad_actividad` (`id`),
  ADD CONSTRAINT `Actividad_calificaci_asignacion_ciclo_id_7db7a8e6_fk_Asignacio` FOREIGN KEY (`asignacion_ciclo_id`) REFERENCES `asignacion_ciclo_asignacionciclo` (`id`);

--
-- Filtros para la tabla `asignacion_ciclo_asignacionciclo`
--
ALTER TABLE `asignacion_ciclo_asignacionciclo`
  ADD CONSTRAINT `Asignacion_Ciclo_asi_alumna_id_87ca7339_fk_Persona_a` FOREIGN KEY (`alumna_id`) REFERENCES `persona_alumna` (`id`),
  ADD CONSTRAINT `Asignacion_Ciclo_asi_grado_id_03c5f10e_fk_Curso_gra` FOREIGN KEY (`grado_id`) REFERENCES `curso_grado` (`id`),
  ADD CONSTRAINT `Asignacion_Ciclo_asi_user_id_72541700_fk_user_user` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`);

--
-- Filtros para la tabla `asistencia_asistencia`
--
ALTER TABLE `asistencia_asistencia`
  ADD CONSTRAINT `Asistencia_asistenci_asignacion_ciclo_id_4a80d097_fk_Asignacio` FOREIGN KEY (`asignacion_ciclo_id`) REFERENCES `asignacion_ciclo_asignacionciclo` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `curso_curso`
--
ALTER TABLE `curso_curso`
  ADD CONSTRAINT `Curso_curso_grado_id_26936d59_fk_Curso_grado_id` FOREIGN KEY (`grado_id`) REFERENCES `curso_grado` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`);

--
-- Filtros para la tabla `persona_alumna`
--
ALTER TABLE `persona_alumna`
  ADD CONSTRAINT `Persona_alumna_persona_id_a385df50_fk_Persona_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`);

--
-- Filtros para la tabla `persona_contacto`
--
ALTER TABLE `persona_contacto`
  ADD CONSTRAINT `Persona_contacto_alumna_id_b1a80955_fk_Persona_alumna_id` FOREIGN KEY (`alumna_id`) REFERENCES `persona_alumna` (`id`),
  ADD CONSTRAINT `Persona_contacto_persona_id_56aac47a_fk_Persona_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`),
  ADD CONSTRAINT `Persona_contacto_user_id_87859761_fk_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`);

--
-- Filtros para la tabla `user_user`
--
ALTER TABLE `user_user`
  ADD CONSTRAINT `user_user_id_rol_id_041d0473_fk_user_rol_id` FOREIGN KEY (`id_rol_id`) REFERENCES `user_rol` (`id`);

--
-- Filtros para la tabla `user_user_groups`
--
ALTER TABLE `user_user_groups`
  ADD CONSTRAINT `user_user_groups_group_id_c57f13c0_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `user_user_groups_user_id_13f9a20d_fk_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`);

--
-- Filtros para la tabla `user_user_user_permissions`
--
ALTER TABLE `user_user_user_permissions`
  ADD CONSTRAINT `user_user_user_permi_permission_id_ce49d4de_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `user_user_user_permissions_user_id_31782f58_fk_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`);

--
-- Filtros para la tabla `web_carrusel`
--
ALTER TABLE `web_carrusel`
  ADD CONSTRAINT `Web_carrusel_usuario_id_4914e437_fk_user_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `user_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
