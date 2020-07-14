// Copyright (C) 1998 - 2019, Daniel Stenberg, <daniel@haxx.se>, et al.

#include <stdio.h>
#include <time.h>
#include <curl/curl.h>

int runCurl(void) {
        CURL *curl;
	CURLcode res;

	curl_global_init(CURL_GLOBAL_DEFAULT);
	curl = curl_easy_init();
	if(curl) {
		curl_easy_setopt(curl, CURLOPT_URL, "https://frugally.io/home");

		/* Skip verification steps here */

		/* Perform the request */
		res = curl_easy_perform(curl);
		/* Check for errors */
		if(res != CURLE_OK)
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

		//printf("%d", res);
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
	return 0;
}

int main(void) {
	clock_t begin = clock();
	for(int i=0; i<100; i++) {
		runCurl();
	}
	clock_t end = clock();
	double time_spent = (double)(end-begin)/CLOCKS_PER_SEC;
	printf("\ntime spent: %f\n", time_spent);
	printf("\naverage time per page: %f\n", time_spent/100);
	return 0;
}

