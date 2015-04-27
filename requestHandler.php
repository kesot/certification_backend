<?php
	
	require ('vendor/autoload.php');

	use GuzzleHttp\Client;

	define('IP', '');
	
	define("RM_USER",			"http://".IP."/remove_user");
	define("REG_USER",			"http://".IP."/add_user");
	define("LOGIN_USER",		"http://".IP."/login");
	define("LOGOUT_USER",		"http://".IP."/logout");
	define("GET_DATA_USER",		"http://".IP."/get_user");
	define("EDIT_DATA_USER",	"http://".IP."/update_user");



	/****************	Работа с пользователями		**************************************/




	// Отослать данные юзера при регистрации 
	function send_user_regData(){
		$client = new Client();
		
		$response = $client->post(REG_USER, [
		    'json' => [
		        'fname'		=>$_POST['firstname'],
				'sname'		=>$_POST['secondname'],
				'mname'		=>$_POST['patronumic'],
				'email'		=>$_POST['email'],
				'login'		=>$_POST['login'],
				'password'	=>hash('sha256', $_POST['password']),
				'birthday'	=>$_POST['year'].'-'.$_POST['month'].'-'.$_POST['day']
	    	]
		]);

		// Распарсить ответ

	}

	// Отослать данные для редактирования пользователя
	function send_user_editData(){
		$client = new Client();
		
		$response = $client->put(EDIT_DATA_USER, [
		    'json' => [
		    	'code'		=> $_COOKIE['code'],
		        'fname'		=>$_POST['firstname'],
				'sname'		=>$_POST['secondname'],
				'mname'		=>$_POST['patronumic'],
				'email'		=>$_POST['email'],
				'password'	=>hash('sha256', $_POST['password']),
				'birthday'	=>$_POST['year'].'-'.$_POST['month'].'-'.$_POST['day']
	    	]
		]);

		// Распарсить ответ

	}


	// Отослать данные юзера при авторизации 
	function user_auth(){
		$client = new Client();
		
		$response = $client->get(LOGIN_USER.'?login='.$_POST['login'].'&password='.hash('sha256',$_POST['password']));
		
		// Добавить code в куки если пользователь прошел

	}

	function user_logout(){
		$client = new Client();
		
		$response = $client->delete(LOGOUT_USER, [
		    'json' => [
		        'code'	=> $_COOKIE['code'],
	    	]
		]);

	}

	// get user
	function get_user(){

		$client = new Client();
		$response = $client->get(GET_DATA_USER.'?code='.$_COOKIE['code']);


	}

	// delete user
	function delete_user(){
		$client = new Client();
		
		$response = $client->delete(RM_USER, [
		    'json' => [
		        'code'	=> $_COOKIE['code'],
	    	]
		]);
		
		// получить ответ 

	}



	/****************	Работа с сертификатами 	**********************************************/

	// Отослать данные при оформлении заказа
	function send_order_data(){

	}

	// Отослать данные при запросе инфы о конкретном заказе
	function send_oneOrder_data(){

	}


?>