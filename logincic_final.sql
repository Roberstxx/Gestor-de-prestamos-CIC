-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 19-05-2025 a las 07:31:51
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
-- Base de datos: `logincic_final`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin_keys`
--

CREATE TABLE `admin_keys` (
  `id` int(11) NOT NULL,
  `clave` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `admin_keys`
--

INSERT INTO `admin_keys` (`id`, `clave`) VALUES
(1, 'CLAVEADMIN2025');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas`
--

CREATE TABLE `areas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `tipo_area` varchar(50) NOT NULL,
  `edificio_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `areas`
--

INSERT INTO `areas` (`id`, `nombre`, `tipo_area`, `edificio_id`) VALUES
(5, 'Sala 1', 'Sala CIC', 1),
(6, 'Sala 2', 'Sala CIC', 1),
(7, 'Aula 1', 'Aula', 2),
(8, 'Aula 2', 'Aula', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `edificios`
--

CREATE TABLE `edificios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `sesion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `edificios`
--

INSERT INTO `edificios` (`id`, `nombre`, `sesion_id`) VALUES
(1, 'Edificio A', 1),
(2, 'Edificio B', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_prestamos`
--

CREATE TABLE `historial_prestamos` (
  `id` int(11) NOT NULL,
  `prestamo_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `accion` enum('prestado','devuelto','cancelado','modificado') NOT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `numero_serie` varchar(100) DEFAULT NULL,
  `fecha_adquisicion` date NOT NULL,
  `estado` enum('Disponible','Prestado','Baja') DEFAULT 'Disponible',
  `observaciones` text DEFAULT NULL,
  `sesion_id` int(11) DEFAULT NULL,
  `stock` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id`, `nombre`, `tipo`, `marca`, `numero_serie`, `fecha_adquisicion`, `estado`, `observaciones`, `sesion_id`, `stock`) VALUES
(1, 'Laptop Dell', 'Laptop', 'Dell', 'ABC123', '2023-08-10', 'Disponible', 'Buen estado', 1, 0),
(2, 'Proyector Epson', 'Proyector', 'Epson', 'EPS456', '2023-09-01', 'Disponible', NULL, 1, 1),
(3, 'Mouse Logitech', 'Accesorio', 'Logitech', 'LOG789', '2022-12-15', 'Disponible', '', 1, 1),
(12, 'HDMI', 'Cable', 'ZXT', '6746749', '2025-05-19', 'Disponible', NULL, 0, 1),
(14, 'Lap Top', 'PC', 'ZXT', '6746748', '2025-05-19', 'Disponible', NULL, 0, 2),
(18, 'HDMI', 'Cable', 'ZXT', '6746799', '2025-05-19', 'Disponible', NULL, NULL, 8),
(19, 'VGA', 'Cable', 'ZXT', '9746749', '2025-05-19', 'Disponible', NULL, NULL, 2),
(20, 'Compu de Escritorio', 'PC', 'ZXT', '9786949', '2025-05-19', 'Disponible', NULL, NULL, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `inventario_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL CHECK (`cantidad` > 0),
  `fecha_prestamo` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_devolucion` datetime DEFAULT NULL,
  `devuelto` tinyint(1) NOT NULL DEFAULT 0,
  `sesion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamos`
--

INSERT INTO `prestamos` (`id`, `usuario_id`, `admin_id`, `inventario_id`, `area_id`, `profesor_id`, `cantidad`, `fecha_prestamo`, `fecha_devolucion`, `devuelto`, `sesion_id`) VALUES
(2, 2, 1, 2, 8, 1, 1, '2025-05-17 02:03:43', '2025-05-17 02:11:07', 1, 1),
(3, 2, 1, 2, 8, 1, 1, '2025-05-17 02:07:30', '2025-05-17 02:11:08', 1, 1),
(4, 2, 1, 3, 6, 2, 1, '2025-05-17 02:07:56', '2025-05-17 02:11:09', 1, 1),
(5, 2, 1, 1, 5, 1, 1, '2025-05-17 02:52:54', '2025-05-17 02:52:58', 1, 1),
(6, 2, 1, 2, 5, 1, 1, '2025-05-18 00:04:06', '2025-05-18 00:14:39', 1, 1),
(7, 2, 1, 3, 5, 1, 1, '2025-05-18 00:15:14', '2025-05-18 00:16:45', 1, 1),
(8, 2, 1, 1, 5, 1, 1, '2025-05-18 00:16:34', '2025-05-18 00:16:47', 1, 1),
(9, 2, 1, 3, 6, 1, 1, '2025-05-18 00:36:51', '2025-05-18 00:37:49', 1, 1),
(10, 2, 1, 1, 5, 1, 1, '2025-05-18 00:37:09', '2025-05-18 16:38:31', 1, 1),
(11, 1, 1, 3, 7, 1, 1, '2025-05-18 16:38:02', '2025-05-18 16:38:32', 1, 1),
(12, 1, 1, 3, 5, 1, 1, '2025-05-18 16:50:56', '2025-05-18 16:51:06', 1, 1),
(13, 1, 1, 2, 5, 1, 1, '2025-05-18 16:55:02', '2025-05-18 20:52:51', 1, 1),
(14, 2, 1, 3, 5, 1, 1, '2025-05-18 20:52:34', '2025-05-18 20:52:50', 1, 1),
(15, 2, 1, 1, 5, 1, 1, '2025-05-18 22:02:49', NULL, 0, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `matricula` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`id`, `nombre`, `correo`, `matricula`) VALUES
(1, 'Prof. María Gómez', 'maria@uacam.mx', '71315'),
(2, 'Prof. Juan López', 'david69@gmail.com', '71316'),
(3, 'Alan Sauriel', '0l070838', '70065'),
(4, 'Luis martin', 'al071456@uacam.mx', '71456'),
(8, 'EDWIN ABRAHAN', 'david69@gmail.com', '71319');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

CREATE TABLE `sesiones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `clave` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sesiones`
--

INSERT INTO `sesiones` (`id`, `nombre`, `clave`) VALUES
(1, 'Roberto martin omez', 'CLAVE-1-scottdanieljonson');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','student') NOT NULL,
  `sesion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password`, `rol`, `sesion_id`) VALUES
(1, 'Roberto martin omez', 'scottdanieljonson@gmail.com', 'scrypt:32768:8:1$THRzj0AbTH3bXZai$536636af13ac856566c8e71fb88930cc054d174496bcc5a5eadcd012993b7d38bda03ae8a85e5a1582286bffcd9e8c85b8b463a231f63d8ec2dfe5bac0dd67cf', 'admin', 1),
(2, 'Alan sauriel Chan', 'arturhat942@gmail.com', 'scrypt:32768:8:1$J0itqsH9Og8PYKcT$d31c30dc99afd7859230b028a196dcf21cef7dbcd063e044138c1ef8a7999fc3a08a4253c0c7455cd1faae9807ca36f1321b65273a637408798c870fbe0766fb', 'student', 1),
(3, 'ROBERTO ANTONIO', 'tylerroberts942@gmail.com', 'scrypt:32768:8:1$jDh4KEdtc6542YUR$072b5dcfc786098f01861a2326c7df943576473071626e1ec05ece6915848f15179492fb8c91f9324b713a439060db46a7f780b300bf94db20e9e76fed45f538', 'student', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin_keys`
--
ALTER TABLE `admin_keys`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `clave` (`clave`);

--
-- Indices de la tabla `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `edificio_id` (`edificio_id`);

--
-- Indices de la tabla `edificios`
--
ALTER TABLE `edificios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sesion_id` (`sesion_id`);

--
-- Indices de la tabla `historial_prestamos`
--
ALTER TABLE `historial_prestamos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `prestamo_id` (`prestamo_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_serie` (`numero_serie`),
  ADD KEY `sesion_id` (`sesion_id`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `inventario_id` (`inventario_id`),
  ADD KEY `area_id` (`area_id`),
  ADD KEY `profesor_id` (`profesor_id`),
  ADD KEY `sesion_id` (`sesion_id`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `matricula` (`matricula`);

--
-- Indices de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `clave` (`clave`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `sesion_id` (`sesion_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admin_keys`
--
ALTER TABLE `admin_keys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `areas`
--
ALTER TABLE `areas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `edificios`
--
ALTER TABLE `edificios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `historial_prestamos`
--
ALTER TABLE `historial_prestamos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `areas`
--
ALTER TABLE `areas`
  ADD CONSTRAINT `areas_ibfk_1` FOREIGN KEY (`edificio_id`) REFERENCES `edificios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `edificios`
--
ALTER TABLE `edificios`
  ADD CONSTRAINT `edificios_ibfk_1` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `historial_prestamos`
--
ALTER TABLE `historial_prestamos`
  ADD CONSTRAINT `historial_prestamos_ibfk_1` FOREIGN KEY (`prestamo_id`) REFERENCES `prestamos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `historial_prestamos_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_3` FOREIGN KEY (`inventario_id`) REFERENCES `inventario` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_4` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_5` FOREIGN KEY (`profesor_id`) REFERENCES `profesores` (`id`),
  ADD CONSTRAINT `prestamos_ibfk_6` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
