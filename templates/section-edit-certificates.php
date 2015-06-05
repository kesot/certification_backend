<!-- 

	take by ID certificate that we need

 -->

<?php

	$temp = get_templates();
	$id = -1;
	for ($i=0; $i < count($temp); $i++) { 
		if($temp[$i]['Id'] == $_GET['id']){
			$id = $i;
			break;
		}
	}



	if($id == -1) 
		@header('Location: http://cert.ru:8888/profile');

?>


<section id="registration-data">
	<form action="/update_template" method="post" enctype="multipart/form-data">
		<input type="hidden" name="MAX_FILE_SIZE" value="9999999999" />
		<input type="hidden" name="CompanyId" value="<?=$temp[$i]['CompanyId']?>">
		<input type="hidden" name="id" value=<?=$temp[$i]['Id']?>>
		<input type="hidden" name="MaskString" value=<?=$temp[$i]['MaskString']?>>
		<h2>Создание нового сертификата:</h2>
		<ul>
			<li>
				<input type="text" id="name" name="name" placeholder="Название" value=<?=$temp[$id]['Name']?>>
			</li>
			<li>
				<input type="text" id="AdministrativeName" name="AdministrativeName" placeholder="Внутреннее название" value=<?=$temp[$id]['AdministrativeName']?>>
			</li>
			<li>
				<p>Описание сертификата:</p>
				<textarea name="Descitption">
					<?=$temp[$id]['Descitption']?>
				</textarea>
			</li>
			<li>
				<input type="text" id="price" name="price" placeholder="Цена" value=<?=$temp[$id]['Price']?>>
			</li>
			<li>
				<input type="text" id="CostValue" name="CostValue" placeholder="Номинал" value=<?=$temp[$id]['CostValue']?>>
			</li>
			<li>
				<p>Выберите фото сертификата</p>
				<input type="file" name="photo">
			</li>
			<li>
				
			</li>
			<li>
				<input type="submit" value="Далее">
			</li>
		</ul>
	</form>
</section>