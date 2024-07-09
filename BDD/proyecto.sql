-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-07-2024 a las 00:07:30
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puesto`
--

CREATE TABLE `puesto` (
  `id_p` int(11) NOT NULL,
  `titulo` text NOT NULL,
  `productos` text NOT NULL,
  `ofertas` text NOT NULL,
  `imagen` text NOT NULL,
  `estado` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `puesto`
--

INSERT INTO `puesto` (`id_p`, `titulo`, `productos`, `ofertas`, `imagen`, `estado`) VALUES
(2, 'Puesto Plumones', 'Marcador pizarra azul, marcador pizarra negro', '800 c/u', 'static/uploads\\imagen_2024-07-09_175748982.png', 'activo'),
(1, 'Puesto ramen', 'Ramen, pocky, jugos, tapas', 'ninguna por ahora', 'static/uploads\\imagen_2024-07-09_175922885.png', 'activo'),
(5, 'Puesto pines', 'Pines varios', '1500 c/u', 'static/uploads\\imagen_2024-07-09_180124180.png', 'inactivo'),
(6, 'Puesto rockets', 'Rockets, conitos y energética', 'no', 'static/uploads\\imagen_2024-07-09_180252836.png', 'activo'),
(7, 'Puesto Scores', 'Score', '$1100 c/u', 'static/uploads\\imagen_2024-07-09_180429570.png', 'activo'),
(8, 'Puesto Alfajores', 'Alfajores a 500', 'no', 'static/uploads\\imagen_2024-07-09_180608856.png', 'inactivo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `usuario` varchar(12) NOT NULL,
  `clave` varchar(12) NOT NULL,
  `nombre` text NOT NULL,
  `wsp` text NOT NULL,
  `datos` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `usuario`, `clave`, `nombre`, `wsp`, `datos`) VALUES
(1, 'rouzzen', '12', 'Vicente', '+5696647570', 'misdatos'),
(2, 'burbil', '12', 'diego ', '1239813', 'aklsdja'),
(3, 'alvin', '12', 'alvaro oso', '129384', 'askjdajd'),
(4, 'payolin', '12', 'Claudio', '2847459598', 'aslkdjalskdam d'),
(5, 'pin', '12', 'Daniel', '+56987389804', 'Banco estado, cuenta rut 1284892'),
(6, 'rocket', '12', 'Claudio', '+56981935299', 'Cuenta santander ...'),
(7, 'Score', '12', 'Lucas', '985636798', 'Cuenta BCi/mach 8213710'),
(8, 'alfa', '12', 'Sofia', '+56994320751', 'Cuenta rut N219249028');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
