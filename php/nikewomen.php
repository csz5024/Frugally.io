#!/usr/bin/php
<?php
        $output=exec("cd /var/www/Frugally/Frugally/nordstromracksales && sudo scrapy crawl NikeWomen");

        echo "<pre>$output</pre>";
?>


