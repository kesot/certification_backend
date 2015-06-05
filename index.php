<?php

	include("requestHandler.php");

	$location = $_SERVER['REQUEST_URI'];
	if( ($pos = (stripos($location,'?'))) > 0 )
		$location = substr($location,0,$pos);

	$user = get_user();


	switch ($location) {
		case '/login':

			if(isset($_POST['login']) && !empty($_POST['login']))
				// && isset($_POST['password']) && !empty($_POST['password']))
				user_auth();
				@header('Location: http://cert.ru:8888');
			break;

		case '/logout':
			
			user_logout();
			@header('Location: http://cert.ru:8888');

			break;

		case '/registration':

			if(isset($_POST['login']) && !empty($_POST['login'])
				&& isset($_POST['password']) && !empty($_POST['password'])
				&& isset($_POST['repassword']) && !empty($_POST['repassword'])){
				send_user_regData();
				@header('Location: http://cert.ru:8888');
			}


			break;

		case '/send_update_user':

			send_user_editData();

			header('Location: http://cert.ru:8888/profile');
			
			break;

		case '/send_update_agent':

			send_agent_editData();

			header('Location: http://cert.ru:8888/profile');
			
			break;
		
		case '/add_to_cart':

			if(!isset($_COOKIE['code'])){
				echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
				break;
			}
			if($user['type'] == '1'){
				echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
				break;
			}

			if(!add_to_cart()){
				echo "Error!";
			}

			@header('Location:'.$_SERVER['HTTP_REFERER']);
			
			break;

		case '/rm_cert':

			delete_from_cart();
			@header('Location: http://cert.ru:8888/cart');

			break;
		
		case '/reg_comp_agent':

			if(isset($_POST['login']) && !empty($_POST['login'])
				&& isset($_POST['password']) && !empty($_POST['password'])
				&& isset($_POST['repassword']) && !empty($_POST['repassword'])){
				send_agent_regData();
				@header('Location: http://cert.ru:8888');
			}

			break;

		case '/add_template':

			if(isset($_POST['name']) && !empty($_POST['name'])
				&& isset($_POST['AdministrativeName']) && !empty($_POST['AdministrativeName'])
				&& isset($_POST['Descitption']) && !empty($_POST['Descitption'])
				&& isset($_POST['price']) && !empty($_POST['price'])
				&& isset($_POST['CostValue']) && !empty($_POST['CostValue'])
				&& isset($_POST['mask']) && !empty($_POST['mask'])){
					$ans = add_templates();
					if($ans){
						$uploaddir = '';
						$uploadfile = $uploaddir . basename($ans['id'].'.jpg');

						if (move_uploaded_file($_FILES['photo']['tmp_name'], $uploadfile)) {
						    
						} else {
						    
						}
					}
					@header('Location: http://cert.ru:8888/profile');
				}

			break;

		case '/update_template':

			if(isset($_POST['name']) && !empty($_POST['name'])
				&& isset($_POST['AdministrativeName']) && !empty($_POST['AdministrativeName'])
				&& isset($_POST['Descitption']) && !empty($_POST['Descitption'])
				&& isset($_POST['price']) && !empty($_POST['price'])
				&& isset($_POST['CostValue']) && !empty($_POST['CostValue'])){
				$ans = update_templates();

				$uploaddir = '';
				$uploadfile = $uploaddir . basename($_POST['id'].'.jpg');

				if (move_uploaded_file($_FILES['photo']['tmp_name'], $uploadfile)) {
				    
				} else {
				    
				}
				@header('Location: http://cert.ru:8888/profile');
			}

			break;

		case '/generate_certificates':

			confirm_templates();
			@header('Location: http://cert.ru:8888/profile');

			break;

		case '/rm_certificates':

			rm_templates();
			@header('Location: http://cert.ru:8888/profile');

			break;

	}

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

				case '/registration_comp_agent':
					include("templates/section-reg-company-agent.php");
					break;

				case '/cart':
					if(isset($_COOKIE['code']))
						include("templates/section-cart.php");
					break;

				case '/restore':
					include("templates/section-restore.php");
					break;

				case '/profile':
					
					if(!isset($_COOKIE['code'])){
						echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
						break;
					}
					$type = $user['type'];
					if($type == 0)
						include("templates/section-profile.php");
					else 
						include("templates/section-profile-comp.php");

					break;

				case '/edit_profile':
						
					if(!isset($_COOKIE['code'])){
						echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
						break;
					}

					$type = $user['type'];
					
					if($type == 0)
						include("templates/section-edit-profile-user.php");
					else 
						include("templates/section-edit-profile-comp.php");
					
					break;

				case '/new_certificate':

					if(!isset($_COOKIE['code'])){
						echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
						break;
					}

					include("templates/section-new-certificates.php");
					break;

				case '/edit_certificates':

					if(!isset($_COOKIE['code'])){
						echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
						break;
					}

					include("templates/section-edit-certificates.php");
					break;

				case '/order':

					if(!isset($_COOKIE['code'])){
						echo "<p style='color:red; text-align:center'>Ошибка доступа!</p>";
						break;
					}

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
				
				default:
					// Подключение секции рекламы
					include("templates/section-advertising.php");
					break;
			}

			?>
			
			
		</div>
		
		<!-- Подключение подвала сайта -->
		<?include("templates/footer.php");?>
		<script type="text/javascript" src="jquery.js"></script>
		<script type="text/javascript" src="main.js"></script>
	</div>
</body>
</html>