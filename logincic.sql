-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 08-05-2025 a las 15:48:19
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
-- Base de datos: `logincic`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin_keys`
--

CREATE TABLE `admin_keys` (
  `id` int(11) NOT NULL,
  `key` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `admin_keys`
--

INSERT INTO `admin_keys` (`id`, `key`) VALUES
(1, 'CLAVEADMIN123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos_realizados`
--

CREATE TABLE `prestamos_realizados` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `sesion_id` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `nombre` varchar(100) DEFAULT NULL,
  `matricula` varchar(20) DEFAULT NULL,
  `tipo_area` varchar(50) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `edificio` varchar(50) DEFAULT NULL,
  `equipo` text DEFAULT NULL,
  `cantidad` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

CREATE TABLE `sesiones` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `clave` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sesiones`
--

INSERT INTO `sesiones` (`id`, `admin_id`, `nombre`, `clave`) VALUES
(1, 0, 'Roberto martin omez', 'CLAVE-1-scottdanieljonson');

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
  `sesion_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password`, `rol`, `sesion_id`) VALUES
(1, 'Roberto martin omez', 'scottdanieljonson@gmail.com', 'scrypt:32768:8:1$drz5NFMvJWYpLGtA$ed912ced87db8f80ba88003694ed643eb4f7f93edd9f261f2172b15f48f672443285b03c8079e72da616c57161e4f72f1cd4a9a51601c92327ade5915c878c09', 'admin', 1),
(2, 'Alan ', 'arturhat942@gmail.com', 'scrypt:32768:8:1$sb1W1u4O5t97KMFh$bb7988d885d7a56449f1358ef18c8f6f389d2e83fe430f9078d8f2729112cc61b68c996365f0fd125677197f508df9037cfb3c7f54f543c6c436ef0017198934', 'student', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin_keys`
--
ALTER TABLE `admin_keys`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`);

--
-- Indices de la tabla `prestamos_realizados`
--
ALTER TABLE `prestamos_realizados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `sesion_id` (`sesion_id`);

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
-- AUTO_INCREMENT de la tabla `prestamos_realizados`
--
ALTER TABLE `prestamos_realizados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `prestamos_realizados`
--
ALTER TABLE `prestamos_realizados`
  ADD CONSTRAINT `prestamos_realizados_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `prestamos_realizados_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `prestamos_realizados_ibfk_3` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
