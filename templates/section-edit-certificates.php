<section id="registration-data">
	<form action="requestHandler.php" method="post">
		<h2>Создание нового сертификата:</h2>
		<ul>
			<li>
				<input type="text" id="name" name="name" placeholder="Название">
			</li>
			<li>
				<input type="text" id="name" name="name" placeholder="Внутреннее название">
			</li>
			<li>
				<p>Описание сертификата:</p>
				<textarea>
					
				</textarea>
			</li>
			<li>
				<input type="text" id="price" name="price" placeholder="Цена">
			</li>
			<li>
				<input type="text" id="coastValue" name="coastValue" placeholder="Номинал">
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