-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-11-2023 a las 05:53:30
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `walking_legs`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `atributos`
--

CREATE TABLE `atributos` (
  `id` int(11) NOT NULL,
  `nombre` int(11) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `atributosxusuarios`
--

CREATE TABLE `atributosxusuarios` (
  `id` int(11) NOT NULL,
  `idusuario` int(11) NOT NULL,
  `idatributo` int(11) NOT NULL,
  `descripcion` varchar(250) NOT NULL,
  `valor` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_paseo`
--

CREATE TABLE `detalle_paseo` (
  `id` int(11) NOT NULL,
  `idpaseo` int(11) NOT NULL,
  `idmascota` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `id` int(11) NOT NULL,
  `total` double NOT NULL,
  `descripcion` varchar(250) NOT NULL,
  `idpaseo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mascotas`
--

CREATE TABLE `mascotas` (
  `id_mascotas` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `raza` varchar(255) DEFAULT NULL,
  `genero` varchar(255) DEFAULT NULL,
  `idusuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paseo`
--

CREATE TABLE `paseo` (
  `id` int(11) NOT NULL,
  `idusuario` int(11) NOT NULL,
  `idpaseador` int(11) NOT NULL,
  `hora_inicio` datetime NOT NULL,
  `hora_fin` datetime NOT NULL,
  `estado` varchar(250) NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_role` int(11) NOT NULL,
  `nombre` varchar(250) DEFAULT NULL,
  `descripcion` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_role`, `nombre`, `descripcion`) VALUES
(1, 'Administrador', 'Rol con todos los privilegios'),
(2, 'Usuario', 'Rol destinado a usuarios que deseen pasear a sus mascotas'),
(3, 'Paseador', 'Rol destinado a usuarios que deseen brindar paseos a mascotas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `apellido` varchar(250) NOT NULL,
  `documento` varchar(10) NOT NULL,
  `correo` varchar(250) NOT NULL,
  `contraseña` varchar(250) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `direccion` varchar(250) NOT NULL,
  `idroles` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `documento`, `correo`, `contraseña`, `telefono`, `direccion`, `idroles`) VALUES
(1, 'Hellen', 'Apellido', '1044603092', 'arrietahellen7@gmail.com', 'hellen123', '3012505269', 'Cll 61 #9 - 138', 1),
(2, 'Santiago', 'Altamar', '1045607803', 'santiagoaltamar8@hotmail.com', 'santiago123', '3023055098', 'cll 20 malambo', 2),
(3, 'lina', 'Zamora', '72232605', 'linazamora15@gmail.com', 'lina123', '3014781956', 'cll 60 #10M - 115', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `atributos`
--
ALTER TABLE `atributos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `atributosxusuarios`
--
ALTER TABLE `atributosxusuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idusuario` (`idusuario`),
  ADD KEY `idatributo` (`idatributo`);

--
-- Indices de la tabla `detalle_paseo`
--
ALTER TABLE `detalle_paseo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idpaseo` (`idpaseo`,`idmascota`),
  ADD KEY `idmascota` (`idmascota`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idpaseo` (`idpaseo`);

--
-- Indices de la tabla `mascotas`
--
ALTER TABLE `mascotas`
  ADD PRIMARY KEY (`id_mascotas`),
  ADD KEY `idusuario` (`idusuario`);

--
-- Indices de la tabla `paseo`
--
ALTER TABLE `paseo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idusuario` (`idusuario`,`idpaseador`),
  ADD KEY `idpaseador` (`idpaseador`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_role`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `telefono` (`telefono`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD KEY `idroles` (`idroles`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `atributosxusuarios`
--
ALTER TABLE `atributosxusuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_paseo`
--
ALTER TABLE `detalle_paseo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `paseo`
--
ALTER TABLE `paseo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_role` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `atributosxusuarios`
--
ALTER TABLE `atributosxusuarios`
  ADD CONSTRAINT `atributosxusuarios_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `atributosxusuarios_ibfk_2` FOREIGN KEY (`idatributo`) REFERENCES `atributos` (`id`);

--
-- Filtros para la tabla `detalle_paseo`
--
ALTER TABLE `detalle_paseo`
  ADD CONSTRAINT `detalle_paseo_ibfk_1` FOREIGN KEY (`idpaseo`) REFERENCES `paseo` (`id`),
  ADD CONSTRAINT `detalle_paseo_ibfk_2` FOREIGN KEY (`idmascota`) REFERENCES `mascotas` (`id_mascotas`);

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`idpaseo`) REFERENCES `paseo` (`id`);

--
-- Filtros para la tabla `mascotas`
--
ALTER TABLE `mascotas`
  ADD CONSTRAINT `mascotas_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `paseo`
--
ALTER TABLE `paseo`
  ADD CONSTRAINT `paseo_ibfk_3` FOREIGN KEY (`idpaseador`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `paseo_ibfk_4` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`idroles`) REFERENCES `roles` (`id_role`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
