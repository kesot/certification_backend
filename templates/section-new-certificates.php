<section id="registration-data">
	<form action="/add_template" method="post" enctype="multipart/form-data">
		<input type="hidden" name="MAX_FILE_SIZE" value="30000000" />
		<h2>Создание нового сертификата:</h2>
		<ul>
			<li>
				<input type="text" id="name" name="name" placeholder="Название">
			</li>
			<li>
				<input type="text" id="AdministrativeName" name="AdministrativeName" placeholder="Внутреннее название">
			</li>
			<li>
				<input type="text" id="mask" name="mask" placeholder="Маска шаблона">
			</li>
			<li>
				<p>Описание сертификата:</p>
				<textarea rows="1" name="Descitption">
					
				</textarea>
			</li>
			<li>
				<input type="text" id="price" name="price" placeholder="Цена">
			</li>
			<li>
				<input type="text" id="CostValue" name="CostValue" placeholder="Номинал">
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