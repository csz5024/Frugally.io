#!/usr/bin/php
<?php
        putenv('PYTHONPATH=/home/frugally/.local/lib/python3.6/site-packages');
        $output=exec("cd /var/www/Frugally/Frugally/nordstromracksales && scrapy crawl NordstromRackWomen");

        echo "<pre>$output</pre>";
?>


