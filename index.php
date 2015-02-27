<!DOCTYPE html>
<html lang="en">
	<!-- Подключение HEADа страницы -->
	<?include("templates/page-head.tpl");?>
<body>
	<div id="wrapper">

		<!-- Подключение шапки сайта -->
		<?include("templates/header.tpl");?>
		
		<div id="main">

			<!-- Подключение основного меню -->
			<?include("templates/main-menu.tpl");?>

			<!-- Подключение секции кратко о сервисе -->
			<?include("templates/section-about.tpl");?>
			
			<!-- Подключение секции рекламы -->
			<?include("templates/section-advertising.tpl");?>

		</div>
		
		<!-- Подключение подвала сайта -->
		<?include("templates/footer.tpl");?>

	</div>
</body>
</html>