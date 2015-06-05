<?php

	$usr = get_user();
	$orders = get_orders();

	if(!$orders && count($orders) <= 0) $orders = 0;
?>
<!-- 
	php handler for take user's info 
	take user's info and he's orders
 -->

<section id="profile">
	<div class="data-table">
		<div class="data-row">
			<div class="data-cell">
				<div class="avatar">
					<img src="1.jpg">
					<a href="">Изменить фото</a>
				</div>
			</div>
			<div class="data-cell">
				<section id="about-user">
					<ul class="unlist">

						<li>Фамилия: <span><?=$usr['fname']?></span></li>
						<li>Имя: <span><?=$usr['sname']?></span></li>
						<li>Дата рождение: <span><?=date($usr['birthday'])?></span></li>
						<li>Логин: <span><?=$usr['login']?></span></li>
						<li>Эл.почта: <span><?=$usr['email']?></span></li>
						<li><a href="/edit_profile?code=<?=$_COOKIE['code']?>">Редактировать профиль</a></li>
					</ul>
				</section>
			</div>
		</div>			
	</div>
	<section id="orders">
		<h2>Мои покупки</h2>
		<?if (!$orders):?>
			<p style="text-align: center;">Вы еще ничего не заказывали!</p>
		<?else:?>
		<table>
			<thead>
				<tr>
					<td>№</td>
					<td>Дата покупки</td>
					<td>Кол-во сертификатов</td>
					<td>Сумма</td>
					<td>Просмотр</td>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>1</td>
					<td>01.01.2015</td>
					<td>5</td>
					<td>15000</td>
					<td><a href="/ordes?id=1">Просмотр</a></td>
				</tr>
			</tbody>
		</table>
		<?endif;?>
	</section>
</section>