<?php

require_once('SF_API.php');

$api = new SF_API_XMLRPC();

printf("Server version: %s\n", $api->infoVersion());
echo "Result: ".$api->messageInput(new SF_Message('Is this message SPAM?'))."\n";

