<!-- 
	
	php handler for take info about user
	user from company can edit only password
	take companies templates for certificates (ID)

 -->

<?php 

	$temp = get_templates();

?>

<section id="profile">
	<div class="data-table">
		<div class="data-row">
			<div class="data-cell">
				<section id="about-user">
					<ul class="unlist">
						<li>Мой логин: <span>login</span></li>
						<li>Моя компания: <span>МВидео</span></li>
						<li><a href="/edit_profile">Изменить пароль</a></li>
						<li><a href="/new_certificate">Создать шаблон</a></li>
					</ul>
				</section>
			</div>
		</div>			
	</div>
	<section id="orders">
		<h2>Шаблоны компании</h2>
		<?if(!$temp):?>
			<p style="text-align: center">Ваша компания не создала еще ни одного шаблона</p>
		<?else:?>
		<p class="alert"><sup>*</sup> после генерации удаление шаблона не возможно!</p>
		<table>
			<thead>
				<tr>
					<td></td>
					<td>№</td>
					<td>Название</td>
					<td>Внутреннее название</td>
					<td>Маска</td>
					<td>Описание</td>
					<td>Цена</td>
					<td>Номинал</td>
					<td></td>
					<td></td>
				</tr>
			</thead>
			<tbody>
				<?for ($i=0; $i < count($temp); $i++):?>
				<tr>
					<td><img src="<?=$temp[$i]['Id']?>.jpg" alt=""></td>
					<td><?=$i?></td>
					<td><?=$temp[$i]['Name']?></td>
					<td><?=$temp[$i]['AdministrativeName']?></td>
					<td><?=$temp[$i]['MaskString']?></td>
					<td><?=$temp[$i]['Descitption']?></td>
					<td><?=$temp[$i]['Price']?></td>
					<td><?=$temp[$i]['CostValue']?></td>
					<?if($temp[$i]['AllCertificatesGenerated'] == false):?>
					<td><a href="/edit_certificates?id=<?=$temp[$i]['Id']?>">Изменить</a></td>
					<td>
						<a href="/generate_certificates?id=<?=$temp[$i]['Id']?>">Сгенерировать</a>/
						<a href="/rm_certificates?id=<?=$temp[$i]['Id']?>" class="alert">Удалить</a>
					</td>
					<?endif?>
				</tr>
				<?endfor?>
			</tbody>
		</table>
		<?endif?>
	</section>
</section>