#!/usr/bin/php
<?php
        $output=exec("cd /var/www/Frugally/Frugally/nordstromracksales && sudo scrapy crawl NordstromRackWomen");

        echo "<pre>$output</pre>";
?>


