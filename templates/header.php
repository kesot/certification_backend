<header id="main">
			
	<div class="data-table">
		<div class="data-row">
			<div class="data-cell">
				<a href="/" class="list-city">г.Москва &#9660;</a>
				<a href="/" class="about-us">О нас</a>
				<a href="/" class="contacts">Контакты</a>
			</div>
			<div class="data-cell"><h1>Certificado</h1></div>
			<div class="data-cell">
				
				<?php

					if(isset($_COOKIE['code']) && !empty($_COOKIE['code']))
						include("cart-in-page.php");
					else
						include("section-auth-user.php");
				?>
				
			</div>
		</div>
	</div>
	
</header>