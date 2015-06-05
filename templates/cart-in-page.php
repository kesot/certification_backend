<?php 

	$user_data = get_user();
	$user_cart = get_cart();

	if($user_data == 0) 


?>
 
<section id="cart-in-page">
	<div class="data-table">
		<div class="data-row">
			
			<div class="data-cell">
				<section id="user-menu">
					<p>
						Привет, 
						<?php
							if($user_data['type'] == 0) echo $user_data['sname'];
							else echo $user_data['login'];

						?>

					</p>
					<ul class="unlist">
						<li><a href="/profile">Профиль</a></li>
						<li><a href="/logout">Выход</a></li>
					</ul>
				</section>
			</div>
			<?if($user_data['type'] == 0):?>
			<div class="data-cell">
				<section id="cart">
					<p>Корзина</p>

					<?if( count($user_cart) <= 0 && !$user_cart):?>
						<p>Пусто :(</p>
					<?else:?>
						<p>
							Сертификатов: 
							<span id="cart-count">
								<?=count($user_cart)?>
							</span> 
							шт.
						</p>

						<p>
							<?php
								$sum = 0;
								for ($i=0; $i < count($user_cart); $i++) { 
									$sum += $user_cart['Certificates'][$i]['CertificateSet']['Price'];
								}
								
							?>
							На сумму:
								<span id="cart-sum"> <?=$sum?> </span>
							руб.
						</p>
						<a class="button" href="/cart">Оформить заказ</a>
					<?endif;?>
					
				</section>
			</div>
			<?endif?>

		</div>
	</div>
</section>