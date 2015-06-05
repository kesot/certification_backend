<?php
	
	unset($_GET['id']);
	$certs = get_certs();

	if(count($certs) >= 4) $count = 4;
	else $count = count($certs);
?>

<section id="advertising">

	<div class="table-row">
		<?for($i=0; $i < $count; $i++):?>
		<div class="cell">
			<div class="up-cell">
				<span><?=$certs[$i]['Name']?></span>
				<input class="cert" type="button" value="Подробнее" data-id="/certificates_one?id=<?=$certs[$i]['Id']?>">
			</div>
			<img src="/<?=$certs[$i]['Id']?>.jpg" alt="Comment">
		</div >
		<?endfor;?>
	</div>

</section>