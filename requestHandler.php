<?php
	
	require ('vendor/autoload.php');

	use GuzzleHttp\Client;

	define('IP', 'http://104.46.40.129');
	

	define("ADD_USER",			IP."/user/add");
	define("GET_USER",			IP."/user/get");
	define("RM_USER",			IP."/user/delete");
	define("UPDATE_USER",		IP."/user/update");
	define("LOGIN",				IP."/user/login");
	define("LOGOUT",			IP."/user/logout");
	define("GET_COMPANIES",		IP."/companies");
	define("T_CERT_GET",		IP."/companies/templates/get");
	define("T_CERT_ADD",		IP."/companies/templates/add");
	define("T_CERT_UPDATE",		IP."/companies/templates/update");
	define("T_CERT_RM",			IP."/companies/templates/delete");
	define("T_CERT_CONFIRM",	IP."/companies/templates/confirm");
	define("CERT_GET",			IP."/certificateSets");
	define("CERT_GET_BY_COMP",	IP."/certificateSets/company");
	define("ORDERS_ALL",		IP."/orders/user");
	define("ORDERS_ONE",		IP."/orders/");
	define("CART_ADD",			IP."/orders/cart/add");
	define("CART_GET",			IP."/orders/cart/get");
	define("CART_RM",			IP."/orders/cart/delete");
	define("CART_CONFIRM",		IP."/orders/cart/confirm");



	/****************	Работа с пользователями		**************************************/




	// Отослать данные юзера при регистрации 
	function send_user_regData(){
		$client = new Client();
			
		if($_POST['password'] !== $_POST['repassword']) return 0;

		try{

			$response = $client->post(ADD_USER, [
			    'json' => [
			    	'type'		=>'0',
			        'fname'		=>$_POST['firstname'],
					'sname'		=>$_POST['secondname'],
					'mname'		=>$_POST['patronumic'],
					'email'		=>$_POST['email'],
					'login'		=>$_POST['login'],
					'password'	=>hash('sha256', $_POST['password']),
					'birthday'	=>$_POST['year'].'-'.$_POST['month'].'-'.$_POST['day']
		    	]
			]);
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}


		// Распарсить ответ

	}

	// Отослать данные для редактирования пользователя
	function send_user_editData(){
		$client = new Client();
		
		$json = array("json" => array());

		$json['json']['code'] = $_COOKIE['code'];

		if(isset($_POST['password']) && !empty($_POST['password']) && ($_POST['password'] == $_POST['repassword'])) 
			$json['json']['password'] = hash('sha256', $_POST['password']);
		else
			return 0;

		if(isset($_POST['fname']) && !empty($_POST['fname']))
			$json['json']['fname'] = $_POST['fname'];

		if(isset($_POST['sname']) && !empty($_POST['sname']))
			$json['json']['sname'] = $_POST['sname'];

		if(isset($_POST['mname']) && !empty($_POST['mname']))
			$json['json']['mname'] = $_POST['mname'];

		if(isset($_POST['email']) && !empty($_POST['email']))
			$json['json']['email'] = $_POST['email'];

		try{

			$response = $client->put(UPDATE_USER, $json);


		}
		catch(GuzzleHttp\Exception\RequestException $e){
			
			return 0;
		}

	}


	function send_agent_editData(){
		$client = new Client();
		
		$json = array("json" => array());

		$json['json']['code'] = $_COOKIE['code'];

		if(isset($_POST['password']) && !empty($_POST['password']) && ($_POST['password'] == $_POST['repassword'])) 
			$json['json']['password'] = hash('sha256', $_POST['password']);
		else
			return 0;

		try{
			$response = $client->put(UPDATE_USER, $json);
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			
			return 0;
		}

	}


	// Отослать данные юзера при авторизации 
	function user_auth(){
		
		$client = new Client();

		$type = 0;
		
		if(isset($_POST['type']) && $_POST['type'] == '1') $type = 1;

		try{

			$url = LOGIN.'?login='.$_POST['login'].'&password='.hash('sha256',$_POST['password'])."&type=".$type;
			$res = $client->get($url);
			
			$code = $res->json();
			$code = $code['code'];

			setcookie("code", $code, strtotime('+30 days'));

		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if($e->getResponse())
				echo $e->getResponse();
			return 0;
		}
		
		// Добавить code в куки если пользователь прошел

	}

	function user_logout(){
		$client = new Client();
		
		try{
			$response = $client->delete(LOGOUT, [
				    'json' => [
				        'code'	=> @$_COOKIE['code'],
			    	]
				]);

			setcookie("code", 0, time()-3600);
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			
			setcookie("code", 0, time()-3600);
		}

	}

	// get user
	function get_user(){

		$client = new Client();

		try{
			$response = $client->get(GET_USER.'?code='.@$_COOKIE['code']);

			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			
			return 0;

		}


	}

	// delete user
	function delete_user(){
		$client = new Client();
		
		try{
			$response = $client->delete(RM_USER, [
			    'json' => [
			        'code'	=> $_COOKIE['code'],
		    	]
			]);
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
		

	}




	function send_agent_regData(){
		$client = new Client();
			
		if($_POST['password'] !== $_POST['repassword']) return 0;

		try{

			$response = $client->post(ADD_USER, [
			    'json' => [
			    	'type'		=>'1',
			    	'company'	=> $_POST['name'],
					'login'		=>$_POST['login'],
					'password'	=>hash('sha256', $_POST['password']),
		    	]
			]);
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}


		// Распарсить ответ

	}



	function get_companies(){
		$client = new Client();
		
		try{
			$response = $client->get(GET_COMPANIES);
			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			
			return 0;
		}
	}


	function get_templates(){
		
		$client = new Client();
		
		try{

			// if(isset($_GET['id']) && !empty($_GET['id']))
			// 	$response = $client->get(T_CERT_GET."/".$_GET['id']."?code=".$_COOKIE['code']);
			// else
				$response = $client->get(T_CERT_GET."?code=".$_COOKIE['code']);
			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}

	function add_templates(){
		
		$client = new Client();
		
		try{
			$response = $client->post(T_CERT_ADD,[
				'json' => [

					"MaskString" 			=> $_POST['mask'], 
					"AdministrativeName" 	=> $_POST['AdministrativeName'], 
					"Name" 					=> $_POST['name'],
					"Descitption" 			=> $_POST['Descitption'],
					"code" 					=> $_COOKIE['code'],
					"Price" 				=> $_POST['price'],
					"CostValue" 			=> $_POST['CostValue']


				]]);

			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}


	function update_templates(){
		
		$client = new Client();
		
		try{
			$response = $client->put(T_CERT_UPDATE,[
				'json' => [

					"id"					=> $_POST['id'], 
					"MaskString" 			=> $_POST['MaskString'], 
					"CompanyId" 			=> $_POST['CompanyId'], 
					"AdministrativeName" 	=> $_POST['AdministrativeName'], 
					"Name" 					=> $_POST['name'],
					"Descitption" 			=> $_POST['Descitption'],
					"code" 					=> $_COOKIE['code'],
					"Price" 				=> $_POST['price'],
					"CostValue" 			=> $_POST['CostValue']


				]]);

			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}

	function confirm_templates(){
		
		$client = new Client();
		
		try{
			$response = $client->post(T_CERT_CONFIRM,[
				'json' => [
					
					"id" 	=> $_GET['id'],
					"code" 	=> $_COOKIE['code']

				]]);

			$data = $response->json();
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}

	function rm_templates(){
		
		$client = new Client();
		
		try{
			$response = $client->delete(T_CERT_RM,[
				'json' => [

					"id" 	=> $_GET['id'],
					"code" 	=> $_COOKIE['code']

				]]);

			$data = $response->json();
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}




	function get_certs(){

		$client = new Client();


		try{
			if(isset($_GET['id']) && !empty($_GET['id']))
				$url = CERT_GET."/".$_GET['id'];
			
			else if(isset($_GET['comp_id']) && !empty($_GET['comp_id']))
				$url = CERT_GET_BY_COMP.'?companyId='.$_GET['comp_id'];
			else
				$url = CERT_GET."?pageIndex=0&pageSize=5";

			$response = $client->get($url);

			$data = $response->json();

			return $data;

		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}


	}


	function get_orders(){

		$client = new Client();


		try{
			if(isset($_POST['id']) && !empty($_POST['id']))
				$response = $client->get(ORDERS_ONE.'?id='.$_POST['id']."&code=".$_COOKIE['code']);
			else
				$response = $client->get(ORDERS_ALL."?code=".$_COOKIE['code']);

			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}


	}




	function add_to_cart(){
		
		$client = new Client();
		
		try{
			$response = $client->post(CART_ADD,[
				"json" =>[

					"code" 	=> $_COOKIE['code'],
					"id" 	=> $_GET['id']
				]
			]);
			$data = $response->json();
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
			return 0;
		}
	}

	function get_cart(){
		
		$client = new Client();
		
		try{
			$response = $client->get(CART_GET.'?code='.$_COOKIE['code']);

			$data = $response->json();
			return $data;
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
			}
			return 0;
		}
	}


	function delete_from_cart(){
		
		$client = new Client();
		
		try{
			$response = $client->delete(CART_RM,[
				'json' => [

					"certificates"	=> $_GET['id'],
					"code" 			=> $_COOKIE['code']

				]]);

			$data = $response->json();
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}

	function confirm_cart(){
		
		$client = new Client();
		
		try{
			$response = $client->post(CART_CONFIRM,[
				'json' => [
					
					"code" => $_COOKIE['code']

				]]);

			$data = $response->json();
		}
		catch(GuzzleHttp\Exception\RequestException $e){
			if ($e->hasResponse()) {
				echo $e->getResponse(). "<br>"; 
			}
		}
	}


?>