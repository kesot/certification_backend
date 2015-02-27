<!DOCTYPE html>
<html lang="en">
<head>
	<!-- Подключение HEADа страницы -->
	<?include("templates/page-head.tpl");?>
</head>
<body>
	<div id="wrapper">

		<!-- Подключение шапки сайта -->
		<?include("templates/header.tpl");?>
		
		<div id="main">
			
			<!-- Подключение основного меню -->
			<?include("templates/main-menu.tpl");?>	
			
			<!-- Подключение секции регистрации -->
			<?include("templates/section-registration.tpl");?>	

		</div>
		
		<!-- Подключение подвала сайта -->
		<?include("templates/footer.tpl");?>
	</div>
</body>
</html>