// Script for finding unique ip addresses

#include <stdio.h>
#include <string.h>

int main(void) {
	//FILE *fdopen(int fd, const char *mode);
	//FILE *popen(const char *command, const char *type);
	//int pclose(FILE *stream)

	FILE *fp;
	char *command = "cat /var/www/Frugally/logs/ssl_access.log | grep -w 200 | grep -v -e '.jpg' | grep -v -i bot | awk '{print $1}' | sort -n | uniq -c | sort -nr";
        char outputIP[100];

	fp = popen(command,"r");
        if(fp==NULL){
		printf("Error during execution\n");
                return 0;
	}
	while(fscanf(fp, "%*s %s ", outputIP)==1) {
		if(strcmp(("%s",outputIP),"192.168.1.1")!=0) {
			printf("%s\n", outputIP);

			FILE *fp2;
			char getLocation[100] = "curl https://freegeoip.app/xml/";
			char locationIP[100];

			strcat(getLocation, outputIP);
			fp2 = popen(getLocation, "r");
			if(fp2==NULL) {
				printf("Error executing second script\n");
				return 0;
			}
			while(fscanf(fp2, "%s ", locationIP)==1){
				printf("%s\n", locationIP);
			}
			fclose(fp2);
		}
	}

	fclose(fp);
        return 0;
}
