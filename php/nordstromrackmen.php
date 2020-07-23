#!/usr/bin/php
<?php
        $output=shell_exec("cd /var/www/Frugally/Frugally/nordstromracksales && scrapy crawl NordstromRackMen");

        echo "<pre>$output</pre>";
?>


