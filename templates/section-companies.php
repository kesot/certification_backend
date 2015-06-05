<?php

	$comp = get_companies();

?>

<?if($comp !== 0):?>

<section id="cities">
	<ul class="unlist">
		<?for ($i=0; $i < count($comp); $i++):?>
			<li>
				<a href="/certificates_by_company?comp_id=<?=$comp[$i]['Id']?>"><?=$comp[$i]['Name']?></a>
			</li>
		<?endfor;?>
	</ul>
</section>

<?endif;?>

<!-- 
	
	js handler for li click
	add ID on each company
	send request for take companies certificates

 -->