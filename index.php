<?php

	$location = $_SERVER['REQUEST_URI'];
?>

<!DOCTYPE html>
<html lang="en">
	<!-- Подключение HEADа страницы -->
	<?include("templates/page-head.php");?>
<body>
	<div id="wrapper">

		<!-- Подключение шапки сайта -->
		<?include("templates/header.php");?>
		
		<div id="main">
			
			<!-- Подключение основного меню -->
			<?include("templates/main-menu.php");?>

			<!-- Подключение секции кратко о сервисе -->
			<?//include("templates/section-about.php");?>

			<?php

			switch ($location) {
				case '/registration':
					include("templates/section-registration.php");
					break;
				
				case '/registration_comp':
					include("templates/section-reg-company.php");
					break;

				case '/cart':
					include("templates/section-cart.php");
					break;

				case '/restore':
					include("templates/section-restore.php");
					break;

				case '/profile':
					// include("templates/section-profile.php");
				include("templates/section-profile-comp.php");

					break;

				case '/edit_profile':
					
					// если обычный пользователь и если пользователь из компании
					
					// include("templates/section-edit-profile-user.php");
					include("templates/section-edit-profile-comp.php");
					break;

				case '/new_certificate':
					include("templates/section-new-certificates.php");
					break;
				case '/edit_certificates':
					include("templates/section-edit-certificates.php");
					break;

				case '/order':
					include("templates/section-order.php");
					break;

				case '/companies':
					include("templates/section-companies.php");
					break;

				case '/certificates_all':
					include("templates/section-certificates.php");
					break;

				case '/certificates_one':
					include("templates/section-about-cert.php");
					break;

				case '/certificates_by_company':
					include("templates/section-certificates.php");
					break;

				case '/logout':
					
					break;
				
				default:
					// Подключение секции рекламы
					include("templates/section-advertising.php");
					break;
			}

			?>
			
			
		</div>
		
		<!-- Подключение подвала сайта -->
		<?include("templates/footer.php");?>

	</div>
</body>
</html>