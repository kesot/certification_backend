<!DOCTYPE html>
<html lang="en">
	<!-- Подключение HEADа страницы -->
	<?include("templates/page-head.tpl");?>
<body>
	<div id="wrapper">

		<!-- Подключение шапки сайта -->
		<?include("templates/header.tpl");?>
		
		<div id="main">
			
			<!-- Подключение секции кратко о сервисе -->
			<?include("templates/main-menu.tpl");?>

			<!-- Подключение секции об одном сертификате -->
			<?include("templates/section-adout-cert.tpl");?>

		</div>
		
		<!-- Подключение подвала сайта -->
		<?include("templates/footer.tpl");?>

	</div>
</body>
</html>