<!-- 

	php handler for take user info
 -->

<section id="registration-data">
	<form action="/send_update_user" method="post">
		<h2>Изменение данных:</h2>
		<ul>
			<p><sup>*</sup>- поля которые вы не хотите изменять оставьте пустыми</p>
			<li>
				<input type="text" id="fname" name="fname" placeholder="Фамилия">
			</li>
			<li>
				<input type="text" id="sname" name="sname" placeholder="Имя">
			</li>
			<li>
				<input type="text" id="mname" name="mname" placeholder="Отчество">
			</li>
			<li>
				<input type="email" id="email" name="email" placeholder="Эл.почта">
			</li>
			<li>
				<input type="password" id="password" name="password" placeholder="Пароль">
			</li>
			<li>
				<input type="password" id="repassword" name="repassword" placeholder="Повторите пароль">
			</li>
			<li>
				<input type="submit" value="Далее">
			</li>
		</ul>
	</form>
</section>


<!-- 

	js handler for password identity

 -->