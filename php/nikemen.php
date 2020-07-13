#!/usr/bin/php
<?php
	$output=exec("cd /var/www/Frugally/Frugally/nordstromracksales && sudo scrapy crawl NikeMen");

	echo "<pre>$output</pre>";
?>
