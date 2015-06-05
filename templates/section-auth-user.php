<form action="/login" method="POST">
	<fieldset>
		<legend>Вход</legend>
		<div class="data-table">
			<div class="data-row">
				<div class="data-cell">
					<input type="text" name="login" placeholder="Логин">
				</div>
			</div>
			<div class="data-row">
				<div class="data-cell">
					<input type="password" name="password" placeholder="Пароль">
				</div>
			</div>
			<div class="data-row">
				<div class="data-cell">
					<input type="checkbox" name="type" value="1">Я партнер
				</div>
			</div>
			<div class="data-row">
				<div class="data-cell">
					<input type="submit" value="Войти">
				</div>
			</div>
		</div>
		<a href="/registration" class="href">Регистрация</a>
		<a href="/restore" class="href">Восстановить пароль</a>
	</fieldset>
</form>