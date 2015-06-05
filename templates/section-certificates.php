<?php 

	$certs = get_certs();

 ?>

<section id="advertising">

	<div class="table-row">
		<?for ($i=0; $i < count($certs); $i++):?>

		<div class="cell">
			<div class="data-table">
				<div class="data-row">
					<div class="data-cell">
						<img src="/<?=$certs[$i]['Id']?>.jpg" alt="Comment">
					</div>
				</div>
				<div class="data-row">
					<div class="data-cell">
						<a href="/certificates_one?id=<?=$certs[$i]['Id']?>" class="button">Подробнее</a>
						<a href="/add_to_cart?id=<?=$certs[$i]['Id']?>" class="button">В корзину</a>
					</div>
				</div>
			</div>
		</div >

		<?endfor;?>
	</div>

</section>