<?php 

	$cart = get_cart();

?>

<section id="order-cart">
	<section id="goods">
		<h2>Корзина</h2>
		<?if(!$cart):?>
			<p style="text-align: center">Ваша корзина пуста</p>
		<?else:?>
		<table>
			<thead>
				<tr>
					<td>№</td>
					<td>Название</td>
					<td>Номинал</td>
					<td>Удалить</td>
				</tr>
			</thead>
			<tbody>
				<?for ($i=0; $i < count($cart) -1; $i++):?>
				<tr>
					<td><?=$i+1?></td>
					<td><?=$cart['Certificates'][$i]['CertificateSet']['Name']?></td>
					<td><?=$cart['Certificates'][$i]['CertificateSet']['CostValue']?> руб.</td>
					<td><a href="/rm_cert?id=<?=$cart['Certificates'][$i]['CertificateSet']['Id']?>">Удалить</a></td>
				</tr>
				<?endfor;?>
			</tbody>
		</table>
	</section>
	<section id="total">
		<?php
			$sum = 0;
			for ($i=0; $i < count($user_cart); $i++) { 
				$sum += $user_cart['Certificates'][$i]['CertificateSet']['Price'];
			}
			
		?>
		<p>Итоговая сумма: <span><?=$sum?></span> руб.</p>
		<a href="/confirm_cart" class="button">Оформить заказ</a>
	</section>
	<?endif?>
</section>

<!-- 
	js for send request on remove cert from cart 
	input button handler
-->