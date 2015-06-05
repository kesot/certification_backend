<?php 

	$cert = get_certs();


?>

<section id="one-cert-data">
	<div class="data-table">
		<div class="data-row">
			<div class="data-cell">
				<img src="<?=$cert['Id']?>.jpg">
			</div>
			<div class="data-cell">
				<section class="about-cert">
					<h3>
						Подарочная карта:
						<span id="comp-name"><?=$cert['Name']?></span>
					</h3>
					<ul>
						<li>
							Номинал: 
							<div class="select">
								<p>></p>
								<select name="cost" id="">
									<option value=<?=$cert['CostValue']?> > 
										<?=$cert['CostValue']?>
									</option>
								</select>
							</div>
						</li>
						<li><a class="button" href="/add_to_cart?id=<?=$cert['Id']?>">Добавить в корзину</a></li>
						<li><input type="button" value="Запомнить"></li>
						<li class="cut">
							<p>
								<?=$cert['Descitption']?>
							</p>
						</li>
						<li>
							<p>
								По желанию Вы можете вписать свое имя и/или фамилию в поле ниже:
							</p>
						</li>
						<li>
							<input class="wide" type="text" placeholder="Ваша фамилия и/или имя" name="fio">
						</li>
						<li>Так же Вы можете написать свое поздравление</li>
						<li><textarea></textarea></li>
						<li><input class="" type="button" value="Сохранить"></li>
					</ul>
				</section>
			</div>
		</div>
	</div>
</section>