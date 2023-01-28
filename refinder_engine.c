#include "refinder_engine.h"
#include "kmp.c"
#include <stdlib.h>
#include <string.h>
#include <ftw.h>
#include <sys/stat.h>
 
unsigned long long files_count = 0;
char search_pattern[261] = {'\0'};
pfile file_list = NULL;
struct stat sbuf;

static int addNode(pfile *table, const char *file_name, char file_type, off_t file_size, time_t edit_time)
{
	pfile nextNode = (pfile)malloc(sizeof(file));
	memset(nextNode->file_name, '\0', sizeof(nextNode->file_name));
	nextNode->file_type = file_type;
	nextNode->file_size = file_size;
	nextNode->edit_time = edit_time;
	strcpy(nextNode->file_name, file_name);
	nextNode->next = *table;
	*table = nextNode;
	return 0;
}

static int freeNode(pfile *table)
{
	pfile cache = *table;
	while (cache != NULL)
	{
		pfile temp = cache;
		cache = cache->next;
		free(temp);
	}
	*table = NULL;
	return 0;
}

static int path_process(const char *file_name, const struct stat *sb, int flag)
{
	files_count++;
	if (KMP(file_name, search_pattern)) return 0;
	stat(file_name, &sbuf);
	if (flag == FTW_D || flag == FTW_DNR || flag == FTW_DP)
	{
		addNode(&file_list, file_name, 'D', sbuf.st_size, sbuf.st_mtime); //Directory.
	}
	else if (flag == FTW_F)
	{
		addNode(&file_list, file_name, 'F', sbuf.st_size, sbuf.st_mtime); //Normal File.
	}
	else if (flag == FTW_SL || flag == FTW_SLN)
	{
		addNode(&file_list, file_name, 'L', sbuf.st_size, sbuf.st_mtime); //Symbolic Link.
	}
	else
	{
		addNode(&file_list, file_name, 'U', sbuf.st_size, sbuf.st_mtime);  //Unknown.
	}
	return 0;
}

DLL_EXPORT unsigned long long __stdcall return_files_count(void) {return files_count;}

DLL_EXPORT pfile __stdcall find(char *workdir, char *pattern)
{
	files_count = 0;
	freeNode(&file_list);
	memset(search_pattern, '\0', sizeof(search_pattern));
	strncpy(search_pattern, pattern, 260);
	ftw(workdir, path_process, 1000);

	return file_list;
}
